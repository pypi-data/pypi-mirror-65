import json
import logging
import pathlib
import sys
import zipfile
from collections import namedtuple
from datetime import datetime
from io import BytesIO, StringIO

import rebotics_sdk

logger = logging.getLogger(__name__)

ClassificationEntry = namedtuple('ClassificationEntry', ['label', 'feature', 'image', 'filename'])


class ClassificationDatabaseException(Exception):
    pass


class BaseClassificationDatabasePacker(object):
    version = 0
    extension = 'zip'

    def __init__(self, source=None, destination=None):
        self.source = source
        self.destination = destination
        self.meta_data = {
            'packed': datetime.now().strftime('%c'),
            'sdk_version': rebotics_sdk.__version__,
            'packer_version': self.version
        }
        self.images = []

        if self.destination is None:
            self.destination = BytesIO()
        elif isinstance(self.destination, str):
            self.destination = "{}.{}".format(self.destination, self.extension)
        else:
            raise ClassificationDatabaseException('destination should be None or path-like')

    def read_lines(self, lines):
        return [x for x in lines.split('\n') if x]

    def zipfile(self, file, **kwargs):
        # if python version is
        params = dict(
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True,
        )

        if (sys.version_info.major, sys.version_info.minor) >= (3, 7):
            # using the most aggressive compression
            params['compresslevel'] = 9  # default is 6

        params.update(kwargs)

        for compression_option in [zipfile.ZIP_BZIP2, zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED]:
            try:
                params['compression'] = compression_option
                return zipfile.ZipFile(
                    file, **params
                )
            except RuntimeError:
                pass

    def pack(self, *args, **kwargs):
        raise NotImplementedError()

    def unpack(self):
        raise NotImplementedError()


class ZipDatabasePacker(BaseClassificationDatabasePacker):
    """
    Unified file format for packing classification database into single folder
    File format is the zip based archive with following :

    labels.txt
    features.txt
    meta.json
    """
    version = 0
    extension = 'zip'

    def pack(self, labels, features, *args, **kwargs):
        labels_io = StringIO("\n".join(labels))
        features_io = StringIO("\n".join(features))
        self.meta_data['count'] = len(labels)

        with self.zipfile(self.destination, mode='w') as zip_io:
            zip_io.writestr('labels.txt', labels_io.getvalue())
            zip_io.writestr('features.txt', features_io.getvalue())
            zip_io.writestr('meta.json', json.dumps(self.meta_data))
        return self.destination

    def unpack(self):
        if self.source is None:
            raise ClassificationDatabaseException("Can not unpack with empty source file")

        with self.zipfile(self.source, mode='r') as zip_io:
            try:
                self.meta_data = json.load(zip_io.open('meta.json'))
            except KeyError:
                # meta.json is not presented, working in the compatibility mode
                pass

            labels = self.read_lines(zip_io.read('labels.txt').decode('utf-8'))
            features = self.read_lines(zip_io.read('features.txt').decode('utf-8'))

            for label, feature in zip(
                labels,
                features,
            ):
                yield ClassificationEntry(
                    label, feature, None, None
                )


class ClassificationDatabasePacker(BaseClassificationDatabasePacker):
    """
    Unified file format for packing classification database into single folder
    File format is the zip based archive with following :

    labels.txt
    features.txt
    meta.json
    images/  - folder with images, this folder can be empty
    """

    version = 1
    extension = 'rcdb'
    images_extensions = [
        'jpeg', 'png', 'jpg',
    ]

    def extract_meta_data(self, labels_path, features_path, images_folder):
        for f in pathlib.Path(images_folder).iterdir():
            if f.is_file():
                for ext in self.images_extensions:
                    if f.name.endswith(ext):
                        self.images.append((f.name, f))

        self.images.sort(key=lambda i: i[0])  # sort by filename

        with open(labels_path, 'r') as labels_io, open(features_path, 'r') as features_io:
            labels = self.read_lines(labels_io.read())
            features = self.read_lines(features_io.read())

        labels_count = len(labels)
        features_count = len(features)
        files_count = len(self.images)

        if labels_count != features_count:
            raise ClassificationDatabaseException('Inconsistent count of labels and features. {}/{}'.format(
                labels_count, features_count
            ))

        if labels_count != files_count:
            raise ClassificationDatabaseException(
                'Inconsistent count of labels and features and files. {}/{}/{}'.format(
                    labels_count, features_count, files_count
                ))

        self.meta_data.update({
            'count': features_count,
            'images': [str(f[0]) for f in self.images]
        })

    def pack(self, labels_path, features_path, images_folder):
        self.extract_meta_data(labels_path, features_path, images_folder)

        with self.zipfile(self.destination, mode='w') as zip_io:
            zip_io.write(labels_path, 'labels.txt')
            zip_io.write(features_path, 'features.txt')
            for name, path in self.images:
                zip_io.write(path, pathlib.Path('images') / name)

            zip_io.writestr('meta.json', json.dumps(self.meta_data))

        return self.destination

    def unpack(self):
        """

        :return: generator of label, feature, image_io
        :rtype:self.meta_data
        """
        if self.source is None:
            raise ClassificationDatabaseException("Can not unpack with empty source file")

        with self.zipfile(self.source, mode='r') as zip_io:
            self.meta_data = json.load(zip_io.open('meta.json'))

            labels = self.read_lines(zip_io.read('labels.txt').decode('utf-8'))
            features = self.read_lines(zip_io.read('features.txt').decode('utf-8'))

            for label, feature, image_name in zip(
                labels,
                features,
                self.meta_data['images']
            ):
                image = zip_io.read('images/{}'.format(image_name))
                yield ClassificationEntry(
                    label, feature, image, image_name
                )

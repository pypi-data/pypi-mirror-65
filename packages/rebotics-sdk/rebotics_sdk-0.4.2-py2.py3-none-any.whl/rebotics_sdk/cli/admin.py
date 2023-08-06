import datetime
import json
import os
import pathlib
from functools import partial
from multiprocessing.pool import Pool

import click
import humanize
import requests
from prettytable import PrettyTable
from pynotifier import Notification

from rebotics_sdk.cli.common import shell, configure, roles
from .utils import ReboticsCLIContext, app_dir, pass_rebotics_context, read_saved_role, process_role
from ..advanced.packers import ClassificationDatabasePacker, ClassificationDatabaseException
from ..providers import AdminProvider, RetailerProvider, sleep
from ..providers.facenet import FacenetProvider
from ..utils import Timer


@click.group()
@click.option('-f', '--format', default='table', type=click.Choice(['table', 'id', 'json']), help='Result rendering')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-c', '--config', type=click.Path(), default='admin.json', help="Specify what config.json to use")
@click.option('-r', '--role', default=lambda: read_saved_role('admin'), help="Key to specify what admin to use")
@click.version_option()
@click.pass_context
def api(ctx, format, verbose, config, role):
    """
    Admin CLI tool to communicate with dataset API
    """
    process_role(ctx, role, 'admin')
    ctx.obj = ReboticsCLIContext(
        role,
        format,
        verbose,
        os.path.join(app_dir, config),
        provider_class=AdminProvider
    )


def get_retailer_version_task(retailer_dict):
    retailer_provider = RetailerProvider(host=retailer_dict['host'], retries=1, timeout=5)
    try:
        response = retailer_provider.version()
        version = response['version']
        uptime = humanize.naturaldelta(datetime.timedelta(seconds=int(response['uptime'])))
    except Exception:
        version = 'not working'
        uptime = '---'

    d = [
        retailer_dict['codename'],
        retailer_dict['title'],
        version,
        uptime,
        retailer_dict['host'],
    ]
    return d


@api.command()
@click.argument('retailer')
@pass_rebotics_context
def configurations(ctx, retailer):
    try:
        res = ctx.provider.get_configurations(retailer)
        ctx.format_result(res)
    except Exception as exc:
        raise click.ClickException(exc)


@api.command()
@click.option('-n', '--notify', is_flag=True)
@click.option('-d', '--delay', type=click.INT, default=60)
@pass_rebotics_context
def retailer_versions(ctx, notify, delay):
    """Fetch retailer versions and their meta information"""
    if notify:
        if ctx.verbose:
            click.echo('Using notify option', err=True)
        Notification(
            title='Subscribed to the notifications',
            description='You will receive notifications for retailer updates',
        ).send()

    provider = ctx.provider
    if ctx.verbose:
        click.echo('Fetching info from rebotics admin.', err=True)
    retailers = provider.get_retailer_list()
    prev_results = []
    results = []
    pool = Pool(len(retailers))

    while True:
        try:
            if ctx.verbose:
                click.echo('Fetching the retailer versions', err=True)
            results = pool.map(get_retailer_version_task, retailers)

            if not notify:
                break

            for prev_result in prev_results:
                retailer_codename = prev_result[0]
                previous_version = prev_result[2]
                for result in results:
                    if result[0] == retailer_codename:
                        current_version = result[2]
                        if previous_version != current_version:
                            notification_message = 'Retailer {} updated from version {} to {}'.format(
                                retailer_codename,
                                previous_version,
                                current_version
                            )
                            click.echo(notification_message)
                            Notification(
                                title=notification_message,
                                description='Current uptime is: {}'.format(result[3]),
                                duration=30,
                                urgency=Notification.URGENCY_CRITICAL,
                            ).send()
            del prev_results
            prev_results = results
            sleep(delay)
        except KeyboardInterrupt:
            break

    table = PrettyTable()
    table.field_names = ['codename', 'title', 'version', 'uptime', 'host']
    for result in results:
        table.add_row(result)
    click.echo(table)


def load_models(ctx, retailer_id, retailer_secret):
    provider = ctx.provider
    provider.set_retailer_identifier(retailer_id, retailer_secret)
    return provider.get_retailer_tf_models()


@api.command()
@click.option('-r', '--retailer-id', help='Retailer id')
@click.option('-s', '--retailer-secret', help='Retailer secret key')
@click.option('-u', '--facenet-url', help='Facenet service URL')
@click.argument('image_url')
@pass_rebotics_context
def extract_feature_vectors(ctx, retailer_id, retailer_secret, facenet_url, image_url):
    """Fetches latest configuration of neural model for retailer by it's ID and Secret key;
    Sends image to facenet to load model into state."""
    models = load_models(ctx, retailer_id, retailer_secret)

    facenet_model = models['facenet_model']
    if ctx.verbose:
        click.echo("Facenet model: %s" % facenet_model['codename'])

    facenet_provider = FacenetProvider(facenet_url)
    feature_extractor = partial(
        facenet_provider.extract_from_image_url,
        model_path=facenet_model['data_path'],
        index_path=facenet_model['index_path'],
        meta_path=facenet_model['meta_path'],
    )

    with Timer() as t:
        result = feature_extractor(image_url)
        click.echo(result)

    if ctx.verbose:
        click.echo("Elapsed: %s seconds" % t.elapsed_secs)


@api.command()
@click.option('-r', '--retailer-id', help='Retailer id')
@click.option('-s', '--retailer-secret', help='Retailer secret key')
@click.option('-u', '--facenet-url', help='Facenet service URL')
@click.argument('image_url')
@click.argument('bounding_boxes', type=click.File())
@pass_rebotics_context
def extract_feature_vectors_for_boxes(ctx, retailer_id, retailer_secret, facenet_url, image_url, bounding_boxes):
    """Fetches latest configuration of neural model for retailer by it's ID and Secret key;
    Sends keyframe image url and list of bounding boxes to facenet to load model into state."""
    models = load_models(ctx, retailer_id, retailer_secret)

    facenet_model = models['facenet_model']
    if ctx.verbose:
        click.echo("Facenet model: %s" % facenet_model['codename'])

    boxes = json.load(bounding_boxes)
    assert isinstance(boxes, list), "Need to supply list of bounding boxes"

    facenet_provider = FacenetProvider(facenet_url)
    feature_extractor = partial(
        facenet_provider.extract_from_keyframe,
        model_path=facenet_model['data_path'],
        index_path=facenet_model['index_path'],
        meta_path=facenet_model['meta_path'],
    )

    with Timer() as t:
        result = feature_extractor(keyframe_url=image_url, bboxes=boxes)
        click.echo(result)

    if ctx.verbose:
        click.echo("Elapsed: %s seconds" % t.elapsed_secs)


@api.command()
@click.argument('retailer', type=click.STRING)
@click.argument('url', type=click.STRING)
@pass_rebotics_context
def set_retailer_url(ctx, retailer, url):
    try:
        ctx.provider.update_host(retailer, url)
    except Exception as exc:
        raise click.ClickException(str(exc))
    else:
        click.echo('Set new host for retailer %s' % retailer)


def upload_packed(ctx, import_request, packed):
    destination = import_request['destination']
    files = {
        'file': ('features_backup.rcdb', packed)
    }
    response = requests.post(destination['url'], data=destination['fields'], files=files)
    if response.status_code < 300:
        ctx.provider.notify_classification_database_import_done(
            id=import_request['id']
        )
        click.echo('File was uploaded to destination. Classification data backup ID={}'.format(import_request['id']))
    else:
        raise click.ClickException("Failed to upload classification file. Destination status: {}".format(
            response.status_code)
        )


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@pass_rebotics_context
def pack_and_import_classification_db(ctx, retailer, model, images, labels, features):
    """
        Pack classification database to single .rcdb file and import it to the Rebotics Admin
db/
├── custom_folder
│   ├── image_400x400_copy.png
│   └── image_400x400.png
├── features.txt
└── labels.txt
    """
    packer = ClassificationDatabasePacker(destination=None)
    if ctx.verbose:
        click.echo("Packing from provided values: \n"
                   "labels: {labels} \n"
                   "features: {features} \n"
                   "images: {images}".format(labels=labels, features=features, images=images))
    try:
        packed = packer.pack(labels, features, images)
    except ClassificationDatabaseException as exc:
        raise click.ClickException(str(exc))
    import_request = ctx.provider.create_classification_database_import(
        retailer=retailer, model=model, extension=packer.extension
    )
    if ctx.verbose:
        click.echo("Import request: {}".format(import_request))
    upload_packed(ctx, import_request, packed)


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.argument('filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@pass_rebotics_context
def import_classification_db(ctx, retailer, model, filepath):
    """
    Import rcdb file to Rebotics Admin
    """
    extension = os.path.split(filepath)[-1].split('.')[-1]
    import_request = ctx.provider.create_classification_database_import(
        retailer=retailer, model=model, extension=extension
    )
    with open(filepath, 'rb') as packed:
        upload_packed(ctx, import_request, packed)


@api.command()
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-t', '--target', type=click.Path(exists=True, file_okay=True, dir_okay=True), default='.')
@pass_rebotics_context
def pack_classification_db(ctx, images, labels, features, target):
    """
        Pack classification database to single .rcdb file
db/
├── custom_folder
│   ├── image_400x400_copy.png
│   └── image_400x400.png
├── features.txt
└── labels.txt
    """
    target = pathlib.Path(target)
    if target.is_dir():
        target = target / "{}.{}".format(
            datetime.datetime.now().strftime('%Y-%m-%dZ%H:%M'),
            ClassificationDatabasePacker.extension
        )
    packer = ClassificationDatabasePacker(destination=target)
    if ctx.verbose:
        click.echo("Packing from provided values: \n"
                   "labels: {labels} \n"
                   "features: {features} \n"
                   "images: {images}".format(labels=labels, features=features, images=images))
    try:
        packed = packer.pack(labels, features, images)
    except ClassificationDatabaseException as exc:
        raise click.ClickException(str(exc))
    click.echo('Written to {}'.format(packed))


api.add_command(shell, 'shell')
api.add_command(roles, 'roles')
api.add_command(configure, 'configure')

from rebotics_sdk.providers.utils import is_valid_url
from .base import ReboticsBaseProvider, remote_service, ProviderHTTPClientException


class AdminProvider(ReboticsBaseProvider):
    @remote_service('/admin/', json=False)
    def admin_ping(self, **kwargs):
        return self.session.get()

    @remote_service('/nn_models/tf/models/')
    def get_retailer_tf_models(self):
        return self.session.get()

    @remote_service('/retailers/host/')
    def get_retailer(self, retailer_codename):
        response = self.session.post(data={
            'company': retailer_codename
        })
        return response

    def get_retailer_host(self, retailer_codename):
        return self.get_retailer(retailer_codename)['host']

    @remote_service('/retailers/')
    def get_retailer_list(self):
        return self.session.get()

    @remote_service('/retailers/host/{codename}/')
    def update_host(self, codename, host):
        if not is_valid_url(host):
            raise ProviderHTTPClientException('%s is not a valid url' % host, host=host)
        return self.session.patch(codename=codename, data={
            'host': host
        })

    def set_retailer_identifier(self, retailer_id, retailer_secret_key):
        self.headers['x-retailer-id'] = retailer_id
        self.headers['x-retailer-secret-key'] = retailer_secret_key

    @remote_service('/api/token-auth/')
    def token_auth(self, username, password):
        json_data = self.session.post(data={
            'username': username,
            'password': password
        })
        self.set_token(json_data['token'])
        return json_data

    def get_configurations(self, codename=None):
        """
        Should call this with codename and provided token authentication,
        or
        with provided retailer identifier
        :param codename:
        :return:
        """
        if codename is not None and not self.is_retailer_identifier_used():
            return self.get_configurations_by_codename(codename)
        elif self.is_retailer_identifier_used():
            return self.get_configurations_by_retailer_authentication()
        else:
            raise ProviderHTTPClientException('You did not use any of the authentication methods to get configurations')

    @remote_service('/retailers/host/{codename}/configurations/')
    def get_configurations_by_codename(self, codename):
        return self.session.get(codename=codename)

    @remote_service('/retailers/configurations/')
    def get_configurations_by_retailer_authentication(self):
        return self.session.get()

    @remote_service('/api/classification_data/import/')
    def create_classification_database_import(self, retailer, model, extension='zip'):
        allowed_extensions = ['rcdb', 'zip']
        if extension not in allowed_extensions:
            raise ValueError("Extension should be on of {} not {}".format(
                allowed_extensions, extension
            ))
        return self.session.post(json={
            'retailer': retailer,
            'model': model,
            'extension': extension
        })

    @remote_service('/api/classification_data/task/export_feature_database/{id}/complete/')
    def notify_classification_database_import_done(self, id):
        return self.session.post(
            id=id,
        )

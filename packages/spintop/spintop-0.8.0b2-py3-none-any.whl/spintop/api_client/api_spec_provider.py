from .base import SpintopAPIClientModule, SpintopAPIAuthProvider

class NoAuthModule(object):
    def get_auth_headers(self):
        return {}

    def refresh_credentials(self):
        raise NotImplementedError('Cannot refresh credentials without an auth module.')

class SpintopAPISpecProvider(SpintopAPIClientModule):
    """A no auth client module to bootstrap the retrieval of api spec before the auth_provider exists,
    since its parameters are returned by the api spec itself."""
    def __init__(self, api_url):
        super().__init__(api_url, auth=NoAuthModule())
        self._api_spec = None
        self._auth_provider = None

    def get_auth_provider(self):
        if self._auth_provider is None:
            api_spec = self.api_spec
            auth_spec = api_spec['auth']
            if auth_spec.get('enabled', False):
                spec = dict(
                    domain=auth_spec.get('domain'),
                    client_id=auth_spec.get('machine_client_id'),
                    audience=auth_spec.get('audience'),
                    jwks_url=auth_spec.get('jwks_url'),
                    user_info_url=auth_spec.get('user_info_url'),
                    payload_claims=auth_spec.get('payload_claims', {}),
                )
                try:
                    self._auth_provider = SpintopAPIAuthProvider(**spec)
                except ValueError:
                    raise ValueError(f'API Spec is invalid: unable to create auth0 provider. {spec}')
        return self._auth_provider
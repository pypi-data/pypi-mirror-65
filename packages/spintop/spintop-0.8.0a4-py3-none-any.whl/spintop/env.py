import os
from dataclasses import dataclass

from .api_client import SpintopAPIClientModule, SpintopAPISpecAuthBootstrap, create_backend_auth_bootstrap_factory
from .auth import FilePathCredentialsStore
from .persistence.mongo import MongoPersistenceFacade
from .persistence.postgresql import PostgreSQLPersistenceFacade, engine_from_uri, SQLOperations

from .spintop import SpintopFactory
from .api_client.tests_facade import SpintopAPIPersistenceFacade

from .storage import SITE_DATA_DIR
from .messages import SpintopMessagePublisher

def alias_for(env_name):
    return property(
        fget= lambda env: env[env_name],
        fset= lambda env, value: env.__setitem__(env_name, value)
    )

NO_VALUE = object()

def Spintop(api_url=None, verbose=False, init_env={}):
    env = SpintopEnv(init_env, verbose=verbose, api_url=api_url)
    return env.spintop_factory()

class SpintopEnv(object):
    # Credentials file is used to store access and refresh tokens.
    SPINTOP_CREDENTIALS_FILE: str = os.path.join(SITE_DATA_DIR, '.spintop-credentials.yml')

    # Client id and secret is used for machine to machine auth flow.
    SPINTOP_M2M_CLIENT_ID: str = None
    SPINTOP_M2M_SECRET_KEY: str = None

    SPINTOP_PERSISTENCE_TYPE: str = 'api'

    # used if SPINTOP_PERSISTENCE_TYPE is 'api'
    SPINTOP_API_URI: str = 'https://cloud.spintop.io'

    # used if SPINTOP_PERSISTENCE_TYPE is 'mongo'
    SPINTOP_MONGO_URI: str 

    # used if SPINTOP_PERSISTENCE_TYPE is 'postgres'
    SPINTOP_POSTGRES_URI: str

    # used by all persistence types
    SPINTOP_DATABASE_NAME: str = None

    # other
    SPINTOP_VERBOSE: bool = False

    # Aliases for python-friendly attributes
    api_url = alias_for('SPINTOP_API_URI') # URL
    api_uri = alias_for('SPINTOP_API_URI') # URI

    credentials_filepath = alias_for('SPINTOP_CREDENTIALS_FILE')
    selected_org_id = alias_for('SPINTOP_DATABASE_NAME')
    verbose = alias_for('SPINTOP_VERBOSE')
    database_name = alias_for('SPINTOP_DATABASE_NAME')

    def __init__(self, _init_values=None, verbose=False, api_url=None, ignore_invalid_init_value=False):
        if _init_values is None:
            _init_values = {}

        # Replace default values by possible a real env value.
        for key in self.ENV_NAMES:
            default_value = NO_VALUE
            if hasattr(self, key):
                default_value = self[key]

            setattr(self, key, os.environ.get(key, default_value))

        for key, value in _init_values.items():
            try:
                self[key] = value # Will validate if key is part of the support env variables.
            except KeyError:
                if not ignore_invalid_init_value:
                    raise

        if api_url:
            # for some reason, the requests module adds 1 second to every request made using localhost
            # replacing it with 127.0.0.1 removes this strange issue.
            self.api_url = api_url.replace('//localhost', '//127.0.0.1') 
        
        self.verbose = verbose

    @property
    def ENV_NAMES(self):
        return list(self.__annotations__.keys())

    def __getattr__(self, key):
        """When an attribute does not exist, attempt to retrieve it from env."""
        try:
            self._must_be_an_env_key(key)
            return os.environ[key]
        except KeyError as e:
            # Raise as attribute error for __getattr__ 
            raise AttributeError(str(e))

    def __getitem__(self, key):
        self._must_be_an_env_key(key)
        value = getattr(self, key)
        if value is NO_VALUE:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key, value):
        self._must_be_an_env_key(key)
        setattr(self, key, value)

    def get(self, key, default_value=None):
        try:
            return self[key]
        except:
            return default_value

    def _must_be_an_env_key(self, key):
        if key not in self.ENV_NAMES:
            raise KeyError(f'{key!r} is not a SpintopEnv variable.')

    def freeze(self, specific_keys=None):
        if not specific_keys: specific_keys = self.ENV_NAMES
        return {key: self.get(key) for key in specific_keys}

    def freeze_database_access_only(self):
        keys = [
            'SPINTOP_PERSISTENCE_TYPE',
            self._facade_uri_env_name(self.SPINTOP_PERSISTENCE_TYPE),
            'SPINTOP_DATABASE_NAME'
        ]
        return self.freeze(keys)

    def copy(self, **new_env_values):
        new_env = SpintopEnv(self.freeze())
        for key, value in new_env_values.items():
            new_env[key] = value
        return new_env

    def new_database_context(self, database_name):
        env = self.copy()
        env.database_name = database_name
        return env

    def get_facade_uri(self, facade_type=None):
        return self[self._facade_uri_env_name(facade_type)]

    def transform_facade_uri(self, transform, facade_type=None):
        key_name = self._facade_uri_env_name(facade_type)
        self[key_name] = transform(self[key_name])

    def _facade_uri_env_name(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        return f'SPINTOP_{facade_type.upper()}_URI'

    def get_persistence_cls(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        facade_cls_by_type = {
            'mongo': MongoPersistenceFacade,
            'postgres': PostgreSQLPersistenceFacade,
            'api': SpintopAPIPersistenceFacade,
        }

        if facade_type not in facade_cls_by_type:
            raise ValueError(f'Unknown facade type SPINTOP_PERSISTENCE_TYPE={facade_type!r}. Available: {list(facade_cls_by_type.keys())!r}')
        
        return facade_cls_by_type[facade_type]

    def get_persistence_params(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        return dict(
            uri=self.get_facade_uri(facade_type),
            database_name=self.database_name # shared by all
        )

    def persistence_facade_factory(self, message_publisher:SpintopMessagePublisher =None, facade_type=None):
        facade_cls = self.get_persistence_cls(facade_type)
        persistence_params = self.get_persistence_params(facade_type)
        facade = facade_cls.from_env(
            env=self,
            **persistence_params
        )
        if message_publisher is not None:
            facade.messages = message_publisher
        return facade
    
    def postgres_sql_ops_factory(self):
        uri = self.get_facade_uri('postgres')
        engine = engine_from_uri(uri, database_name=self.database_name)
        return SQLOperations(engine)

    def postgres_singer_stream_factory(self, **kwargs):
        from .persistence.singer_postgresql import PostgreSQLSingerTarget
        uri = self.get_facade_uri('postgres')
        return PostgreSQLSingerTarget(uri, database_name=self.database_name, **kwargs)

    def spintop_factory(self, **kwargs):
        auth_bootstrap_factory = SpintopAPISpecAuthBootstrap
        if self.SPINTOP_M2M_CLIENT_ID:
            # Use machine to machine auth bootstrap.
            auth_bootstrap_factory = create_backend_auth_bootstrap_factory(self.SPINTOP_M2M_CLIENT_ID, self.SPINTOP_M2M_SECRET_KEY)

        return SpintopFactory(
            api_url=self.api_uri,
            credentials_filepath=self.credentials_filepath,
            selected_org_id=self.selected_org_id,
            auth_bootstrap_factory=auth_bootstrap_factory,
            **kwargs
        )
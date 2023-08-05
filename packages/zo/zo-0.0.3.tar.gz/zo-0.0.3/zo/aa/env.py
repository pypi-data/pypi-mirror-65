import pathlib
import re
import time
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from typing import List, Union, Any
# from ipaddress import IPv4Address

from zo.pydantic import BaseModelValidation, constr, conint
from zo.log import log_level


class _Env(BaseModelValidation):
    validate_assignment = True
    title: constr(min_length=1, max_length=256) = ''
    version: constr(min_length=1, max_length=128) = ''
    debug: bool = False
    api_prefix: str = ''
    app_host: constr(regex=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$') = '127.0.0.1'
    app_port: conint(ge=1, le=65536) = 8000
    db_host: Union[constr(regex=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'), constr(regex=r'(d|ssdb)')] = '127.0.0.1'
    db_port: conint(ge=1, le=65536) = 8000
    token_secret_key: Any = ''
    token_user_expire: conint(ge=1) = 1
    allowed_hosts: List[str] = []

    run_app: constr(regex=r'^(run|main):app$') = 'run:app'
    run_reload: bool = False
    run_workers: int = 1
    run_log_level: constr(regex=r'^(critical|error|warning|info|debug|trace)$') = 'info'
    run_access_log: bool = False

    docs_url: Union[constr(regex=r'^/\w+'), None] = None
    redoc_url: Union[constr(regex=r'^/\w+'), None] = None


def get_env(path='.env') -> _Env:
    path = pathlib.Path(path)
    assert path.exists(), '.env file not exist'
    config = Config(path)
    env = _Env()

    env.debug = config('debug', cast=bool, default=False)

    if env.debug:
        env.version = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
        co = re.sub('VERSION = .*', f'VERSION = {env.version}', path.read_text())
        path.write_text(co)
    else:
        env.version = config('version')

    env.title = config('title')
    env.api_prefix = config('api_prefix', default='')
    env.app_host = config('app_host')
    env.app_port = config('app_port', cast=int)
    env.db_host = config('db_host')
    env.db_port = config('db_port', cast=int)
    env.token_secret_key = config('token_secret_key', cast=Secret)
    env.token_user_expire = eval(config('token_user_expire'))
    env.allowed_hosts = list(config('allowed_hosts', cast=CommaSeparatedStrings, default=''))

    env.run_app = config('run_app')
    env.run_reload = config('run_reload')
    env.run_workers = config('run_workers')
    env.run_log_level = config('run_log_level')
    env.run_access_log = config('run_access_log')
    env.docs_url = config('docs_url', default=None) or None
    env.redoc_url = config('redoc_url', default=None) or None
    return env

import hashlib
import os
import socket
from typing import Any
from zo.pydantic import BaseModel
from zo.log import log


def calc_hash(v, hash_factory=hashlib.sha3_256):
    h = hash_factory()
    # v = v.encode() if isinstance(v, str) else v
    v = v if isinstance(v, (bytes, bytearray)) else str(v).encode()
    assert isinstance(v, (bytes, bytearray)), f'calc_hash type error = {type(v)}'
    h.update(v)
    return h.hexdigest()


def calc_file_hash(path, hash_factory=hashlib.sha3_256, chunk_num_blocks=128):
    h = hash_factory()
    assert os.path.exists(path), f'File not exists? {[path]}'
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_num_blocks * h.block_size), b''):
            h.update(chunk)
    return h.hexdigest()


class HostInfo(BaseModel):
    hostname: str = ''
    ip: str = '-'

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.get_hostname()
        self.get_ip()

    def get_hostname(self):
        try:
            self.hostname = socket.gethostname()
        except Exception as e:
            log.error(f'get host name  e={e}')

    def get_ip(self):
        for conn_ip in ['223.5.5.5', '1.2.4.8', '1.1.1.1']:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect((conn_ip, 80))
                self.ip = s.getsockname()[0]
                break
            except Exception as e:
                log.error(f'conn_ip={conn_ip} e={e}')
            finally:
                s.close()

    def show(self):
        print(self.__dict__)


def to_str(v: Any, split_co='_'):
    if isinstance(v, list):
        return split_co.join([str(_) for _ in v])
    return str(v)

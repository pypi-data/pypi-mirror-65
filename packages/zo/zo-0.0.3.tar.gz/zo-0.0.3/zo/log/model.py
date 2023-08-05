from pydantic import BaseModel
from enum import Enum


class LogLevelEnum(str, Enum):
    critical = 'critical'
    error = 'error'
    warning = 'warning'
    info = 'info'
    debug = 'debug'
    trace = 'trace'


class LogLevel(BaseModel):
    critical = 'critical'
    error = 'error'
    warning = 'warning'
    info = 'info'
    debug = 'debug'
    trace = 'trace'

#
# log_level = LogLevel()
# log.info('init log_level')

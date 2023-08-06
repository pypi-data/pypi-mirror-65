from turboconfig.rwlock import ReadWriteLock

from .client import TCClient, TCConfig
from .identity import TurboConfigIdentity
from .util import tc_logger

"""Settings."""
start_wait = 5

__client = None
__config = TCConfig()
__lock = ReadWriteLock()


def _set_config(config):
    global __config
    global __client
    global __lock
    try:
        __lock.lock()
        if __client:
            tc_logger.info("Reinitializing TurboConfig Client with new config")
            new_client = TCClient(config=config, start_wait=start_wait)
            old_client = __client
            __client = new_client
            old_client.close()
    finally:
        __config = config
        __lock.unlock()


def _set_sdk_key(sdk_key):
    global __config
    global __client
    global __lock
    sdk_key_changed = False

    try:
        __lock.rlock()
        if sdk_key == __config.sdk_key:
            tc_logger.info(
                "New sdk_key is the same as the existing one. doing nothing."
            )
        else:
            sdk_key_changed = True
    finally:
        __lock.runlock()

    if sdk_key_changed:
        try:
            __lock.lock()
            __config = __config.copy_with_new_sdk_key(new_sdk_key=sdk_key)
            if __client:
                tc_logger.info("Reinitializing TurboConfig Client with new sdk key")
                new_client = TCClient(config=__config, start_wait=start_wait)
                old_client = __client
                __client = new_client
                old_client.close()
        finally:
            __lock.unlock()


def initialize(sdk_key_or_config):
    if isinstance(sdk_key_or_config, TCConfig):
        _set_config(sdk_key_or_config)
    elif isinstance(sdk_key_or_config, str):
        _set_sdk_key(sdk_key_or_config)
    else:
        raise Exception("Invalid SDK key or config found")
    return get_instance()


def get_instance():
    global __config
    global __client
    global __lock

    try:
        __lock.rlock()
        if __client:
            return __client
    finally:
        __lock.runlock()

    try:
        __lock.lock()
        if not __client:
            tc_logger.info("Initializing TruboConfig Client")
            __client = TCClient(config=__config, start_wait=start_wait)
        return __client
    finally:
        __lock.unlock()


__all__ = ["get_instance", "initialize", "TurboConfigIdentity"]

import threading

try:
    import queue
except Exception:
    import Queue as queue  # noqa: F401 , Python 3

from threading import Lock

from turboconfig.util import check_uwsgi, tc_logger, EvaluationResult
from turboconfig.config import TCConfig
from turboconfig.data_updater import PollingDataUpdater


class TCClient:
    """Client instances are thread-safe.
    """

    def __init__(self, sdk_key=None, config=None, start_wait=5):
        check_uwsgi()

        if config is not None and config.sdk_key is not None and sdk_key is not None:
            raise Exception(
                "TruboConfig client init received both sdk_key and config with sdk_key. "
                "Only one of either is expected"
            )

        if sdk_key is not None:
            self._config = TCConfig(sdk_key=sdk_key)
        else:
            self._config = config or TCConfig.default()
        self._config._validate()

        self._lock = Lock()
        self._storage = self._config.storage

        data_updater_ready = threading.Event()
        self._data_updater = PollingDataUpdater(
            self._config.poll_interval,
            self._config.requester,
            self._storage,
            data_updater_ready,
        )
        self._data_updater.start()

        if start_wait > 0:
            tc_logger.info(
                "Waiting up to "
                + str(start_wait)
                + " seconds for TurboConfig client to initialize..."
            )
            data_updater_ready.wait(start_wait)

        if self._data_updater.initialized() is True:
            tc_logger.info("Started TurboConfig Client: OK")
        else:
            tc_logger.warning(
                "Initialization timeout exceeded for TurboConfig Client or an error occurred. "
                "Flags may not yet be available."
            )

    def get_sdk_key(self):
        return self._config.sdk_key

    def close(self):
        tc_logger.info("Closing TurboConfig client..")
        self._data_updater.stop()

    # These magic methods allow a client object to be automatically cleaned up by the "with" scope operator
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def is_initialized(self):
        return self._data_updater.initialized()

    def get_boolean_config(self, key, identity, default):
        return self._get_value(key, identity, default).value

    def get_string_config(self, key, identity, default):
        return self._get_value(key, identity, default).value

    def get_integer_config(self, key, identity, default):
        return self._get_value(key, identity, default).value

    def _get_value(self, key, identity, default):
        if not self.is_initialized():
            tc_logger.warning(
                "Flag evaluation attempted before client has initialized! Storage unavailable - returning default: "
                + str(default)
                + " for flag key: "
                + key
            )
            return EvaluationResult(default, type(default).__name__, True)
        if identity is None:
            tc_logger.warning(
                "identity not specified - returing default: "
                + str(default)
                + " for flag key: "
                + key
            )
            return EvaluationResult(default, type(default).__name__, True)

        try:
            evaluation_result = self._evaluate_identity_flag(key, identity)
            if not evaluation_result:
                tc_logger.warning(
                    "Unable to fetch latest flag data. Serving stored value of flag {} for user {}".format(
                        key, identity.user_id
                    )
                )
                return EvaluationResult(default, type(default).__name__, True)
            else:
                return evaluation_result
        except Exception as e:
            tc_logger.warning(
                "Something went wrong while evaluating identity flag. Serving default value. Error: {}".format(
                    e
                )
            )
            return EvaluationResult(default, type(default).__name__, True)

    def _evaluate_identity_flag(self, key, identity):
        stored_identity = self._storage.get_identity(identity.user_id)
        if stored_identity and stored_identity == identity:
            flag_data = self._storage.get_flag_data_for_user(key, identity.user_id)
            result = EvaluationResult(flag_data.get("value"), flag_data.get("dataType"))
            return result
        else:
            updated_data = self._config.requester.update_flags_for_user(identity)
            if updated_data:
                flag_data = self._storage.update_data_for_user(
                    identity, updated_data, key
                )
                result = EvaluationResult(
                    flag_data.get("value"), flag_data.get("dataType")
                )
                return result
            else:
                return None


__all__ = ["TCClient", "TCConfig"]

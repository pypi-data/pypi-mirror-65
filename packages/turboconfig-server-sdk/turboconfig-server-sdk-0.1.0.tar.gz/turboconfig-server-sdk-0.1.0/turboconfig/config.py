from turboconfig.util import tc_logger
from turboconfig.storage import InMemoryStorage
from turboconfig.requester import DataRequester


class TCConfig:
    def __init__(
        self,
        sdk_key=None,
        base_uri="https://api.turboconfig.com",
        timeout=10,
        verify_ssl=True,
        poll_interval=30,
    ):
        self.__sdk_key = sdk_key
        self.__base_uri = base_uri.rstrip("\\")
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl
        self.__poll_interval = poll_interval
        self.__storage = InMemoryStorage()
        self.__requester = DataRequester(
            self.__base_uri, self.__sdk_key, self.__timeout, self.__verify_ssl,
        )

    @classmethod
    def default(cls):
        return cls()

    def copy_with_new_sdk_key(self, new_sdk_key):
        return TCConfig(
            sdk_key=new_sdk_key,
            base_uri=self.__base_uri,
            timeout=self.__timeout,
            verify_ssl=self.__verify_ssl,
            poll_interval=self.__poll_interval,
        )

    @property
    def sdk_key(self):
        return self.__sdk_key

    @property
    def base_uri(self):
        return self.__base_uri

    @property
    def timeout(self):
        return self.__timeout

    @property
    def verify_ssl(self):
        return self.__verify_ssl

    @property
    def poll_interval(self):
        return self.__poll_interval

    @property
    def storage(self):
        return self.__storage

    @property
    def requester(self):
        return self.__requester

    def _validate(self):
        if self.sdk_key is None or self.sdk_key == "":
            tc_logger.warning("Missing or blank sdk_key.")

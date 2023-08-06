import requests

from turboconfig.util import tc_logger


class DataRequester:
    def __init__(self, base_uri, token, timeout, verify_ssl):
        self.__base_uri = base_uri
        self.__token = token
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl

    def _get_flags_url(self):
        return self.__base_uri + "/api/v1/flags"

    def _get_headers(self, user_id):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.__token,
            "X-Temp-Token": "python-sdk-temp-token",
            "X-Identification": user_id,
        }

    def update_flags_for_user(self, identity):
        response = requests.post(
            url=self._get_flags_url(),
            json=identity.get_request_json(),
            headers=self._get_headers(identity.user_id),
            timeout=self.__timeout,
            verify=self.__verify_ssl,
        )
        if int(response.status_code / 100) == 2:
            try:
                return response.json().get("flags", [])
            except Exception as e:
                tc_logger.error(
                    "Something went wrong while parsing response for user {}. Error: {}".format(
                        identity.user_id, e
                    )
                )
                return None
        else:
            tc_logger.error(
                "Something went wrong while fetching flags data for user {}".format(
                    identity.user_id
                )
            )
            return None

    def fetch_flags_for_user(self, user_id):
        response = requests.get(
            url=self._get_flags_url(),
            headers=self._get_headers(user_id),
            timeout=self.__timeout,
            verify=self.__verify_ssl,
        )

        if int(response.status_code / 100) == 2:
            try:
                return response.json().get("flags", [])
            except Exception as e:
                tc_logger.error(
                    "Something went wrong while parsing response for user {}. Error: {}".format(
                        user_id, e
                    )
                )
                return None
        else:
            tc_logger.error(
                "Something went wrong while fetching flags data for user {}".format(
                    user_id
                )
            )
            return None

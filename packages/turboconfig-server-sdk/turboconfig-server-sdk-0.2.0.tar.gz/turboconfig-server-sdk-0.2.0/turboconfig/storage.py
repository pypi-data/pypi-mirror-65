from collections import defaultdict

from turboconfig.rwlock import ReadWriteLock
from turboconfig.util import tc_logger

"""
{
    "flags": {
        "identification" <user_id>: {
            "flag-1" <key>: {
                "dataType": string,
                "value": int/string/boolean,
            }
        }
    },
    "identities": {
        "identification": TurboConfigIdentity()
    }
}
"""


class InMemoryStorage:
    def __init__(self):
        self._lock = ReadWriteLock()
        self._store = defaultdict(dict)

    def get_flag_data_for_user(self, key, user_id):
        try:
            self._lock.rlock()
            flag_data = self._store["flags"].get(user_id, {}).get(key)
            if not flag_data:
                tc_logger.debug(
                    "Attempted to get missing key %s in flags for user '%s' - returning None",
                    key,
                    user_id,
                )
                return None
            return flag_data
        finally:
            self._lock.runlock()

    def get_identity(self, user_id):
        try:
            self._lock.rlock()
            identity = self._store["identities"].get(user_id)
            if not identity:
                tc_logger.debug(
                    "Attempted to get missing identity %s in identities - returning None",
                    user_id,
                )
                return None
            return identity
        finally:
            self._lock.runlock()

    def update_data_for_user(self, identity, updated_data, return_flag_key=None):
        try:
            self._lock.rlock()
            self._store["identities"][identity.user_id] = identity
            tc_logger.debug("Updated identity of user {}".format(identity.user_id))

            requested_flag_data = {}
            final_data = {}
            for flag_data in updated_data:
                data = {
                    "value": flag_data["value"],
                    "dataType": flag_data["dataType"],
                }
                final_data[flag_data["key"]] = data
                if return_flag_key == flag_data["key"]:
                    requested_flag_data = data
            self._store["flags"][identity.user_id] = final_data
            tc_logger.debug("Updated flags of user {}".format(identity.user_id))
            return requested_flag_data

        finally:
            self._lock.runlock()

    def get_all_user_ids(self):
        try:
            self._lock.rlock()
            return self._store["identities"].keys()
        finally:
            self._lock.runlock()

    def refresh_user_flags(self, user_id, flags_data):
        try:
            self._lock.rlock()
            final_data = {}
            for flag_data in flags_data:
                final_data[flag_data["key"]] = {
                    "value": flag_data["value"],
                    "dataType": flag_data["dataType"],
                }
            self._store["flags"][user_id] = final_data
            tc_logger.debug("Updated flags of user {}".format(user_id))

        finally:
            self._lock.runlock()

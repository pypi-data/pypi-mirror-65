import time

from threading import Thread

from turboconfig.util import tc_logger


class PollingDataUpdater(Thread):
    def __init__(self, poll_interval, requester, storage, ready):
        Thread.__init__(self)
        self.daemon = True
        self._poll_interval = poll_interval
        self._requester = requester
        self._storage = storage
        self._running = False
        self._ready = ready

    def run(self):
        if not self._running:
            tc_logger.info(
                "Starting PollingDataUpdater with request interval: "
                + str(self._poll_interval)
            )
            self._running = True
            while self._running:
                start_time = time.time()
                try:
                    user_ids = self._storage.get_all_user_ids()
                    for user_id in user_ids:
                        updated_flags = self._requester.fetch_flags_for_user(user_id)
                        if updated_flags:
                            self._storage.refresh_user_flags(user_id, updated_flags)

                    if not self._ready.is_set() is True:
                        tc_logger.info("PollingUpdateProcessor initialized ok")
                        self._ready.set()
                except Exception as e:
                    tc_logger.exception(
                        "Error: Exception encountered when updating flags. %s" % e
                    )
                elapsed = time.time() - start_time
                if elapsed < self._poll_interval:
                    time.sleep(self._poll_interval - elapsed)

    def initialized(self):
        return self._running and self._ready.is_set() is True

    def stop(self):
        tc_logger.info("Stopping PollingDataUpdater")
        self._running = False

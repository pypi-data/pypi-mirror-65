import sys
import logging

_PY_ = None

if sys.version_info[0] < 3:
    _PY_ = 2
else:
    _PY_ = 3


tc_logger = logging.getLogger(sys.modules[__name__].__name__)


def check_uwsgi():
    if "uwsgi" in sys.modules:
        import uwsgi

        if uwsgi.opt.get("enable-threads"):
            return
        if uwsgi.opt.get("threads") is not None and int(uwsgi.opt.get("threads")) > 1:
            return
        tc_logger.error(
            "The TurboConfig client requires the 'enable-threads' or 'threads' option be passed to uWSGI."
        )


class EvaluationResult:
    def __init__(self, value, data_type, default=False):
        self.__value = value
        self.__data_type = data_type
        self.__default = default

    @property
    def value(self):
        return self.__value

    @property
    def data_type(self):
        return self.__data_type

    def is_default_value(self):
        return self.__default

import logging
from functools import wraps
from log_labeler.utils import Utils
from django.conf import settings
from log_labeler import ALLOWED_DYNAMIC_DEBUG_LEVEL_VALUES, LOG_LABEL_EXCLUDE_LOG_LIST, LOGGING


def __update_log_level(logger_names, exclude_log_list, level):
    logger_names_to_set = Utils.array_difference(logger_names, exclude_log_list)
    for logger_name in logger_names_to_set:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)


def process_dynamic_log_level(request):
    if "loggers" in getattr(settings, LOGGING):
        logger_names = list(getattr(settings, LOGGING)["loggers"].keys())
        exclude_log_list = getattr(settings, LOG_LABEL_EXCLUDE_LOG_LIST, list())
        __update_log_level(logger_names, exclude_log_list, settings.DEFAULT_LOG_LEVEL)

        if settings.NIM_DJANGO_REQUEST_LOG_LEVEL_NAME in request.META:
            level_value = request.META.get(settings.NIM_DJANGO_REQUEST_LOG_LEVEL_NAME).upper()
            logger_message = logging.getLogger(__name__)
            nim_headers = Utils.get_nim_headers(request)
            if level_value in ALLOWED_DYNAMIC_DEBUG_LEVEL_VALUES:
                __update_log_level(logger_names, exclude_log_list, level_value)
                logger_message.info("The log level has been overwritten by the header '{}' to the value {}".format(
                    settings.NIM_DJANGO_REQUEST_LOG_LEVEL_NAME, level_value), extra=nim_headers)
            else:
                logger_message.info("The header '{}' has an invalid value, the values allowed are {}".format(
                    settings.NIM_DJANGO_REQUEST_LOG_LEVEL_NAME, ", ".join(ALLOWED_DYNAMIC_DEBUG_LEVEL_VALUES)),
                    extra=nim_headers)


def dynamic_log_level():
    def _dynamic_log_level(func):
        def dynamic_log_level_logic(*argv, **kwargs):
            if "request" in kwargs:
                request = kwargs["request"]
                process_dynamic_log_level(request)
            elif len(argv) > 1:  # The first argument is the Django Rest HTTP request
                request = argv[1]
                process_dynamic_log_level(request)
            return func(*argv, **kwargs)

        return wraps(func)(dynamic_log_level_logic)

    return _dynamic_log_level

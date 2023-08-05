import logging
import traceback
from django.core.exceptions import ImproperlyConfigured

from .utils import Utils
from django.conf import settings
from log_labeler import local, LOG_LABEL_REQUEST_SETTING, DEFAULT_HEADER_VALUE, \
        MAX_REQUEST_RESPONSE_SIZE, DEFAULT_LOG_LEVEL, \
        NIM_DJANGO_REQUEST_LOG_LEVEL_NAME, LOGGING

logger = logging.getLogger(__name__)


class HeaderToLabelMiddleware(object):
    """
    Provides full logging of requests and responses
    """
    _initial_http_body = ""
    _request_start_time = None
    _TRUNCATE_INDICATOR = "---[TRUNCATED]---"
    _OBFUSCATE_INDICATOR = "---[HIDDEN]---"
    _REQUEST = "Request"
    _RESPONSE = "Response"
    _ERROR = "Error"

    def __init__(self, get_response=None):
        if not hasattr(settings, LOG_LABEL_REQUEST_SETTING):
            raise ImproperlyConfigured(f"Please set {LOG_LABEL_REQUEST_SETTING}, it is the dictionary of header names and values that need to be appended to the log")

        if not hasattr(settings, MAX_REQUEST_RESPONSE_SIZE):
            raise ImproperlyConfigured(f"Please set {MAX_REQUEST_RESPONSE_SIZE}, it is the value of the max length of the response")

        if not hasattr(settings, DEFAULT_LOG_LEVEL):
            raise ImproperlyConfigured(f"Please set {DEFAULT_LOG_LEVEL}, it is the value of the log level")

        if not hasattr(settings, NIM_DJANGO_REQUEST_LOG_LEVEL_NAME):
            raise ImproperlyConfigured(f"Please set {NIM_DJANGO_REQUEST_LOG_LEVEL_NAME}, it is the value of the header name containing the correlation id")

        self.get_response = get_response

    def process_request(self, request):
        self._initial_http_body = Utils.obfuscate_body(Utils.adjust_string_length(request.body, getattr(settings, MAX_REQUEST_RESPONSE_SIZE)))
        self._request_start_time = Utils.get_time_in_milliseconds()
        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())

        headers = Utils.obfuscate_headers(Utils.get_all_headers(request))

        log_entry_info = dict(
            type=self._REQUEST,
            request_start_time_ms=self._request_start_time,
            method=request.method,
            url=Utils.obfuscate_url(request.build_absolute_uri())
        )
        log_entry_info.update(headers)

        log_entry_debug = dict(
            type=self._REQUEST,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=Utils.get_time_in_milliseconds(),
            method=request.method,
            body=self._initial_http_body,
            url=Utils.obfuscate_url(request.build_absolute_uri())
        )
        log_entry_debug.update(headers)

        for label, header_name in log_label_request_settings.items():
            header_value = Utils.get_header_by_name(request, header_name, DEFAULT_HEADER_VALUE)
            setattr(local, label, header_value)
            setattr(request, label, header_value)
            log_entry_info[label] = header_value
            log_entry_debug[label] = header_value

        logger.debug('', extra=log_entry_debug)
        logger.info('', extra=log_entry_info)

    def process_response(self, request, response):
        headers = Utils.obfuscate_headers(Utils.get_all_headers(request))
        status_code = 500
        if hasattr(response, "status_code"):
            status_code = response.status_code

        if hasattr(response, "content"):
            content = response.content.decode("UTF-8")
        else:
            content = str(response)

        log_entry = dict(
            type=self._RESPONSE,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=Utils.get_time_in_milliseconds(),
            method=request.method,
            body=self._initial_http_body,
            status_code=status_code,
            response=Utils.obfuscate_response(Utils.adjust_string_length(content,
                                                settings.MAX_REQUEST_RESPONSE_SIZE) if status_code < 400 else Utils.obfuscate_response(content)),
            url=Utils.obfuscate_url(request.build_absolute_uri())
        )
        log_entry.update(headers)

        log_entry_info = dict(
            type=self._RESPONSE,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=Utils.get_time_in_milliseconds(),
            status_code=status_code,
            method=request.method,
            url=Utils.obfuscate_url(request.build_absolute_uri())
        )
        log_entry_info.update(log_entry_info)
        log_entry_info.update(headers)

        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())
        for label in log_label_request_settings:
            log_entry[label] = getattr(request, label)
            log_entry_info[label] = getattr(request, label)

        if status_code < 400:
            logger.debug(
                '', extra=log_entry
            )
        else:
            logger.error(
                '', extra=log_entry
            )

        logger.info(
            '', extra=log_entry_info
        )
        return response

    def process_exception(self, request, exception):
        headers = Utils.obfuscate_headers(Utils.get_all_headers(request))
        log_entry = dict(
            type=self._ERROR,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=Utils.get_time_in_milliseconds(),
            method=request.method,
            body=self._initial_http_body,
            status_code=500,
            exception=str(exception),
            url=Utils.obfuscate_url(request.build_absolute_uri()),
            stack_trace=traceback.format_exc()
        )
        log_entry.update(headers)

        log_entry_info = dict(
            type=self._ERROR,
            request_start_time_ms=self._request_start_time,
            request_end_time_ms=Utils.get_time_in_milliseconds(),
            status_code=500,
            method=request.method,
            url=Utils.obfuscate_url(request.build_absolute_uri())
        )
        log_entry_info.update(headers)

        log_label_request_settings = getattr(settings, LOG_LABEL_REQUEST_SETTING, dict())
        for label in log_label_request_settings:
            log_entry[label] = getattr(request, label)
            log_entry_info[label] = getattr(request, label)

        logger.error(
            '', extra=log_entry
        )
        logger.info(
            '', extra=log_entry_info
        )
        return exception

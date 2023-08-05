import re
import math
import time
import logging
from django.conf import settings
from log_labeler import LOG_LABEL_OBFUSCATE, HIDDEN_INDICATOR

logger = logging.getLogger(__name__)


class Obfuscation_Type:
    JSON = "JSON"
    XML = "XML"
    URL = "URL"


class Utils:
    @classmethod
    def array_difference(cls, array1, array2):
        return list(set(array1) - set(array2))

    @classmethod
    def array_intersection(cls, array1, array2):
        return list(set(array1) & set(array2))

    @classmethod
    def remove_new_lines(cls, data):
        return data.replace("\n", "").replace("\r", "")

    @classmethod
    def get_nim_headers(cls, request):
        NIM_HEADER_REG_EXP = r"^HTTP\_NIM\_"
        HTTP_REG_EXP = r"^HTTP\_"
        nim_headers = dict()
        for key, value in request.META.items():
            if re.match(NIM_HEADER_REG_EXP, key):
                transformed_key = re.sub(HTTP_REG_EXP, "", key).replace("_", "-")
                nim_headers[transformed_key.lower()] = value

        return nim_headers

    @classmethod
    def get_all_headers(cls, request):
        headers = dict()
        for key, value in request.META.items():
            headers[key.lower()] = value

        return headers

    @classmethod
    def get_header_by_name(cls, request, header_name, default_value):
        return request.META.get(header_name.upper(), default_value)

    @classmethod
    def adjust_string_length(cls, value, max_length):
        TRUNCATE_INDICATOR = "---[TRUNCATED]---"
        if isinstance(value, bytes):
            value = value.decode("UTF-8")
        output = value

        if max_length and max_length.upper() != "OFF":
            max_length = int(max_length)
            value = value
            length = len(value)
            if length > max_length:
                extra_chars = int(math.floor((length - max_length) / 2))
                adjust_even = 1 if length % 2 == 0 else 0
                middle = int(math.ceil(length / 2))
                output = "".join(
                    [value[:middle - extra_chars], TRUNCATE_INDICATOR, value[middle + extra_chars + adjust_even:]])
        return output

    @classmethod
    def get_time_in_milliseconds(cls):
        return int(round(time.time() * 1000))

    @classmethod
    def obfuscate_headers(cls, headers):
        _headers = headers.copy()
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "headers" in log_label_obfuscate:
            headers_to_obfuscate = cls.array_intersection(log_label_obfuscate["headers"], _headers)
            for header_name in headers_to_obfuscate:
                _headers[header_name] = HIDDEN_INDICATOR

        return _headers

    @classmethod
    def obfuscate(cls, data, start, end):
        return "{}{}{}".format(data[:start], HIDDEN_INDICATOR, data[end:])

    @classmethod
    def starts_with(cls, data, start_string):
        return data.lower().startswith(start_string.lower())

    @classmethod
    def find_next_json_closing_quote(cls, data):
        try:
            quote_index = data.index("\"")
            if quote_index == 0:
                return 0

            if data[quote_index - 1] == "\\":
                return quote_index + cls.find_next_json_closing_quote(data[quote_index + 1:])

            return quote_index
        except ValueError:
            return 0

    @classmethod
    def obfuscate_by_type(cls, data, field_name, obfuscation_type):
        if obfuscation_type == Obfuscation_Type.XML:
            if field_name.lower() in data.lower():
                start_indicator = "(?i)(<\\s*(\\w+\\:)?\\s*{}(\\s*[\\s\\S]*?>)?)".format(re.escape(field_name))
                end_indicator = "(?i)(<\\/\\s*(\\w+\\:)?\\s*{}>)".format(re.escape(field_name))

                start_matches = re.search(start_indicator, data)
                end_matches = re.search(end_indicator, data)
                if start_matches and end_matches:
                    start_index = data.index(start_matches.groups()[0]) + len(start_matches.groups()[0])
                    end_index = data.index(end_matches.groups()[0])

                    return cls.obfuscate(data, start_index, end_index)

        if obfuscation_type == Obfuscation_Type.JSON:
            if field_name.lower() in data.lower():
                indicator = '(?i)((\\"{}\\"\\s*:\\s*\\")((\\\\"|[^\\\\\"])*)\\")'.format(re.escape(field_name))
                matches = re.search(indicator, data)

                if matches and cls.starts_with(matches.groups()[0], "\"{}\"".format(field_name)):
                    start_index = data.index(matches.groups()[0]) + len(matches.groups()[1])
                    end_index = len(data[:start_index]) + cls.find_next_json_closing_quote(data[start_index:])

                    return cls.obfuscate(data, start_index, end_index)

        if obfuscation_type == Obfuscation_Type.URL:
            if field_name.lower() in data.lower():
                indicator = "(?i)((((\\?|\\&){}=)((\\\"|[^\\&])*)))".format(re.escape(field_name))
                matches = re.search(indicator, data)

                if matches and cls.starts_with(matches.groups()[0].lstrip("?").lstrip("&"), field_name):
                    stripped_match = matches.groups()[0].lstrip("?").lstrip("&")
                    key_matches = matches.groups()[2].lstrip("?").lstrip("&")
                    start_index = data.index(stripped_match) + len(key_matches)
                    try:
                        end_index = len(data[:start_index]) + data[start_index:].index("&")
                    except ValueError:
                        end_index = len(data[:start_index]) + len(data[start_index:])

                    return cls.obfuscate(data, start_index, end_index)

        return data

    @classmethod
    def obfuscate_body(cls, body):
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "body" in log_label_obfuscate:
            body = cls.remove_new_lines(body)
            for obfuscation in log_label_obfuscate["body"]:
                field_name = obfuscation[0]
                obfuscation_type = obfuscation[1]
                body = cls.obfuscate_by_type(body, field_name, obfuscation_type)

        return body

    @classmethod
    def obfuscate_response(cls, response):
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "response" in log_label_obfuscate:
            response = cls.remove_new_lines(response)
            for obfuscation in log_label_obfuscate["response"]:
                field_name = obfuscation[0]
                obfuscation_type = obfuscation[1]
                response = cls.obfuscate_by_type(response, field_name, obfuscation_type)

        return response

    @classmethod
    def obfuscate_url(cls, url):
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "url" in log_label_obfuscate:
            for obfuscation in log_label_obfuscate["url"]:
                field_name = obfuscation[0]
                obfuscation_type = obfuscation[1]
                url = cls.obfuscate_by_type(url, field_name, obfuscation_type)

        return url

django-log-labeler
=====================

**Django middleware and log filter to attach values from the headers to every log message generated as part of a request.**

**Author:** Hermann Stephane Ntsamo

Example
-------

```
DEBUG [340d34bb4bb91ed4f45c414808a03a65] myproject.apps.myapp.views: Some log message
DEBUG [340d34bb4bb91ed4f45c414808a03a65] myproject.apps.myapp.forms: Some other log message
```


Installation and usage
----------------------

First, install the package: `pip install django-log-labeler`

Add the middleware to your `MIDDLEWARE_CLASSES` setting.

```python
MIDDLEWARE_CLASSES = (
    'log_labeler.middleware.HeaderToLabelMiddleware',
    # ... other middleware goes here
)
```

Add the `log_labeler.filters.HeaderToLabelFilter` to your `LOGGING` setting. Update your `formatters` to include the header names you want appearing in the log message. Add a handler to output the messages (eg to the console), and finally attach the handler to your application's logger.

An example `LOGGING` setting is below:

```python
DEFAULT_LOG_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

LOG_LABEL_REQUEST_SETTING = {
    "correlation_id": "HTTP_NIM_CORRELATION_ID",
    "session_id": "HTTP_NIM_SESSION_ID",
    "app_id": "HTTP_NIM_APP_ID",
    "nim_user": "HTTP_NIM_USER",
    "app_version": "HTTP_NIM_APP_VERSION",
}

LOG_LABEL_EXCLUDE_LOG_LIST = [
    "",
    "django"
]

LOG_LABEL_OBFUSCATE = {
    "headers": ["Authorization"],
    "body": {
        "(?i)(\\<(\\w+\\:)?password.*\\>).+(\\<\\/(\\w+\\:)?password.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(\\<(\\w+\\:)?session.*\\>).+(\\<\\/(\\w+\\:)?session.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(\\<(\\w+\\:)?token.*\\>).+(\\<\\/(\\w+\\:)?token.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(.*\\??password([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??token([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??session([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.+\\\".*session.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
        "(?i)(.+\\\".*token.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
        "(?i)(.+\\\".*password.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
    },
    "response": {
        "(?i)(\\<(\\w+\\:)?password.*\\>).+(\\<\\/(\\w+\\:)?password.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(\\<(\\w+\\:)?session.*\\>).+(\\<\\/(\\w+\\:)?session.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(\\<(\\w+\\:)?token.*\\>).+(\\<\\/(\\w+\\:)?token.*\\>)": r"\1[--HIDDEN--]\3",
        "(?i)(.*\\??password([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??token([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??session([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.+\\\".*session.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
        "(?i)(.+\\\".*token.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
        "(?i)(.+\\\".*password.*\\\"\\s*\\:\\s*\\\")(.+)(\\\"(\\,|\\}).*)": r"\1[--HIDDEN--]\3",
    },
    "url": {
        "(?i)(.*\\??password([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??token([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
        "(?i)(.*\\??session([^=]*)=)([^\\&]*)(.*)": r"\1[--HIDDEN--]\4",
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_labeler.filters.HeaderToLabelFilter'
        }
    },
    'formatters': {
        'json': {
              '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
              'format': '%(message)s'
          }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'json',
        },
    },
    'loggers': {
        'log_labeler.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

NIM_DJANGO_REQUEST_LOG_LEVEL_NAME = "HTTP_NIM_DJANGO_REQUEST_LOG_LEVEL"
MAX_REQUEST_RESPONSE_SIZE = os.getenv('MAX_REQUEST_RESPONSE_SIZE', 'OFF')
```

You can then output log messages as usual:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Hello world!")
```

Settings Description:
---------------------

######DEFAULT_LOG_LEVEL
The default log level to apply on the logger if not other log level is specified

######LOG_LABEL_REQUEST_SETTING
The list of key/value pair that maps an HTTP header to a log entry

######LOG_LABEL_EXCLUDE_LOG_LIST
The list of loggers to ignore when dynamically changing log levels

######LOG_LABEL_OBFUSCATE
The dictionary with expected key headers, body, response and URL

######NIM_DJANGO_REQUEST_LOG_LEVEL_NAME
The name of the header to use to change the logging level. EG: DEBUG, INFO, ERROR...

######MAX_REQUEST_RESPONSE_SIZE
The maximum allowed size for request and responses in case they are successful. Error message are not truncated.


License
-------

Copyright © 2012-2018, DabApps.

All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

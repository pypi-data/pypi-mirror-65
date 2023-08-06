import sys
import socket
import logging
import datetime
import traceback

from .sock import Sock
from .http import Http
from .excepthook import errorship_sys_hook_decorator


class Handler(logging.Handler):
    """
    Handler that sends errors/exceptions and their stack traces to the datadog eventstream.

    Usage:

    .. highlight:: python
    .. code-block:: python

        1. In regular python logging

        import logging
        import errorship

        def get_logger():
            logger = logging.getLogger("MyLoggerName")
            level = "INFO"
            handler = errorship.Handler(
                datadog_agent_host="localhost",
                datadog_agent_port=8125,
                errorship_license_key="MyErrorshipLicensekey",
                tags={"env": "production", "project": "accounting"},
            )
            handler.setFormatter(logging.Formatter("%(message)s"))
            handler.setLevel(level)
            logger.addHandler(handler)
            logger.setLevel(level)
            return logger


        logger = get_logger()
        logger.info("hello world")
        try:
            countries = {}
            countries["Canada"]
        except Exception as e:
            logger.exception("country_error. error={0}".format(e))

        2. In Django

        # settings.py
        LOGGING = {
            "version": 1,
            "handlers": {
                "console": {"level": "INFO", "class": "logging.StreamHandler"},
                "errorship": {
                    "level": "ERROR",
                    "class": "errorship.Handler",
                    "datadog_agent_host": "localhost",
                    "datadog_agent_port": 8125,
                    "errorship_license_key": "MyErrorshipLicensekey",
                    "tags": {"env": "production", "project": "accounting"},
                },
            },
            "loggers": {
                "django": {"handlers": ["console", "errorship"], "level": "INFO"},
                "myApp": {"handlers": ["console", "errorship"], "level": "INFO"},
            },
        }
    """

    _auth_error = "Authorization failure. Please visit https://errorship.com/ to get a valid `errorship_license_key`"

    def __init__(self, datadog_agent_host, datadog_agent_port, errorship_license_key, tags=None):
        """
        Parameters:
            datadog_agent_host(string):    The host of the DogStatsd server.
            datadog_agent_port(integer):   The port of the DogStatsd server.
            errorship_license_key(string): A unique errorship license key for this project. You can get one from "https://errorship.com/"
                                           You won't be able to send exceptions to datadog if the key is invalid.
            tags(dict or None):            Tags to attach to the exceptions sent to datadog.
        """
        super(Handler, self).__init__(level=logging.ERROR)

        datadog_agent_host = str(datadog_agent_host)
        if not isinstance(datadog_agent_host, str):
            raise TypeError(
                "`datadog_agent_host` should be of type:: `str` You entered: {0}".format(
                    type(datadog_agent_host)
                )
            )
        if not isinstance(datadog_agent_port, int):
            raise TypeError(
                "`datadog_agent_port` should be of type:: `int` You entered: {0}".format(
                    type(datadog_agent_port)
                )
            )
        if not isinstance(errorship_license_key, str):
            raise TypeError(
                "`errorship_license_key` should be of type:: `str` You entered: {0}".format(
                    type(errorship_license_key)
                )
            )
        if not isinstance(tags, (type(None), dict)):
            raise TypeError(
                "`tags` should be of type:: `dict` or `None` You entered: {0}".format(type(tags))
            )

        self.datadog_agent_host = datadog_agent_host
        self.datadog_agent_port = datadog_agent_port
        self.tags = self._convert_tags(tags)
        self.sock = Sock(host=self.datadog_agent_host, port=self.datadog_agent_port)

        self.md_tmpl = """%%%\n```python\n{trace}\n```\n\n{extra_info}%%%"""
        self.machine = socket.gethostname()
        self.arg_vector = sys.argv

        self.errorship_license_key = errorship_license_key  # this key is per project
        # auth check should be the last thing in the init method
        self._authorised, self._pricing_plan = self._check_key(self.errorship_license_key)
        if not self._authorised:
            # TODO: should we raise error or just fail silently?
            # write tests to figure it out
            raise AuthError(self._auth_error)

        self._set_sys_except_hooks()

    @staticmethod
    def _convert_tags(tags):
        """
        converts a dictionary to the representation of tags as required by datadog
        """
        if not tags:
            return None

        _tags = []
        for k, v in tags.items():
            _tags.append(str(k) + ":" + str(v))
        return _tags

    def _check_key(self, errorship_license_key):
        # check errorship_license_key
        # NB: If the data we send to errorship.com were to change,
        # we would also need to update our privacy & security policy
        # at https://errorship.com/privacy.html
        url = "https://errorship.com/api/?errorshipLicensekey={errorship_license_key}".format(
            errorship_license_key=errorship_license_key
        )
        h = Http(url=url, timeout=2.376)
        return h.req_n_auth()

    def _set_sys_except_hooks(self):
        """
        set an excepthook that will capture all uncaught exceptions
        """
        new_hook = errorship_sys_hook_decorator(
            original_excepthook=sys.excepthook, log_handler=self
        )
        if sys.excepthook.__name__ == new_hook.__name__:
            return
        else:
            sys.excepthook = new_hook

    def emit(self, record):
        """
        Send any exceptions/errors to datadog.
        """
        try:
            if record.levelno < logging.ERROR:  # self.level
                # do nothing
                return
            if not self._authorised:
                return

            # send to dd
            payload = self._make_payload(record)
            self.sock.send(payload)

            # make sure errorship excepthook still exists
            # this is because a third party excepthook may have unset our hook.
            # however, errorship plays nice and makes sure that we return control
            # to any other excepthook that may have been set before us.
            self._set_sys_except_hooks()
        except Exception:
            self.handleError(record)

    def handleError(self, record):
        """
        Handle errors which occur during an emit() call.
        """
        # we do not want errors of our logging system to affect business logic.
        # we should add a flag to this handler that will allow us to see errors
        # of this logging system when/if we need to debug it.
        self.sock.close()

    def _make_payload(self, record):
        exc_info = record.exc_info
        if not exc_info:
            exc_info = sys.exc_info()
        exception_type, exception_value, exception_traceback = exc_info

        # 1. get title
        exception_name = exception_value.__class__.__name__ if exception_value else ""
        exception_args = exception_value.args if exception_value else ""
        title = "{exception_name}{exception_args}".format(
            exception_name=exception_name, exception_args=exception_args
        )[:100]

        # 2. get text
        extra_info = (
            "**argv:** {argv}\n"
            "**hostName:** {hostName}\n"
            "**processName:** {processName}\n"
            "**threadName:** {threadName}\n"
            "**processId:** {processId}\n"
            "**threadId:** {threadId}\n"
            "**logMessage:** {logMessage}\n".format(
                argv=self.arg_vector,
                hostName=self.machine,
                processName=record.processName,
                threadName=record.threadName,
                processId=record.process,
                threadId=record.thread,
                # we don't want log message to hog the 4000char limit imposed on text field by datadog
                # so we slice it down
                logMessage=record.getMessage()[:200],
            )
        )
        stack_trace = traceback.format_exception(
            exception_type, exception_value, exception_traceback
        )
        text = self._get_and_fit_text(stack_trace=stack_trace, extra_info=extra_info)

        # 3. get date created
        date_created = int(record.created)

        # 4. get aggregation_key
        aggregation_key = "{exception_name}-{exception_args}-{today}-{tags}".format(
            # The character `|` is used by the datadog/statsD protocol and is thus special.
            # Hence, we can't use it in our own things. Thus we use `-`
            exception_name=exception_name,
            exception_args=exception_args,
            today=datetime.datetime.now().strftime("%D"),
            tags=",".join(self.tags) if self.tags else "tags",
        )[:100]

        return self._create_datadog_event(
            title=title, text=text, aggregation_key=aggregation_key, date_created=date_created
        )

    def _get_and_fit_text(self, stack_trace, extra_info):
        """
        The maximum size of text we can send to datadog is 4000chars.
        However, we may sometimes have stacktraces that are already larger than 4000chars
        by themselves even before adding all the other metadata.
        So we need a way to try and fit in the most useful info into 4000chars or less.
        """
        max_text_size = 4000  # according to datadog api
        first_trace_item_size = len(stack_trace[0])  # ie, `Traceback (most recent call last):`
        extra_info_size = len(extra_info)
        md_tmpl_size = len(self.md_tmpl)
        size_available_for_stack_trace = max_text_size - (
            first_trace_item_size + extra_info_size + md_tmpl_size
        )

        # For stack trace, the most recent calls are last.
        # And they are usually the ones that touch on users code.
        # We thus need to give them priority and make sure to include them.
        # Hence we slice using negative indice starting at the end.
        trace = stack_trace[0] + "".join(stack_trace)[-size_available_for_stack_trace:]
        trace = trace.replace(
            "Traceback (most recent call last):\nTraceback (most recent call last):\n",
            "Traceback (most recent call last):\n",
        )

        text = self.md_tmpl.format(trace=trace, extra_info=extra_info)[:max_text_size]
        return text

    def _create_datadog_event(self, title, text, aggregation_key, date_created, alert_type="error"):
        """
        documentation is at: https://docs.datadoghq.com/api/?lang=bash#post-an-event

        """
        MAX_ALLOWED_PAYLOAD_SIZE = 8 * 1024  # 8KB

        title = title.replace("\n", "\\n")
        text = text.replace("\n", "\\n")
        payload = "_e{brace_begin}{len_title},{len_text}{brace_end}:{title}|{text}|d:{date_created}|k:{aggregation_key}|t:{alert_type}".format(
            brace_begin="{",
            len_title=len(title),
            len_text=len(text),
            brace_end="}",
            title=title,
            text=text,
            date_created=date_created,
            aggregation_key=aggregation_key,
            alert_type=alert_type,
        )
        if self.tags:
            payload = "{payload}|#{tags}".format(payload=payload, tags=",".join(self.tags))

        if len(payload) > MAX_ALLOWED_PAYLOAD_SIZE:
            # drop the event on the floor
            raise PayloadError(
                "The event {title} has a size of {payload_size} which is larger than datadog max allowed size of 8KB.".format(
                    title=title, payload_size=len(payload)
                )
            )

        return payload


class AuthError(Exception):
    """
    Error raised if the project fails authentication with errorship.
    Some of the reasons for the failure is:
      1. the project has not been registered with errorship
      2. overdue subscription payment

    Please visit https://errorship.com/ to get a valid `errorship_license_key`"
    """

    pass


class PayloadError(Exception):
    """
    raised if the payload to send to datadog has an issue.
    """

    pass

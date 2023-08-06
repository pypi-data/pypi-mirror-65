import sys
import logging


def errorship_sys_hook_decorator(original_excepthook, log_handler):
    """
    usage:
        import sys

        h = errorship.Handler(
            datadog_agent_host="localhost",
            datadog_agent_port=8125,
            errorship_license_key="errorship_license_key",
            tags={"env": "production", "project": "accounting"},
        )
        sys.excepthook = errorship_sys_hook_decorator(
            original_excepthook=sys.excepthook, log_handler=h
        )
    """

    def errorship_sys_hook(exc_type, exc_value, exc_traceback):
        """
        custom excepthook.

        1. https://docs.python.org/3.6/library/sys.html#sys.excepthook
        2. https://github.com/python/cpython/blob/2.7/Python/sysmodule.c#L132-L147
        3. https://github.com/python/cpython/blob/3.8/Python/sysmodule.c#L636-L655
        """
        record = logging.LogRecord(
            name="",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="",
            args=(),
            exc_info=(exc_type, exc_value, exc_traceback),
        )

        # emit record to datadog
        log_handler.emit(record=record)

        # do normal thing
        if original_excepthook == sys.__excepthook__:
            return sys.__excepthook__(exc_type, exc_value, exc_traceback)
        elif original_excepthook.__name__ == errorship_sys_hook.__name__:
            # if `errorship_sys_hook` is the original excepthook, call the python default
            # otherwise we risk going into a recursive loop
            return sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            # Someone else had also modified `sys.excepthook`.
            # Thus, we should play fair and return control to them.
            # Let's hope that if they were called first, they would return the favor
            return original_excepthook(exc_type, exc_value, exc_traceback)

    return errorship_sys_hook

import logging
from .handler import Handler


def setup(datadog_agent_host, datadog_agent_port, errorship_license_key, tags=None):
    handler = Handler(
        datadog_agent_host=datadog_agent_host,
        datadog_agent_port=datadog_agent_port,
        errorship_license_key=errorship_license_key,
        tags=tags,
    )

    if logging.getLogger("") == logging.getLogger():
        logging.getLogger("").addHandler(handler)
    else:
        logging.getLogger("").addHandler(handler)
        logging.getLogger().addHandler(handler)

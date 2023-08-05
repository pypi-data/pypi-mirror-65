import logging

import yaml

from miniscule.base import read_config

log = logging.getLogger(__name__)


def init_logging(config=None, key="log_config"):
    """Initialize logging.

    :param config: The configuration dictionary
    :param key: The key under which the path of the logging configuration is
        stored.

    :returns: Nothing
    """

    path = (config or read_config()).get(key)
    if path is None:
        log.warning("No logging configuration specified")
        return

    with open(path, "r") as handle:
        log_config = yaml.load(handle.read(), Loader=yaml.SafeLoader)
        logging.config.dictConfig(log_config)

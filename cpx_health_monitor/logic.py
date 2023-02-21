import logging

from cpx_health_monitor.version import __version__

LOG = logging.getLogger(__name__)


def run() -> None:
    LOG.info(
        "hello from cpxstat v%s",
        __version__,
    )

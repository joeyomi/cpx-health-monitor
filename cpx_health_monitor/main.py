import logging
import sys


from typing import Optional

import click


from cpx_health_monitor.config import try_to_load_config
from cpx_health_monitor.logging import setup_logging
from cpx_health_monitor.logic import run

LOG = logging.getLogger(__name__)



@click.command()
@click.option(
    '--config_path',
    type=click.Path(dir_okay=False, path_type=str),
    required=False,
    help="Path to config file",
)
@click.option(
    '--config_section_name',
    type=str,
    required=False,
    help="Name of config section to use",
)
def main(
    config_path: Optional[str]=None,
    config_section_name: Optional[str]=None,
) -> int:
    
    config = try_to_load_config(config_path, config_section_name)

    setup_logging(config['logging'])

    try:
        LOG.info("cpxstat started")
        run()
    except Exception:
        LOG.exception("cpxstat failed")
        exit_code = -1
    else:
        LOG.info("cpxstat ended")
        exit_code = 0
    finally:
        return exit_code


if __name__ == "__main__":
    sys.exit(main())

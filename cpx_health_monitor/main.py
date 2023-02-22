#!/usr/bin/env python3

import logging
import sys

import click
import pyfiglet

# from cpx_health_monitor.config import try_to_load_config
# from cpx_health_monitor.logging import setup_logging
from cpx_health_monitor.logic import run

LOG = logging.getLogger(__name__)

# cpxstat config
"""
@click.group()
def configs():
    #Configure cpxstat
    pass


@configs.command()
@click.option(
    '--config_path',
    type=click.Path(dir_okay=False, path_type=str),
    required=False,
    help="Path to config file",
)
@configs.command()
@click.option(
    '--config_section_name',
    type=str,
    required=False,
    help="Name of config section to use",
)
@configs.command()
@click.option(
    '--list',
    type=str,
    required=False,
    help="Name of config section to use",
)
 """
# cpxstat instances list


@click.group()
def instances():
    """Monitor cpxstat instances"""
    pass


@instances.command(help="List instances")
@click.option("--service", help="Filter by service name")
@click.option("--status", help="Filter by status")
def list(service, status):
    """List instances"""
    run("instances", "list", service, status)


# cpxstat instances watch
@instances.command(help="Watch instances")
@click.option("--service", help="Filter by service name")
@click.option("--status", help="Filter by status")
def watch(service, status):
    """Watch instances"""
    run("instances", "watch", service, status)


# cpxstat instances show
@instances.command(help="Show instance details")
@click.argument("instancename")
def show(instancename):
    """Show an instance"""
    run("instances", "show", instancename)


# cpxstat services
@click.group()
def services():
    """Monitor cpxstat services"""
    pass


# cpxstat services list
@services.command(help="List services")
@click.option("--status", help="Filter by status")
def list(status):
    """List services"""
    run("services", "list", status)


# cpxstat services watch
@services.command(help="Watch services")
@click.argument("servicename", required=False)
@click.option("--status", help="Filter by status")
def watch(servicename, status):
    """Watch services"""
    run("services", "watch", servicename, status)


# cpxstat services show
@services.command(help="Show service details")
@click.argument("servicename")
def show(servicename):
    """Show a service"""
    run("services", "show", servicename)


# cpxstat CLI
@click.group(help="CPXStat command-line interface")
def cpxstat():
    """CPXStat command-line interface"""
    pass


# cpxstat.add_command(configs)
cpxstat.add_command(instances)
cpxstat.add_command(services)


# @click
def main(
    # config_path: Optional[str] = None,
    # config_section_name: Optional[str] = None,
) -> int:
    # config = try_to_load_config(config_path, config_section_name)

    # setup_logging(config['logging'])

    exit_code = None
    print(pyfiglet.figlet_format("CPX STAT"))

    try:
        LOG.info("cpxstat started")
        # run()
        cpxstat()
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

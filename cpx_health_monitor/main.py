#!/usr/bin/env python3

import logging
import sys

import click
import pyfiglet

from cpx_health_monitor.logic import run

LOG = logging.getLogger(__name__)


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
) -> int:
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

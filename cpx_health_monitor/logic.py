#!/usr/bin/env python3

import time
import click
from cpx_health_monitor.classmodules import CPXMonitor, CPXMonitorPrinter
from rich.console import Console
from rich.live import Live

import requests
from typing import List, Dict, Optional
from collections import defaultdict
from rich.table import Table

import logging

from cpx_health_monitor.version import __version__

LOG = logging.getLogger(__name__)


def run(group, command, *args) -> None:
    LOG.info(
        "hello from cpxstat v%s",
        __version__,
    )
    try:
        if group == 'instances':
            if command == 'list':
                run_list_instances(*args)
            elif command == 'watch':
                run_watch_instances(*args)
            elif command == 'show':
                run_show_instance(*args)
            else:
                raise click.UsageError(
                    f"Invalid command '{command}'. See 'cpxstat --help' for available commands.")
        elif group == 'services':
            if command == 'list':
                run_list_services(*args)
            elif command == 'watch':
                run_watch_services(*args)
            elif command == 'show':
                run_show_service(*args)
            else:
                raise click.UsageError(
                    f"Invalid command '{command}'. See 'cpxstat --help' for available commands.")
        else:
            raise click.UsageError(
                f"Invalid command '{group}'. See 'cpxstat --help' for available commands.")
            # click.echo(f"Error: Invalid command '{command}'")
            # click.echo("Run 'cpxstat --help' for more information.")
    except Exception as e:
        raise click.ClickException(str(e))
        # click.echo(f"Error: {e}")
        # click.echo("Run 'cpxstat --help' for more information.")


console = Console()

cpx = CPXMonitor()  # TODO: Initialise from config
printer = CPXMonitorPrinter(cpx_monitor=cpx)


def run_list_instances(service=None, status=None):
    # Implementation logic for listing instances
    console.print(printer.get_stats(status=status, service=service))


def run_watch_instances(service=None, status=None):
    # Implementation logic for watching instances
    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            live.update(printer.get_stats(
                status=status, service=service), refresh=True)
            time.sleep(1)


def run_show_instance(instancename):
    if not instancename:
        raise click.UsageError("Missing argument 'instancename'")
    # Implementation logic for showing instance
    console.print(printer.get_stats(ip=instancename))


def run_list_services(status=None):
    # Implementation logic for listing services
    console.print(printer.get_services(status=status))


def run_watch_services(servicename=None, status=None):
    # Implementation logic for watching services
    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            if servicename:
                live.update(printer.get_services(
                    service=servicename), refresh=True)
            else:
                live.update(printer.get_services(status=status), refresh=True)
            time.sleep(1)


def run_show_service(servicename):
    if not servicename:
        raise click.UsageError("Missing argument 'servicename'")
    # Implementation logic for showing service
    console.print(printer.get_services(service=servicename))

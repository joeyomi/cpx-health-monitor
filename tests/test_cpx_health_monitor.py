import pytest
from click.testing import CliRunner
from cpx_health_monitor.main import instances, services


@pytest.fixture
def runner():
    return CliRunner()


def test_instances_list(runner):
    result = runner.invoke(instances, ['list'])
    assert result.exit_code == 0
    assert "Instance" in result.output


def test_instances_list_with_service(runner):
    result = runner.invoke(instances, ['list', '--service', 'MLService'])
    assert result.exit_code == 0
    assert "Instance" in result.output
    assert "MLService" in result.output


def test_instances_list_with_status(runner):
    result = runner.invoke(
        instances, ['list', '--status', 'healthy'])
    assert result.exit_code == 0
    assert "Instance" in result.output
    assert "Healthy" in result.output


def test_services_list(runner):
    result = runner.invoke(services, ['list'])
    assert result.exit_code == 0
    assert "Service" in result.output


def test_services_list_with_status(runner):
    result = runner.invoke(services, ['list', '--status', 'healthy'])
    assert result.exit_code == 0
    assert "Service" in result.output
    assert "Healthy" in result.output


def test_services_show(runner):
    result = runner.invoke(services, ['show', 'AuthService'])
    assert result.exit_code == 0


""" 
def test_instances_watch(runner):
    result = runner.invoke(instances, ['watch'])
    assert result.exit_code == 0
"""


""" 
def test_instances_watch_with_service(runner):
    result = runner.invoke(instances, ['watch', '--service', 'GeoService'])
    assert result.exit_code == 0
"""


""" 
def test_instances_watch_with_status(runner):
    result = runner.invoke(instances, ['watch', '--status', 'unhealthy'])
    assert result.exit_code == 0
"""


""" 
def test_instances_show(runner):
    result = runner.invoke(instances, ['instances', 'show', 'INSTANCE_NAME'])
    assert result.exit_code == 0
"""


""" 
def test_services_watch(runner):
    result = runner.invoke(services, ['watch'])
    assert result.exit_code == 0
"""


""" 
def test_services_watch_with_service(runner):
    result = runner.invoke(services, ['watch', 'UserService'])
    assert result.exit_code == 0
"""

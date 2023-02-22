import requests
from typing import List, Dict, Optional
from collections import defaultdict
from rich.table import Table


class CPXMonitor:
    """
    Class for monitoring the health and performance of a group of servers.

    Attributes:
        host (str): The hostname or IP address of the server to monitor.
        port (int): The port number on which to access the server.
        protocol (str): The protocol to use for accessing the server (e.g. "http").
        _health_threshold (int): The maximum number of unhealthy instances that can exist before a service is marked as unhealthy.

    Methods:
        _get_instances() -> List[str]: Retrieves a list of all instances being monitored.
        _get_health(instance: dict) -> str: Determines the health status of a given instance.
        get_stats(ip: str=None) -> List[Dict[str, Dict[str, Any]]]: Retrieves performance statistics for a specified IP address or all monitored instances.
        get_services(instances: List[Dict[str, Dict[str, str]]]=None) -> List[Dict[str, Dict[str, Any]]]: Retrieves statistics for all monitored services.
    """

    def __init__(self, host="localhost", port=5000, protocol="http") -> None:
        """
        Initializes a new instance of the CPXMonitor class.

        Args:
            host (str): The hostname or IP address of the server to monitor.
            port (int): The port number on which to access the server.
            protocol (str): The protocol to use for accessing the server (e.g. "http").
        """

        self._port = port
        self._host = host
        self._protocol = protocol
        self._health_threshold = 2
        self._endpoint = f"{self._protocol}://{self._host}:{self._port}"
        self._servers_endpoint = f"{self._endpoint}/servers"

    def _get_instances(self) -> List[str]:
        """
        Retrieves a list of all instances being monitored.

        Returns:
            A list of IP addresses for all instances being monitored.
        """

        response = requests.get(self._servers_endpoint)
        response.raise_for_status()
        return response.json()

    def _get_health(self, instance: Dict[str, str]) -> str:
        """
        Determines the health status of a given instance.

        Args:
            instance (dict): A dictionary containing performance statistics for the instance.

        Returns:
            A string indicating the health status of the instance ("Healthy" or "Unhealthy").
        """

        cpu = int(instance['cpu'].replace('%', ''))
        memory = int(instance['memory'].replace('%', ''))

        if cpu >= 80 or memory >= 80:
            return "Unhealthy"
        return "Healthy"

    def get_stats(self, ip: str = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Retrieves performance statistics for a specified IP address or all monitored instances.

        Args:
            ip (str): The IP address of the instance to retrieve statistics for. If None, statistics will be retrieved for all monitored instances.

        Returns:
            A list of dictionaries containing performance statistics for each instance.
        """

        def get_stat(instance_ip: str) -> Dict[str, Dict[str, str]]:
            response = requests.get(f"{self._endpoint}/{instance_ip}")
            response.raise_for_status()
            return response.json()

        if ip is None:
            temp_list = []
            instances = self._get_instances()

            for instance in instances:
                temp = get_stat(instance_ip=instance)
                temp['status'] = self._get_health(instance=temp)
                temp_list.append({instance: temp})

            return temp_list
        else:
            temp = get_stat(instance_ip=ip)
            temp['status'] = self._get_health(instance=temp)
            return [{ip: temp}, ]

    def get_services(self, instances: List[Dict[str, Dict[str, str]]] = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Get statistics for all services running on the monitored hosts.

        Args:
            instances (List[Dict[str, Dict[str, str]]], optional):
                List of instance information dictionaries. Defaults to None.

        Returns:
            List[Dict[str, Dict[str, str]]]:
                List of service statistics dictionaries with average CPU and memory usage,
                and number of healthy, unhealthy, and total instances for each service.
        """
        if instances is None:
            instances = self.get_stats()

        service_stats = defaultdict(
            lambda: {"cpu": [], "memory": [], "healthy": 0, "unhealthy": 0, "total": 0})

        for instance in instances:
            for ip, stats in instance.items():
                service = stats["service"]
                service_stats[service]["total"] += 1
                if stats["status"] == "Unhealthy":
                    service_stats[service]["unhealthy"] += 1
                else:
                    service_stats[service]["healthy"] += 1
                service_stats[service]["cpu"].append(
                    int(stats["cpu"].replace("%", "")))
                service_stats[service]["memory"].append(
                    int(stats["memory"].replace("%", "")))

        result = []
        for service, stats in service_stats.items():
            avg_cpu = sum(stats["cpu"]) / len(stats["cpu"])
            avg_memory = sum(stats["memory"]) / len(stats["memory"])
            status = "Healthy" if stats["unhealthy"] <= self._health_threshold else "Unhealthy"

            temp = {"cpu": f"{int(avg_cpu)}%", "memory": f"{int(avg_memory)}%", "status": status,
                    "total_instances": stats["total"], "healthy_instances": stats["healthy"],
                    "unhealthy_instances": stats["unhealthy"]}

            result.append({service: temp})

        return result

    def get_services_new(self, service: Optional[str] = None,
                         instances: Optional[List[Dict[str, Dict[str, str]]]] = None) -> List[
            Dict[str, Dict[str, str]]]:
        """
        Get statistics for all services running on the monitored hosts, or a single service if specified.

        Args:
            service (str, optional):
                Name of the service to retrieve statistics for. Defaults to None.
            instances (List[Dict[str, Dict[str, str]]], optional):
                List of instance information dictionaries. Defaults to None.

        Returns:
            List[Dict[str, Dict[str, str]]]:
                List of service statistics dictionaries with average CPU and memory usage,
                and number of healthy, unhealthy, and total instances for each service.
        """
        if instances is None:
            instances = self.get_stats()

        service_stats = defaultdict(
            lambda: {"cpu": [], "memory": [], "healthy": 0, "unhealthy": 0, "total": 0})

        for instance in instances:
            for ip, stats in instance.items():
                service_name = stats["service"]
                service_stats[service_name]["total"] += 1
                if stats["status"] == "Unhealthy":
                    service_stats[service_name]["unhealthy"] += 1
                else:
                    service_stats[service_name]["healthy"] += 1
                service_stats[service_name]["cpu"].append(
                    int(stats["cpu"].replace("%", "")))
                service_stats[service_name]["memory"].append(
                    int(stats["memory"].replace("%", "")))

        result = []

        if service is not None:
            if service in service_stats:
                stats = service_stats[service]
                avg_cpu = sum(stats["cpu"]) / len(stats["cpu"])
                avg_memory = sum(stats["memory"]) / len(stats["memory"])
                status = "Healthy" if stats["unhealthy"] <= self._health_threshold else "Unhealthy"
                temp = {"cpu": f"{int(avg_cpu)}%", "memory": f"{int(avg_memory)}%", "status": status,
                        "total_instances": stats["total"], "healthy_instances": stats["healthy"],
                        "unhealthy_instances": stats["unhealthy"]}
                result.append({service: temp})
            return result

        for service_name, stats in service_stats.items():
            avg_cpu = sum(stats["cpu"]) / len(stats["cpu"])
            avg_memory = sum(stats["memory"]) / len(stats["memory"])
            status = "Healthy" if stats["unhealthy"] <= self._health_threshold else "Unhealthy"
            temp = {"cpu": f"{int(avg_cpu)}%", "memory": f"{int(avg_memory)}%", "status": status,
                    "total_instances": stats["total"], "healthy_instances": stats["healthy"],
                    "unhealthy_instances": stats["unhealthy"]}
            result.append({service_name: temp})

        return result


class CPXMonitorPrinter:
    """
    Class for printing the result of the CPXMonitor methods in a table format.
    """

    def __init__(self, cpx_monitor):
        """
        Initializes a new instance of the CPXMonitorPrinter class.

        Args:
            cpx_monitor (CPXMonitor): An instance of the CPXMonitor class.
        """
        self.cpx_monitor = cpx_monitor

    def get_stats(self, ip=None, service=None, status=None):
        """
        Retrieves performance statistics for a specified IP address or all monitored instances and prints them in a table format.

        Args:
            ip (str): The IP address of the instance to retrieve statistics for. If None, statistics will be retrieved for all monitored instances.
            service (str): The name of the service to retrieve instance statistics for. If None, instance statistics for all services will be retrieved.
            status (str): The status of the instances to retrieve statistics for. If None, statistics for all instances will be retrieved.
        """
        stats = self.cpx_monitor.get_stats(ip)

        table = Table(title="Instance Statistics")
        table.add_column("Instance", justify="left")
        table.add_column("Service", justify="left")
        table.add_column("CPU Usage", justify="right")
        table.add_column("Memory Usage", justify="right")
        table.add_column("Status", justify="center")

        temp = []

        for instance_stats in stats:
            for instance_ip, stats in instance_stats.items():
                if service is not None and stats["service"].lower() != service.lower():
                    continue
                if status is not None and stats["status"].lower() != status.lower():
                    continue
                temp.append([instance_ip, stats["service"],
                            stats["cpu"], stats["memory"], stats["status"]])

        [table.add_row(*row) for row in sorted(temp)]
        return table

    def get_services(self, instances=None, service=None, status=None):
        """
        Retrieves statistics for all services running on the monitored hosts and prints them in a table format.

        Args:
            instances (List[Dict[str, Dict[str, str]]], optional):
                List of instance information dictionaries. Defaults to None.
            service (str, optional):
                The name of the service to print the statistics for. Defaults to None.
            status (str, optional):
            The status of the instances to print the statistics for. Defaults to None.
        """
        stats = self.cpx_monitor.get_services(instances)

        table = Table(title="Service Statistics")
        table.add_column("Service", justify="left")
        table.add_column("CPU Usage", justify="right")
        table.add_column("Memory Usage", justify="right")
        table.add_column("Status", justify="center")
        table.add_column("Healthy Instances", justify="right")
        table.add_column("Unhealthy Instances", justify="right")
        table.add_column("Total Instances", justify="right")

        temp = []

        for service_stats in stats:
            for service_name, stats in service_stats.items():
                if service is not None and service_name.lower() != service.lower():
                    continue
                if status is not None and stats["status"].lower() != status.lower():
                    continue
                temp.append([
                    service_name,
                    stats["cpu"],
                    stats["memory"],
                    stats["status"],
                    str(stats["healthy_instances"]),
                    str(stats["unhealthy_instances"]),
                    str(stats["total_instances"]),
                ])

        [table.add_row(*row) for row in sorted(temp)]
        return table

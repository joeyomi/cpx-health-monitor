CPX Health Monitor CLI
======================

Command line interface (CLI) tool to monitor the health of Cloud Provider X (CPX) instances


Features
--------

* List and watch CPX instances and services.
* Filter instances and services by name and status.
* Show details of a particular instance or service.


Installation
------------

To install the CPX Health Monitor CLI, you can use pip to install the tool from a remote tar file.

* First, download the latest version of the tool from the remote tar file:

    .. code-block::

       wget https://example.com/cpxstat-1.0.0.tar.gz

* Then, use pip to install the tool from the tar file:

    .. code-block::

       pip install cpxstat-1.0.0.tar.gz

This will install the cpxstat command line tool and its dependencies in your Python environment. 

Alternatively, you can install the tool directly from a remote URL using pip:

    .. code-block::

       pip install https://example.com/cpxstat-1.0.0.tar.gz

Note that you may need to use sudo or run the command as an administrator depending on your system's configuration.

Once installed, you can run the tool using the cpxstat command.

Usage
-----

To use the CPX Health Monitor CLI, run the following command:

    .. code-block::

       cpxstat [OPTIONS] COMMAND [ARGS]...

The available commands are:

* `instances` : Monitor CPX instances.
* `services` : Monitor CPX services.

For more information on a specific command, use the --help option, for example:

    .. code-block::

       cpxstat instances --help

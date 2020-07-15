Simple application to help me organize my YouTube subscriptions by categories.

Main requirements
=================

- `Python 3.7+ <https://www.python.org/>`_
- `Poetry <https://python-poetry.org/>`_ as dependency manager
- `Docker <https://www.docker.com/>`_ for deployment

Development
===========

On repository root directory use the following command to install all dependencies and prepare your development environment. It will install all packages needed for application execution plus libraries used for development and testing.

.. code-block:: bash

    poetry install

Production
==========

To orchestrate all containers we are using `docker-compose <https://docs.docker.com/compose/>`_ and a few environment variables containing everything needed to configure the project to run.

Configuration files are:

- **docker-compose.yml**: contains the general container configurations that are suitable for development and production
- **docker-compose-prod.yml**: contains an extra service (nginx reverse proxy) and overrides some existing services. You need to change this file before starting the containers
- **.env**: contains environment variables shared by the services

After updating **docker-compose-prod.yml** doc and **.env** file, start everything with the following:

.. code:: shell

    docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d

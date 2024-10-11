# Setup local Airflow development


## Table of contents
- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [Setup Python environment](#setup-python-environment)
- [Setup Airflow](#setup-airflow)
  - [Build Airflow image](#build-custom-airflow-docker-image-from-dockerfile)
  - [Create containers](#create-containers-based-on-docker-compose-file)
- [Run Airflow](#run-airflow)


## Prerequisites

* Docker desktop installed ([source](https://www.docker.com/products/docker-desktop/))
* Python 3.11 installed ([source](https://www.python.org/downloads/release/python-3110/))


## Introduction

Local Development is splited in two:

1. Local Environment
2. Local Airflow

In order to develop locally we need a Python environment correctly setup and a Airflow instance running. Here we will use Docker to run Airflow.

How Airflow local works? We are building our custom Airflow Docker image by extending the official Apache Airflow Docker image and adding our custom Python packages. This process is defined in the `dockerfile` file. The Python packages extended by our custom Airflow Docker image are listed in the `requirements.txt` file.

After building our custom Airflow Docker image, we need to build our containers with Airflow Webserver, Airflow Worker, Airflow Triggerer and other services. We are using `docker-compose` and this process is defined in the `docker-compose.yaml` file.

Both our custom Airflow image and our local Python environment share/use the packages listed in the `requirements.txt` file. Airflow needs it to execute our DAGs and we need it in our local Python environment in order to develop our DAGs (import packages, be able to debub and etc). This is key for the local development.


## Setup Python environment

0. Make sure you are inside the root of the project

1. create virtual environment using venv
   * run `py -3.11 -m venv venv`
      * this will create a fresh Python environment using `Python 3.11` with the name `venv`

2. activate the virtual environment
   * run `.\venv\Scripts\activate.bat`

3. install dependencies
   * run `pip install -r .\.docker\requirements.txt`
     * this will install all Python packages listed in the `.\.docker\requirements.txt` file inside the new `venv` environment

After all that you should have a fresh Python 3.11 environment setup.

You can check the environment by runnign `py --list`, you should see something like `*  Active venv` - The `*` means this is the current environment and `venv` is the name.

You can check the Python packages installed in this environment by running `pip freeze`.


## Setup Airflow

Here we will build our custom Airflow Docker image and create our containers.

### Build custom Airflow docker image from Dockerfile
* checkout to `.docker` dir
  * run `cd .docker`
* build the image
  * run `docker build -t airflow .`

### Build Airflow services based on docker-compose file
* run `docker-compose build`

### Create containers
* run `docker-compose up -d`
  * this will start Airflow containers


## Run Airflow

After setting up Airflow everything should be fine. Airflow is started by running `docker-compose up -d` inside the `.docker` dir.

You don't have to run it again unless you restart your computer. You don't need to run it again if you modify the DAG files - DAGs directory are mounted to the Airflow container, changes will be mirrored automatically.

If you add new providers or Python packages you need to rebuild the custom Airflow image and build Airflow services and containers again.

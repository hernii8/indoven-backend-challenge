# Indoven backend challenge

This is the solution proposed for the backend coding challenge from Indoven for the role of backend engineer. You can check the requirements of the challenge [here] (https://github.com/idoven/backend-challenge/blob/main/README.md).


## Install

This project uses [Docker](https://www.docker.com/). Go check it out if you don't have it locally installed.

## Usage

To start the API, you'll have first to build the image:

```sh
$ docker build -t idoven-api .
```

Then you can start the container.

```sh
$ docker run -p 8000:8000 -it --rm idoven-api
```

If you don't want to use docker, you can manually run the project using Poetry and Python:

```sh
$ poetry install
$ python3 server.py
```

To ensure that the application is working, and check the API documentation with the available endpoints, you can navigate to https://localhost:8000/docs.

## Tests

To run the tests, you can use:
```sh
$ sudo docker run -it -e ENV=test --rm idoven-api pytest
```

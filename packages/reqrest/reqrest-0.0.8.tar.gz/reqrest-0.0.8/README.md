# reqrest

[![Build Status](https://github.com/rorymurdock/reqrest/workflows/Pytest/badge.svg)](https://github.com/rorymurdock/reqrest/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/ae2db247ebaa2ed83ea3/maintainability)](https://codeclimate.com/github/rorymurdock/reqREST/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/rorymurdock/reqREST/badge.svg?branch=master)](https://coveralls.io/github/rorymurdock/reqREST?branch=master)
[![Requirements Status](https://requires.io/github/rorymurdock/reqREST/requirements.svg?branch=master)](https://requires.io/github/rorymurdock/reqREST/requirements/?branch=master)

A package for using REST APIs

## Purpose

A lot of APIs are REST based, reqrest provides an easy way to use them.

## Usage

Getting started is easy, first install the package using `pip install reqrest`

Next import it

```python
from reqrest import REST
```

```python
RESTAPI = REST('postman-echo.com')
```

Then query your API

```python
RESTAPI.get('/get')
```

You can add custom headers

```python
custom_headers = {"authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="}
RESTAPI = REST('postman-echo.com', headers=custom_headers)
```

Or querystrings

```python
querystring = {}
querystring[pagesize] = 1000
RESTAPI.get('/get', querystring=querystring)
```

Have a read of `examples/simple.py`

# Authentication

You can use basic_auth to create and store your headers / config

```python
headers = Auth().read_config("basic_config.json")
RESTAPI = REST('postman-echo.com', headers=headers)
```

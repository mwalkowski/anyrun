## APP.ANY.RUN CLIENT [![Build Status](https://travis-ci.com/mwalkowski/anyrun.svg?branch=master)](https://travis-ci.com/mwalkowski/anyrun) [![codecov](https://codecov.io/gh/mwalkowski/anyrun/branch/master/graph/badge.svg)](https://codecov.io/gh/mwalkowski/anyrun) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![PyPI version](https://badge.fury.io/py/anyrun.svg)](https://badge.fury.io/py/anyrun)

This is a package that allows downloading and searching malware analysis from public submissions from [app.any.run](https://app.any.run).
It is built as a websocket client application 

### Features


- Register to all public submissions
- Requirements

   - websocket_client==0.56.0
   - Python 3.5, 3.6, 3.7

### Installation


You can install django-celery-results either via the Python Package Index (PyPI)
or from source.

To install using `pip`,::

    $ pip install -U anyrun
 
### QuickStart

```
from anyrun import AnyRunClient


def callback(msg: dict) -> None:
    print(msg)


if __name__ == "__main__":
    client = AnyRunClient(
        on_message_cb=callback,
        enable_trace=False
    )
    client.connect()
    client.run_forever()

````
And as a response you should get
```
...
...
{'msg': 'added', 'collection': 'tasks', 'id': '5cf6d8005ed7525c25fe5660', 'fields': ... }
...
...
```
### Settings

|param|description|
|---|---|
|enable_trace| enables debug trace logs, default: False|


Testing
-------
You can run the tests by using tox.
```
pip install tox
```
Then:   
```
tox
```

TODO
----

- Add support for search.
- More examples.
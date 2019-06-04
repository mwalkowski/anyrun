## APP.ANY.RUN CLIENT [![Build Status](https://travis-ci.com/mwalkowski/anyrun.svg?branch=master)](https://travis-ci.com/mwalkowski/anyrun) [![codecov](https://codecov.io/gh/mwalkowski/anyrun/branch/master/graph/badge.svg)](https://codecov.io/gh/mwalkowski/anyrun)

This is a package that allows downloading and searching malware analysis from public submissions from [app.any.run](https://app.any.run).
It is built as a websocket client application 

### Features


- Register to all public submissions
- Requirements

   - websocket_client==0.56.0
   - Python 3.5, 3.6, 3.7

### QuickStart

```
from anyrun.client import AnyRunClient


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
You can run the tests by creating a Python virtual environment, installing
the requirements from `test_requirements.txt` 
```
pip install -r requirements.txt -r test_requirements.txt
```
Then:   
```
python pytest
```

TODO
----

- Add support for search.
- Add more tests
- More examples.
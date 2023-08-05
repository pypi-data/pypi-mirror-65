Figure SDK
---------

The official [Figure](https://figure.co/) SDK for Python.

Role
----

The intention of this module is to provide developers a nice API to integrate their Python applications with Figure.

Installation
------------

Install the Figure SDK:

From Source:
```
git clone https://github.com/postcard/figure-sdk-python
cd figure-sdk-python 
python setup.py install
```

From git:
```
pip install git+https://github.com/postcard/figure-sdk-python.git
```

From PyPi:
``` 
pip install figure-sdk
``` 


Platforms
---------

We also support [NodeJS SDK](https://github.com/postcard/figure-sdk-node).

Basic Usage
-----------

```python
>>> import figure
>>> figure.token = "yourtoken"
>>> data = figure.Portrait.get_all(query={'event__uuid': 'event__uuid', 'last': 10})
>>> # do something with data
...
```

Support
-------

If you're having any problem, please [raise an issue](https://github.com/postcard/figure-sdk-python/issues/new).


License
-------

The project is licensed under the MIT license.

# HTTP Request Methods

HTTP verbs that python core's HTTP parser supports.

This module provides an export that is just like
[HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) from Developer Mozilla,
with the following differences:

  * All method names are lower-cased.
  * All method names are upper-cased.

We use the methods package from [Node.js](https://www.npmjs.com/package/methods) as inspiration

## Install
Install and update using [Pip](https://pypi.org/):

```sh
$ pip install httpmethods
```

## API

```python
import httpmethods as methods
```


### A Simple Example
```python
from httpmethods import getHttpMethods

for method in getHttpMethods():
    print(method)
```
```
$ get
$ post
$ put
$ delete
$ ...
```

```python
from httpmethods import getHttpMethods

for method in getHttpMethods(uppercase=True):
    print(method)
```
```
$ GET
$ POST
$ PUT
$ DELETE
$ ...
```
## License

[MIT](LICENSE)
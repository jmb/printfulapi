# Printful API Python Library

A python wrapper for [Printful API v2.0](https://developers.printful.com/docs/v2-beta/).

## Usage
Set your Printful API token up at https://developers.printful.com

Put your Prinful API token into an environment variable `PRINTFUL_API_TOKEN` or in a `.env` file:
```
PRINTFUL_API_TOKEN=<api key string>
```

To get your list of stores (for example):
```
from printful.rest_adapter import RestAdapter
from printful.models.generic import Result
from printful.utils import get_api_token
apikey = get_api_token()
pfapi = RestAdapter(api_key=apikey)
stores = pfapi.get(endpoint="/stores")
print(stores.data)
```

The output is a JSON dictionary with a list of stores with some extra paging and link information:
```
{'data': [{'id': 10, 'name': 'My Store', 'type': 'native'}], 'extra': [], 'paging': {'total': 1, 'limit': 20, 'offset': 0}, '_links': {'self': {'href': 'https://api.printful.com/v2/stores?limit=20'}}}
```

## Contributing

I have been trying to follow the project structure guide as laid out by [The Hitchhikers Guide to Python](https://docs.python-guide.org/writing/structure/) with [this guide from pretzellogix.net](https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/) my initial guide on how to write an API library module.

Please submit pull requests and comments - I'm sure this could be better!
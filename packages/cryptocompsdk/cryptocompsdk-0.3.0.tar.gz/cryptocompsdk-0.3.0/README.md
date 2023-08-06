# CryptoCompare-Py

## Overview

This is a Python SDK for the CryptoCompare APIs which require an API key.

https://min-api.cryptocompare.com/pricing

## Getting Started

Install `cryptocompsdk`:

```
pip install cryptocompsdk
```

A simple example:

```python
import cryptocompsdk

from cryptocompsdk import CryptoCompare
API_KEY = 'my-api-key'
cc = CryptoCompare(API_KEY)

data = cc.history.get(from_symbol='BTC', to_symbol='USD', exchange='Kraken')
df = data.to_df()
```

## Links

See the
[documentation here.](https://nickderobertis.github.io/cryptocompare-py/)


## Author

Created by Nick DeRobertis. MIT License.

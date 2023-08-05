# Vega API client

![Python tests](https://github.com/vegaprotocol/python-api-client/workflows/Python%20tests/badge.svg?branch=master)

This is the Vega API client, which can talk to a Vega node using gRPC or REST.

## Example

```python
from google.protobuf.empty_pb2 import Empty

import vegaapiclient as vac

# Either gRPC
api = vac.API.GRPC
url = "veganode.example.com:1234"

# Or REST
# api = vac.API.REST
# url = "https://veganode.example.com"

# Create client for accessing public data
datacli = vac.VegaTradingDataClient(api, url)

# Create client for trading (e.g. submitting orders)
tradingcli = vac.VegaTradingClient(api, url)

# Get a list of markets
markets = datacli.Markets(Empty()).markets

# Get a specific market by ID
req = vac.grpc.api.trading.MarketByIDRequest(marketID="MARKETID")
market = datacli.MarketByID(req)
```

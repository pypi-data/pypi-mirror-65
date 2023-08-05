import os
import pytest

import vegaapiclient as vac


@pytest.fixture(scope='module')
def tradingGRPC():
    grpc_node = os.getenv("GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    return vac.VegaTradingClient(vac.API.GRPC, grpc_node)


@pytest.fixture(scope='module')
def tradingdataGRPC():
    grpc_node = os.getenv("GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    return vac.VegaTradingDataClient(vac.API.GRPC, grpc_node)


@pytest.fixture(scope='module')
def tradingREST():
    rest_node = os.getenv("REST_NODE")
    assert rest_node is not None and rest_node != ""
    return vac.VegaTradingClient(vac.API.REST, rest_node)


@pytest.fixture(scope='module')
def tradingdataREST():
    rest_node = os.getenv("REST_NODE")
    assert rest_node is not None and rest_node != ""
    return vac.VegaTradingDataClient(vac.API.REST, rest_node)


@pytest.fixture(scope='module')
def walletclient():
    walletserver = os.getenv("WALLETSERVER")
    assert walletserver is not None and walletserver != ""
    return vac.WalletClient(walletserver)

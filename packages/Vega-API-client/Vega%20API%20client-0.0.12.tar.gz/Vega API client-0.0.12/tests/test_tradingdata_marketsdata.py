from google.protobuf.empty_pb2 import Empty

from .fixtures import tradingdataGRPC, tradingdataREST  # noqa: F401


def test_MarketsData(tradingdataGRPC, tradingdataREST):  # noqa: F811
    g = tradingdataGRPC.MarketsData(Empty())
    r = tradingdataREST.MarketsData(Empty())

    # The order (of MarketData objects in the list) is not guaranteed.
    gIDs = set(md.market for md in g.marketsData)
    rIDs = set(md.market for md in r.marketsData)
    assert gIDs == rIDs

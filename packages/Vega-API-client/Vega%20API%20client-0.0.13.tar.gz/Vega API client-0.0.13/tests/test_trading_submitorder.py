import base64
import binascii
from google.protobuf.empty_pb2 import Empty

import vegaapiclient as vac

from .fixtures import (  # noqa: F401
    tradingGRPC,
    tradingdataGRPC,
    tradingREST,
    tradingdataREST,
    walletclient,
    walletname,
    walletpassphrase,
    walletClientWalletKeypair
)


def test_SubmitOrderGRPC(
    tradingGRPC, tradingdataGRPC, walletClientWalletKeypair  # noqa: F811
):
    submitOrder(tradingGRPC, tradingdataGRPC, walletClientWalletKeypair)


def test_SubmitOrderREST(
    tradingREST, tradingdataREST, walletClientWalletKeypair  # noqa: F811
):
    submitOrder(tradingREST, tradingdataREST, walletClientWalletKeypair)


def submitOrder(
    trading, tradingdata, walletClientWalletKeypair  # noqa: F811
):
    (
        walletclient, walletname, passphrase, pubKey  # noqa: F811
    ) = walletClientWalletKeypair

    # Get free money for the pubKey
    request = vac.grpc.api.trading.NotifyTraderAccountRequest(
        notif=vac.grpc.vega.NotifyTraderAccount(
            traderID=pubKey,
            amount=10000000
        )
    )
    response = trading.NotifyTraderAccount(request)
    assert response.submitted

    markets = tradingdata.Markets(Empty()).markets
    assert len(markets) > 0
    market = markets[0]

    # Prepare the SubmitOrder
    now = int(tradingdata.GetVegaTime(Empty()).timestamp)
    request = vac.grpc.api.trading.SubmitOrderRequest(
        submission=vac.grpc.vega.OrderSubmission(
            expiresAt=now + 120000000000,
            marketID=market.id,
            partyID=pubKey,
            price=10,
            side=vac.grpc.vega.Side.Buy,
            size=1,
            timeInForce=vac.grpc.vega.Order.TimeInForce.GTT,
            type=vac.grpc.vega.Order.Type.LIMIT
        )
    )
    response = trading.PrepareSubmitOrder(request)
    blob = response.blob
    pendingOrder = response.pendingOrder
    assert pendingOrder.reference != ""
    assert pendingOrder.price == request.submission.price
    assert pendingOrder.marketID == request.submission.marketID
    assert pendingOrder.partyID == request.submission.partyID
    assert pendingOrder.size == request.submission.size

    # Sign the tx
    r = walletclient.signtx(base64.b64encode(blob).decode("ascii"), pubKey)
    assert r.status_code == 200
    signedTx = r.json()["signedTx"]

    # Submit the signed transaction
    request = vac.grpc.api.trading.SubmitTransactionRequest(
        tx=vac.grpc.vega.SignedBundle(
            data=base64.b64decode(signedTx["data"]),
            sig=base64.b64decode(signedTx["sig"]),
            pubKey=binascii.unhexlify(signedTx["pubKey"])
        )
    )
    assert len(request.tx.pubKey) == 32, binascii.hexlify(request.tx.pubKey)
    response = trading.SubmitTransaction(request)
    assert response.success

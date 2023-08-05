import requests


class VegaTradingClient(object):
    """
    The Vega Trading Client talks to a back-end node.
    """

    def __init__(
        self,
        url: str
    ) -> None:
        if url is None:
            raise Exception("Missing node URL")
        self.url = url

        self._httpsession = requests.Session()

    # PrepareSubmitOrder,SubmitOrderRequest,PrepareSubmitOrderResponse
    # PrepareCancelOrder,CancelOrderRequest,PrepareCancelOrderResponse
    # PrepareAmendOrder,AmendOrderRequest,PrepareAmendOrderResponse
    # Withdraw,WithdrawRequest,WithdrawResponse
    # SubmitTransaction,SubmitTransactionRequest,SubmitTransactionResponse

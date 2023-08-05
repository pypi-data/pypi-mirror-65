from .api import API
from .grpc import VegaTradingClient as grpcTradingClient
from .rest import VegaTradingClient as restTradingClient


class VegaTradingClient(object):

    def __init__(
        self,
        url: str
    ) -> None:
        if any(url.startswith(prefix) for prefix in ["https://", "http://"]):
            self._restImpl = restTradingClient(url)
            self._api = API.REST
        else:
            self._grpcImpl = grpcTradingClient(url)
            self._api = API.GRPC

    def __getattr__(self, funcname):
        if self._api == API.GRPC:
            return getattr(self._grpcImpl, funcname)
        elif self._api == API.REST:
            return getattr(self._restImpl, funcname)
        else:
            raise Exception("API not implemented")

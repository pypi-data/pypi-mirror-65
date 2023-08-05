from .cfx import CFXMessage


class AreYouThereRequest(CFXMessage):
    """
    Allows any CFX endpoint to determine if another particular CFX endpoint is present on a CFX network.
    The response sends basic information about the endpoint, including its CFX Handle, and network hostname / address.
    """
    pass


class AreYouThereResponse(CFXMessage):
    pass


class WhoIsThereRequest(CFXMessage):
    pass


class WhoIsThereResponse(CFXMessage):
    pass

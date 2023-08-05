from .cfx import CFXMessage

class EndpointConnected(CFXMessage):
    pass

class EndpointShuttingDown(CFXMessage):
    pass

class GetEndpointInformationRequest(CFXMessage):
    pass

class GetEndpointInformationResponse(CFXMessage):
    pass

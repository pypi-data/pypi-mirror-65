

from ..utils import Object


class CallState(Object):
    """
    Describes the current call state

    No parameters required.
    """
    ID = "callState"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "CallStateReady or CallStateHangingUp or CallStateDiscarded or CallStatePending or CallStateError or CallStateExchangingKeys":
        if q.get("@type"):
            return Object.read(q)
        return CallState()



from ..utils import Object


class CallDiscardReason(Object):
    """
    Describes the reason why a call was discarded

    No parameters required.
    """
    ID = "callDiscardReason"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "CallDiscardReasonEmpty or CallDiscardReasonMissed or CallDiscardReasonDeclined or CallDiscardReasonDisconnected or CallDiscardReasonHungUp":
        if q.get("@type"):
            return Object.read(q)
        return CallDiscardReason()

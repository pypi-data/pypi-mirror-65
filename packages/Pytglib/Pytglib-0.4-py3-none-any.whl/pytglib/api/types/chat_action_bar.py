

from ..utils import Object


class ChatActionBar(Object):
    """
    Describes actions which should be possible to do through a chat action bar

    No parameters required.
    """
    ID = "chatActionBar"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatActionBarReportUnrelatedLocation or ChatActionBarAddContact or ChatActionBarReportSpam or ChatActionBarReportAddBlock or ChatActionBarSharePhoneNumber":
        if q.get("@type"):
            return Object.read(q)
        return ChatActionBar()

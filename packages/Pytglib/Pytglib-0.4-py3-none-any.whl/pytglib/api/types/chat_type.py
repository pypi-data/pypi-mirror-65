

from ..utils import Object


class ChatType(Object):
    """
    Describes the type of a chat

    No parameters required.
    """
    ID = "chatType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatTypeSecret or ChatTypeBasicGroup or ChatTypePrivate or ChatTypeSupergroup":
        if q.get("@type"):
            return Object.read(q)
        return ChatType()

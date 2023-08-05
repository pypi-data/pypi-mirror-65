

from ..utils import Object


class ChatMembersFilter(Object):
    """
    Specifies the kind of chat members to return in searchChatMembers

    No parameters required.
    """
    ID = "chatMembersFilter"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatMembersFilterContacts or ChatMembersFilterBots or ChatMembersFilterMembers or ChatMembersFilterAdministrators or ChatMembersFilterRestricted or ChatMembersFilterBanned":
        if q.get("@type"):
            return Object.read(q)
        return ChatMembersFilter()

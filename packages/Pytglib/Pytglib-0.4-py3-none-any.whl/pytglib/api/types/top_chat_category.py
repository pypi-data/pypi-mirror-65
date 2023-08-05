

from ..utils import Object


class TopChatCategory(Object):
    """
    Represents the categories of chats for which a list of frequently used chats can be retrieved

    No parameters required.
    """
    ID = "topChatCategory"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "TopChatCategoryGroups or TopChatCategoryForwardChats or TopChatCategoryChannels or TopChatCategoryCalls or TopChatCategoryInlineBots or TopChatCategoryBots or TopChatCategoryUsers":
        if q.get("@type"):
            return Object.read(q)
        return TopChatCategory()

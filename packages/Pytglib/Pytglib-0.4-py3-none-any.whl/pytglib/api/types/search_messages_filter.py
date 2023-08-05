

from ..utils import Object


class SearchMessagesFilter(Object):
    """
    Represents a filter for message search results

    No parameters required.
    """
    ID = "searchMessagesFilter"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "SearchMessagesFilterPhotoAndVideo or SearchMessagesFilterUrl or SearchMessagesFilterEmpty or SearchMessagesFilterCall or SearchMessagesFilterUnreadMention or SearchMessagesFilterChatPhoto or SearchMessagesFilterMention or SearchMessagesFilterVideoNote or SearchMessagesFilterVoiceAndVideoNote or SearchMessagesFilterVoiceNote or SearchMessagesFilterDocument or SearchMessagesFilterVideo or SearchMessagesFilterAudio or SearchMessagesFilterMissedCall or SearchMessagesFilterPhoto or SearchMessagesFilterAnimation":
        if q.get("@type"):
            return Object.read(q)
        return SearchMessagesFilter()

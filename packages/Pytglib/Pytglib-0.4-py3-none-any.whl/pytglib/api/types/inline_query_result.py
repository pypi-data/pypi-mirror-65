

from ..utils import Object


class InlineQueryResult(Object):
    """
    Represents a single result of an inline query

    No parameters required.
    """
    ID = "inlineQueryResult"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InlineQueryResultAnimation or InlineQueryResultVideo or InlineQueryResultVoiceNote or InlineQueryResultSticker or InlineQueryResultVenue or InlineQueryResultGame or InlineQueryResultDocument or InlineQueryResultContact or InlineQueryResultArticle or InlineQueryResultLocation or InlineQueryResultAudio or InlineQueryResultPhoto":
        if q.get("@type"):
            return Object.read(q)
        return InlineQueryResult()

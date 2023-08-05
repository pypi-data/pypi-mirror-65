

from ..utils import Object


class InputInlineQueryResult(Object):
    """
    Represents a single result of an inline query; for bots only

    No parameters required.
    """
    ID = "inputInlineQueryResult"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputInlineQueryResultArticle or InputInlineQueryResultVoiceNote or InputInlineQueryResultAudio or InputInlineQueryResultAnimatedGif or InputInlineQueryResultLocation or InputInlineQueryResultVenue or InputInlineQueryResultVideo or InputInlineQueryResultGame or InputInlineQueryResultContact or InputInlineQueryResultPhoto or InputInlineQueryResultSticker or InputInlineQueryResultAnimatedMpeg4 or InputInlineQueryResultDocument":
        if q.get("@type"):
            return Object.read(q)
        return InputInlineQueryResult()

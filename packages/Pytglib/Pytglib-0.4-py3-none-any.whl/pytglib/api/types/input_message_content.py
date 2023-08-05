

from ..utils import Object


class InputMessageContent(Object):
    """
    The content of a message to send

    No parameters required.
    """
    ID = "inputMessageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputMessageText or InputMessageAudio or InputMessageDice or InputMessagePoll or InputMessageSticker or InputMessageVideoNote or InputMessageVenue or InputMessageVoiceNote or InputMessageContact or InputMessageVideo or InputMessagePhoto or InputMessageGame or InputMessageForwarded or InputMessageInvoice or InputMessageDocument or InputMessageLocation or InputMessageAnimation":
        if q.get("@type"):
            return Object.read(q)
        return InputMessageContent()

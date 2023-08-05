

from ..utils import Object


class ChatAction(Object):
    """
    Describes the different types of activity in a chat

    No parameters required.
    """
    ID = "chatAction"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatActionUploadingVideo or ChatActionChoosingContact or ChatActionUploadingVoiceNote or ChatActionTyping or ChatActionRecordingVideo or ChatActionChoosingLocation or ChatActionUploadingVideoNote or ChatActionUploadingDocument or ChatActionStartPlayingGame or ChatActionUploadingPhoto or ChatActionRecordingVideoNote or ChatActionRecordingVoiceNote or ChatActionCancel":
        if q.get("@type"):
            return Object.read(q)
        return ChatAction()

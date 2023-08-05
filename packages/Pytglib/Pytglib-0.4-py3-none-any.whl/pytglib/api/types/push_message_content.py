

from ..utils import Object


class PushMessageContent(Object):
    """
    Contains content of a push message notification

    No parameters required.
    """
    ID = "pushMessageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PushMessageContentContact or PushMessageContentMediaAlbum or PushMessageContentContactRegistered or PushMessageContentVoiceNote or PushMessageContentScreenshotTaken or PushMessageContentChatChangeTitle or PushMessageContentAnimation or PushMessageContentInvoice or PushMessageContentGameScore or PushMessageContentPhoto or PushMessageContentBasicGroupChatCreate or PushMessageContentText or PushMessageContentPoll or PushMessageContentHidden or PushMessageContentDocument or PushMessageContentChatAddMembers or PushMessageContentChatChangePhoto or PushMessageContentVideo or PushMessageContentMessageForwards or PushMessageContentSticker or PushMessageContentChatJoinByLink or PushMessageContentAudio or PushMessageContentVideoNote or PushMessageContentLocation or PushMessageContentChatDeleteMember or PushMessageContentGame":
        if q.get("@type"):
            return Object.read(q)
        return PushMessageContent()

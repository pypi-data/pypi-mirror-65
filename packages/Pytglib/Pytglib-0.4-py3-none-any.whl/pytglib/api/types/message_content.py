

from ..utils import Object


class MessageContent(Object):
    """
    Contains the content of a message

    No parameters required.
    """
    ID = "messageContent"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "MessageChatSetTtl or MessagePassportDataReceived or MessagePassportDataSent or MessageChatChangeTitle or MessageDocument or MessageExpiredPhoto or MessagePoll or MessageCustomServiceAction or MessageChatDeleteMember or MessageChatChangePhoto or MessageScreenshotTaken or MessageAnimation or MessageContactRegistered or MessageCall or MessageChatJoinByLink or MessageDice or MessageText or MessageChatAddMembers or MessageVenue or MessageVoiceNote or MessagePhoto or MessageExpiredVideo or MessageSticker or MessageChatUpgradeFrom or MessageLocation or MessageUnsupported or MessageVideo or MessageContact or MessageSupergroupChatCreate or MessageChatUpgradeTo or MessageGame or MessageChatDeletePhoto or MessagePaymentSuccessfulBot or MessageAudio or MessageBasicGroupChatCreate or MessageInvoice or MessageGameScore or MessageWebsiteConnected or MessagePaymentSuccessful or MessagePinMessage or MessageVideoNote":
        if q.get("@type"):
            return Object.read(q)
        return MessageContent()

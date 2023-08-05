

from ..utils import Object


class ChatEventAction(Object):
    """
    Represents a chat event

    No parameters required.
    """
    ID = "chatEventAction"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatEventPhotoChanged or ChatEventIsAllHistoryAvailableToggled or ChatEventTitleChanged or ChatEventMessageEdited or ChatEventMessagePinned or ChatEventLocationChanged or ChatEventMemberLeft or ChatEventInvitesToggled or ChatEventMemberPromoted or ChatEventLinkedChatChanged or ChatEventDescriptionChanged or ChatEventMemberInvited or ChatEventMessageDeleted or ChatEventSlowModeDelayChanged or ChatEventMemberRestricted or ChatEventPollStopped or ChatEventMessageUnpinned or ChatEventUsernameChanged or ChatEventStickerSetChanged or ChatEventSignMessagesToggled or ChatEventPermissionsChanged or ChatEventMemberJoined":
        if q.get("@type"):
            return Object.read(q)
        return ChatEventAction()

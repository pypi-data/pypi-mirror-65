

from ..utils import Object


class UserPrivacySetting(Object):
    """
    Describes available user privacy settings

    No parameters required.
    """
    ID = "userPrivacySetting"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UserPrivacySettingAllowCalls or UserPrivacySettingShowLinkInForwardedMessages or UserPrivacySettingAllowPeerToPeerCalls or UserPrivacySettingAllowFindingByPhoneNumber or UserPrivacySettingShowPhoneNumber or UserPrivacySettingShowProfilePhoto or UserPrivacySettingShowStatus or UserPrivacySettingAllowChatInvites":
        if q.get("@type"):
            return Object.read(q)
        return UserPrivacySetting()

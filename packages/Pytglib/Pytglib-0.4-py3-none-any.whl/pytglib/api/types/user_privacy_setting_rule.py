

from ..utils import Object


class UserPrivacySettingRule(Object):
    """
    Represents a single rule for managing privacy settings

    No parameters required.
    """
    ID = "userPrivacySettingRule"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UserPrivacySettingRuleRestrictAll or UserPrivacySettingRuleAllowContacts or UserPrivacySettingRuleRestrictUsers or UserPrivacySettingRuleRestrictChatMembers or UserPrivacySettingRuleRestrictContacts or UserPrivacySettingRuleAllowAll or UserPrivacySettingRuleAllowUsers or UserPrivacySettingRuleAllowChatMembers":
        if q.get("@type"):
            return Object.read(q)
        return UserPrivacySettingRule()



from ..utils import Object


class Update(Object):
    """
    Contains notifications about data changes

    No parameters required.
    """
    ID = "update"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "UpdateMessageSendAcknowledged or UpdateChatDraftMessage or UpdateNewInlineCallbackQuery or UpdateChatHasScheduledMessages or UpdatePoll or UpdateTermsOfService or UpdateNewCallbackQuery or UpdateMessageContent or UpdateLanguagePackStrings or UpdateChatChatList or UpdateMessageViews or UpdateChatDefaultDisableNotification or UpdateFavoriteStickers or UpdateUserChatAction or UpdateInstalledStickerSets or UpdateNewShippingQuery or UpdateChatIsSponsored or UpdateSecretChat or UpdateChatPinnedMessage or UpdateMessageSendFailed or UpdateChatPhoto or UpdateBasicGroup or UpdateBasicGroupFullInfo or UpdateChatIsPinned or UpdateNewCustomQuery or UpdateAuthorizationState or UpdateFile or UpdateNewChat or UpdateNewMessage or UpdateChatUnreadMentionCount or UpdateHavePendingNotifications or UpdateUserStatus or UpdateConnectionState or UpdateChatActionBar or UpdateChatLastMessage or UpdateNotificationGroup or UpdateSupergroupFullInfo or UpdateNewChosenInlineResult or UpdateMessageMentionRead or UpdateChatReplyMarkup or UpdateChatOrder or UpdateFileGenerationStop or UpdateUnreadMessageCount or UpdateMessageEdited or UpdateChatReadInbox or UpdateChatOnlineMemberCount or UpdateUsersNearby or UpdateNewInlineQuery or UpdateSelectedBackground or UpdateSavedAnimations or UpdatePollAnswer or UpdateMessageContentOpened or UpdateChatNotificationSettings or UpdateOption or UpdateUnreadChatCount or UpdateNotification or UpdateMessageLiveLocationViewed or UpdateChatTitle or UpdateDeleteMessages or UpdateActiveNotifications or UpdateUser or UpdateChatPermissions or UpdateChatIsMarkedAsUnread or UpdateServiceNotification or UpdateCall or UpdateTrendingStickerSets or UpdateNewCustomEvent or UpdateUserPrivacySettingRules or UpdateSupergroup or UpdateRecentStickers or UpdateScopeNotificationSettings or UpdateNewPreCheckoutQuery or UpdateChatReadOutbox or UpdateUserFullInfo or UpdateFileGenerationStart or UpdateMessageSendSucceeded":
        if q.get("@type"):
            return Object.read(q)
        return Update()

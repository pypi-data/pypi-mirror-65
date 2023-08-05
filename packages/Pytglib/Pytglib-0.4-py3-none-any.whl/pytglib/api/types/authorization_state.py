

from ..utils import Object


class AuthorizationState(Object):
    """
    Represents the current authorization state of the client

    No parameters required.
    """
    ID = "authorizationState"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "AuthorizationStateWaitRegistration or AuthorizationStateClosed or AuthorizationStateWaitPhoneNumber or AuthorizationStateWaitEncryptionKey or AuthorizationStateWaitCode or AuthorizationStateWaitPassword or AuthorizationStateClosing or AuthorizationStateWaitOtherDeviceConfirmation or AuthorizationStateLoggingOut or AuthorizationStateWaitTdlibParameters or AuthorizationStateReady":
        if q.get("@type"):
            return Object.read(q)
        return AuthorizationState()



from ..utils import Object


class PassportElementErrorSource(Object):
    """
    Contains the description of an error in a Telegram Passport element

    No parameters required.
    """
    ID = "passportElementErrorSource"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementErrorSourceSelfie or PassportElementErrorSourceDataField or PassportElementErrorSourceFiles or PassportElementErrorSourceFrontSide or PassportElementErrorSourceFile or PassportElementErrorSourceTranslationFile or PassportElementErrorSourceUnspecified or PassportElementErrorSourceReverseSide or PassportElementErrorSourceTranslationFiles":
        if q.get("@type"):
            return Object.read(q)
        return PassportElementErrorSource()

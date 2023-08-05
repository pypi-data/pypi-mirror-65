

from ..utils import Object


class InputPassportElementErrorSource(Object):
    """
    Contains the description of an error in a Telegram Passport element; for bots only

    No parameters required.
    """
    ID = "inputPassportElementErrorSource"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputPassportElementErrorSourceTranslationFile or InputPassportElementErrorSourceReverseSide or InputPassportElementErrorSourceSelfie or InputPassportElementErrorSourceDataField or InputPassportElementErrorSourceFile or InputPassportElementErrorSourceFrontSide or InputPassportElementErrorSourceFiles or InputPassportElementErrorSourceUnspecified or InputPassportElementErrorSourceTranslationFiles":
        if q.get("@type"):
            return Object.read(q)
        return InputPassportElementErrorSource()

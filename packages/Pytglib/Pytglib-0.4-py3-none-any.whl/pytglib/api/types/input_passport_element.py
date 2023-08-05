

from ..utils import Object


class InputPassportElement(Object):
    """
    Contains information about a Telegram Passport element to be saved

    No parameters required.
    """
    ID = "inputPassportElement"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InputPassportElementAddress or InputPassportElementUtilityBill or InputPassportElementTemporaryRegistration or InputPassportElementPersonalDetails or InputPassportElementInternalPassport or InputPassportElementPassportRegistration or InputPassportElementBankStatement or InputPassportElementPhoneNumber or InputPassportElementRentalAgreement or InputPassportElementEmailAddress or InputPassportElementIdentityCard or InputPassportElementDriverLicense or InputPassportElementPassport":
        if q.get("@type"):
            return Object.read(q)
        return InputPassportElement()

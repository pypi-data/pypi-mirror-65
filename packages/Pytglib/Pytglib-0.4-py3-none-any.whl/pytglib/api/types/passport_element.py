

from ..utils import Object


class PassportElement(Object):
    """
    Contains information about a Telegram Passport element

    No parameters required.
    """
    ID = "passportElement"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementIdentityCard or PassportElementDriverLicense or PassportElementBankStatement or PassportElementPersonalDetails or PassportElementPassportRegistration or PassportElementEmailAddress or PassportElementTemporaryRegistration or PassportElementUtilityBill or PassportElementInternalPassport or PassportElementPhoneNumber or PassportElementRentalAgreement or PassportElementPassport or PassportElementAddress":
        if q.get("@type"):
            return Object.read(q)
        return PassportElement()

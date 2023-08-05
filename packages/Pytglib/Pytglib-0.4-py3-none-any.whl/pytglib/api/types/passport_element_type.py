

from ..utils import Object


class PassportElementType(Object):
    """
    Contains the type of a Telegram Passport element

    No parameters required.
    """
    ID = "passportElementType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PassportElementTypeAddress or PassportElementTypePhoneNumber or PassportElementTypeIdentityCard or PassportElementTypePersonalDetails or PassportElementTypeRentalAgreement or PassportElementTypePassportRegistration or PassportElementTypeBankStatement or PassportElementTypeInternalPassport or PassportElementTypeDriverLicense or PassportElementTypeEmailAddress or PassportElementTypePassport or PassportElementTypeUtilityBill or PassportElementTypeTemporaryRegistration":
        if q.get("@type"):
            return Object.read(q)
        return PassportElementType()

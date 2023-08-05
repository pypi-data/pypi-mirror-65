

from ..utils import Object


class InlineKeyboardButtonType(Object):
    """
    Describes the type of an inline keyboard button

    No parameters required.
    """
    ID = "inlineKeyboardButtonType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "InlineKeyboardButtonTypeCallbackGame or InlineKeyboardButtonTypeSwitchInline or InlineKeyboardButtonTypeLoginUrl or InlineKeyboardButtonTypeBuy or InlineKeyboardButtonTypeUrl or InlineKeyboardButtonTypeCallback":
        if q.get("@type"):
            return Object.read(q)
        return InlineKeyboardButtonType()

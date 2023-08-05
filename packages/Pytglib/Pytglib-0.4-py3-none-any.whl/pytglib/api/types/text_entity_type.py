

from ..utils import Object


class TextEntityType(Object):
    """
    Represents a part of the text which must be formatted differently

    No parameters required.
    """
    ID = "textEntityType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "TextEntityTypeCode or TextEntityTypeHashtag or TextEntityTypeMention or TextEntityTypeItalic or TextEntityTypeStrikethrough or TextEntityTypePre or TextEntityTypePreCode or TextEntityTypeUrl or TextEntityTypeBold or TextEntityTypeBotCommand or TextEntityTypeCashtag or TextEntityTypeEmailAddress or TextEntityTypeUnderline or TextEntityTypePhoneNumber or TextEntityTypeTextUrl or TextEntityTypeBankCardNumber or TextEntityTypeMentionName":
        if q.get("@type"):
            return Object.read(q)
        return TextEntityType()

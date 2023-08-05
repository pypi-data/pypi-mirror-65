

from ..utils import Object


class RichText(Object):
    """
    Describes a text object inside an instant-view web page

    No parameters required.
    """
    ID = "richText"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "RichTextAnchorLink or RichTextSubscript or RichTextIcon or RichTextReference or RichTextItalic or RichTextUrl or RichTextUnderline or RichTextPlain or RichTextStrikethrough or RichTextEmailAddress or RichTextSuperscript or RichTextPhoneNumber or RichTextAnchor or RichTexts or RichTextBold or RichTextFixed or RichTextMarked":
        if q.get("@type"):
            return Object.read(q)
        return RichText()

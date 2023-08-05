

from ..utils import Object


class PageBlock(Object):
    """
    Describes a block of an instant view web page

    No parameters required.
    """
    ID = "pageBlock"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "PageBlockAuthorDate or PageBlockTable or PageBlockMap or PageBlockVideo or PageBlockFooter or PageBlockTitle or PageBlockAudio or PageBlockDivider or PageBlockHeader or PageBlockSubtitle or PageBlockSubheader or PageBlockParagraph or PageBlockPhoto or PageBlockKicker or PageBlockEmbedded or PageBlockAnchor or PageBlockRelatedArticles or PageBlockList or PageBlockCover or PageBlockPreformatted or PageBlockBlockQuote or PageBlockPullQuote or PageBlockEmbeddedPost or PageBlockDetails or PageBlockAnimation or PageBlockSlideshow or PageBlockVoiceNote or PageBlockCollage or PageBlockChatLink":
        if q.get("@type"):
            return Object.read(q)
        return PageBlock()

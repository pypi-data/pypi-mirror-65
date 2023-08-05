

from ..utils import Object


class ChatReportReason(Object):
    """
    Describes the reason why a chat is reported

    No parameters required.
    """
    ID = "chatReportReason"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "ChatReportReasonChildAbuse or ChatReportReasonViolence or ChatReportReasonPornography or ChatReportReasonCopyright or ChatReportReasonSpam or ChatReportReasonCustom or ChatReportReasonUnrelatedLocation":
        if q.get("@type"):
            return Object.read(q)
        return ChatReportReason()

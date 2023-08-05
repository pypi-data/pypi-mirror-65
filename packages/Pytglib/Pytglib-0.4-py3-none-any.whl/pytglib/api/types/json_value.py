

from ..utils import Object


class JsonValue(Object):
    """
    Represents a JSON value

    No parameters required.
    """
    ID = "jsonValue"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "JsonValueArray or JsonValueNull or JsonValueBoolean or JsonValueObject or JsonValueNumber or JsonValueString":
        if q.get("@type"):
            return Object.read(q)
        return JsonValue()

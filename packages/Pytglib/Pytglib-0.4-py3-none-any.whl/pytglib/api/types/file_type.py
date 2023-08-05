

from ..utils import Object


class FileType(Object):
    """
    Represents the type of a file

    No parameters required.
    """
    ID = "fileType"

    def __init__(self, **kwargs):
        
        pass

    @staticmethod
    def read(q: dict, *args) -> "FileTypeUnknown or FileTypeSecret or FileTypeNone or FileTypeWallpaper or FileTypePhoto or FileTypeSecure or FileTypeAudio or FileTypeSecretThumbnail or FileTypeVideoNote or FileTypeDocument or FileTypeSticker or FileTypeProfilePhoto or FileTypeThumbnail or FileTypeVideo or FileTypeAnimation or FileTypeVoiceNote":
        if q.get("@type"):
            return Object.read(q)
        return FileType()

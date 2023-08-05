from typing import Optional

from fa_common import sizeof_fmt, CamelModel


# Shared properties
class File(CamelModel):
    size: str  # e.g. '3 KB'
    size_bytes: int
    url: Optional[str] = None  # download url
    id: str  # id can be path or database id
    dir: bool  # is current node dir?
    path: str  # path to current item (e.g. /folder1/someFile.txt)
    # optional (but we are using id as name if name is not present) (e.g. someFile.txt)
    name: Optional[str] = None
    content_type: Optional[str]

    def set_size(self, bytes: int):
        self.size = sizeof_fmt(bytes)
        self.size_bytes = bytes

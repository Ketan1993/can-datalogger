""""TRC file parser"""

import typing
import os
from typing import Any, Optional

#file type
FileLike = typing.Union[typing.TextIO]
#file Path Type
StrPathLike = typing.Union[str, "os.PathLike[str]"]
#Accept IO file type
AcceptIOType = typing.Union[FileLike, StrPathLike]

class BaseIOHandler():

    """
    File type like TextIO
    """
    file : typing.Union[typing.TextIO]

    def __init__(self, 
                 file: Optional[AcceptIOType], 
                 mode: str = "rt", **kwargs: Any):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type,
                 exc_val, exc_tb
                ) -> None:
        
        self.stop()
    
    def stop(self) -> None:
        if self.file is not None:
            self.file.close()


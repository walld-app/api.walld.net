'''dto classes for api'''
from pydantic import BaseModel
from pydantic import Optional


class Wall(BaseModel):
    '''represents wall from api point of view in dto for filtering purposes'''
    width: int
    height: int
    color: Optional[str]
    category: str
    sub_category: str
    file_name: str
    ratio: Optional[str]

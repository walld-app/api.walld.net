from pydentic import BaseModel 

class Wall(BaseModel):
    wall_id: int
    width: int
    height: int
    color: Optional[str]
    category: str
    sub_category: str
    file_name: str
    ratio: Optional[str]
    
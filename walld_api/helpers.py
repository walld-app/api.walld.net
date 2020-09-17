from walld_db.helpers import DB
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from pydantic import BaseModel
from typing import Optional, List

db = DB(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)


def get_cats_sub_cats() -> dict:
    d = {}
    cats = db.categories_objects
    for i in cats:
        d[i.name] = [l.name for l in i.sub_categories]
    return d


class ApiRequest(BaseModel):
    category: Optional[str]
    sub_category: Optional[str]
    tags: Optional[List[str]]
    colours: Optional[List[str]]


class ApiPicAnswer(BaseModel):
    id: int
    colours: List[str]
    source_url: str
    url: str

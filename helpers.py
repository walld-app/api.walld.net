from walld_db.helpers import DB
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


db = DB(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)


def get_cats_sub_cats() -> dict:
    d = {}
    cats = db.categories_objects
    for i in cats:
        d[i.category_name] = [l.sub_category_name for l in i.sub_categories]
    return d

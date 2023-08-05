from wallpaper_setter.utils.config import Config
from wallpaper_setter.db.connect import Database

def get_database():
    conf = Config()
    db = Database(conf.database_uri)
    return db

import pathlib
import toml
import os

class Config:
    database_uri = None
    image_extensions = []

    def __init__(self):
        home = os.getenv("HOME")
        if home == "":
            raise OSError("HOME not set")

        conf_locs = ['.config/wallpaper_setter', '.wallpaper_setter']
        conf_loc = None
        for cl in conf_locs:
            if pathlib.Path(home, cl).exists():
                conf_loc = pathlib.Path(home, cl, 'config.toml')
                break
        if conf_loc is None:
            raise Exception("No config folder found!")

        if conf_loc.exists():
            conf = toml.load(conf_loc)
            self.database_uri = conf["wallpaper_db"]
            self.image_extensions = conf["image_extensions"]
        else:
            raise Exception("No config file found!")

    @staticmethod
    def create_config(db_uri):
        home = os.getenv("HOME")
        if home == "":
            raise Exception("HOME not set")

        conf_loc = pathlib.Path(home, ".config/wallpaper_setter", "config.toml")
        conf_loc.parent.mkdir(parents=True, exist_ok=True)
        toml.dump({'wallpaper_db': db_uri, 'image_extensions': ['.jpg', '.jpeg', '.png']}, open(conf_loc, 'w'))
        return Config()

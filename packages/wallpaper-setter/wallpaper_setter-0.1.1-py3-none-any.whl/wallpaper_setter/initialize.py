import os
import pathlib
from datetime import datetime

import click
import pywal

from wallpaper_setter.utils.config import Config
from wallpaper_setter.db.connect import Database
from wallpaper_setter.db.models import Folder, Wallpaper

@click.command()
def initialize():
    # Try to get config
    conf = None
    try:
        conf = Config()
    except Exception as e:
        if click.confirm("No config found, would you like to create one?", default=True):
            uri = 'sqlite:///' + str(pathlib.Path(os.getcwd(), 'Wallpapers.db').as_posix())
            conf = Config.create_config(uri)
    except OSError as e:
        print("Path not set, please set PATH to continue")

    # Populate database with tables
    db = Database(conf.database_uri)
    db.create_tables()
    sess = db.get_session()

    # Trying to determine current wallpaper
    cur_wp = pathlib.Path(pywal.wallpaper.get())
    f_path = cur_wp.parent
    w_name = cur_wp.name

    print("The current wallpaper is: {}".format(cur_wp))
    if click.confirm("Do you want to add it?", default=True):
        f = sess.query(Folder).filter_by(path=str(f_path)).first()
        if f is None:
            f = Folder(path=str(f_path))
            sess.add(f)
        name = click.prompt("Name")

        w = Wallpaper(file_name=str(w_name), folder=f)
        if name:
            w.name = name
        w.current = True
        w.times_used = 1
        w.last_time = datetime.now()
        sess.add(w)
        sess.commit()

    print("Run `wpsetter update` to add all wallpapers in the folder of your wallpaper")

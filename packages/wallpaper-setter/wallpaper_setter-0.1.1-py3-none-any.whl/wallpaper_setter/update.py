import pathlib

import click

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.db.models import Wallpaper, Folder, Category
from wallpaper_setter.utils.config import Config

@click.command()
def update():
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except Exception as e:
        print("Failed to access database")
        print(e)
        return

    conf = None
    try:
        conf = Config()
    except:
        print("Failed to load config... Did you initialize")
        return
   
    # Check if registered folders still on drive
    fs = sess.query(Folder).all()
    for f in fs:
        if not pathlib.Path(f.path).exists():
            print("Folder {} not found, deleting...".format(f.path))
            sess.delete(f)

    # Check if current wallpapers are still on drive
    ws = sess.query(Wallpaper).all()
    for w in ws:
        if not pathlib.Path(w.folder.path, w.file_name).exists():
            print("{} does not exist, deleting...".format(w.file_name))
            sess.delete(w)

    # Check folders for new wallpapers
    for f in fs:
        for ext in conf.image_extensions:
            for fn in pathlib.Path(f.path).glob('*{}'.format(ext)):
                if f.wallpapers.filter_by(file_name=str(fn.name)).count() == 0:
                    if click.confirm("{} is not in the database, do you want to add it?".format(str(fn.name)), default=True):
                        name = click.prompt("Name", default="")
                        w = Wallpaper(file_name=str(fn.name), folder=f)
                        if name:
                            if len(sess.query(Wallpaper).filter_by(name=name).all()) == 0:
                                w.name = name
                            else:
                                print("Name {} already in use".format(name))
                                return
                        try:
                            sess.add(w)
                            sess.commit()
                            print("Added wallpaper to database")
                        except Exception as e:
                            print(e)

    # Check if wallpaper has name and category
    ws = sess.query(Wallpaper).all()
    cs = sess.query(Category).all()
    if len(cs) == 0:
        return
    for w in ws:
        if not w.name:
            if click.confirm("Wallpaper {} has no name, set it?".format(w.file_name), default=True):
                name = click.prompt("Name")
                if name:
                    if len(sess.query(Wallpaper).filter_by(name=name).all()) == 0:
                        w.name = name
                    else:
                        print("Name {} already in use".format(name))
                        return
        if not w.category:
            if click.confirm("Wallpaper {} has no category, set it?".format(w.name), default=True):
                category = click.prompt("Category", type=click.Choice([c.name for c in cs]), show_choices=True)
                w.category = sess.query(Category).filter_by(name=category).first()

    sess.commit()

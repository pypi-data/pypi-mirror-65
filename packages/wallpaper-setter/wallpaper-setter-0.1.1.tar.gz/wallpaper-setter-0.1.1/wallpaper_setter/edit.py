import click

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.db.models import Folder, Wallpaper, Category

@click.command('edit')
@click.argument('id')
@click.option("--name", default=None, help='New name for wallpaper')
@click.option("--category", default=None, help="Set category for wallpaper with category name")
def edit_wallpaper(id, name, category):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    w = sess.query(Wallpaper).filter_by(id=id).first()
    if w is None:
        print("Could not find wallpaper with id {}".format(id))
        return
    else:
        if name:
            w.name = name
        if category:
            c = sess.query(Category).filter_by(name=category).first()
            if c is None:
                print("Could not find category {}".format(category))
            else:
                w.category = c

    sess.commit()

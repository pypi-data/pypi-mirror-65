import click

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.db.models import Category

@click.command('toggle')
@click.argument('name')
def toggle_category(name):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    c = sess.query(Category).filter_by(name=name).first()
    if c is None:
        print("Could not find category {}".format(name))
        return
    else:
        c.active = not c.active
        print("Category {} is now {}".format(name, 'active' if c.active else 'inactive'))

    sess.commit()

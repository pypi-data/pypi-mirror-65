import click

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.db.models import Folder, Wallpaper

@click.group()
def delete():
    pass

@click.command('folder')
@click.argument('id')
def delete_folder(id):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    f = sess.query(Folder).filter_by(id=id).first()
    if click.confirm("Are you sure you want to delete '{}'?".format(f.path)):
        sess.delete(f)
        sess.commit()
        print("Deleted folder")

@click.command('wallpaper')
@click.option('--id', default=None, help="ID of the wallpaper to delete")
@click.option('--name', default=None, help="Name of the wallpaper to delete")
def delete_wallpaper(id, name):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return
    
    if id:
        w = sess.query(Wallpaper).filter_by(id=id).first()
        if click.confirm("Are you sure you want to delete '{}'?".format(w.file_name)):
            sess.delete(w)
            sess.commit()
            print("Deleted wallpaper")
    elif name:
        w = sess.query(Wallpaper).filter_by(name=name).first()
        if click.confirm("Are you sure you want to delete '{}'?".format(w.name)):
            sess.delete(w)
            sess.commit()
            print("Deleted wallpaper")
    else:
        print("Please use --id or --name. See --help for more info.")

delete.add_command(delete_folder)
delete.add_command(delete_wallpaper)

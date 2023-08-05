import click
import sqlalchemy.sql.functions as func

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.utils.table import get_table
from wallpaper_setter.db.models import Folder, Wallpaper, Category

@click.group('list')
def ls():
    pass

@click.command('folder')
def list_folder():
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    fs = sess.query(Folder).all()
    
    table = get_table()
    table.setData([{"ID": f.id, "Path": f.path, "No. wallpapers": f.wallpapers.count()} for f in fs])

    table.displayTable()

@click.command('wallpaper')
def list_wallpaper():
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    ws = sess.query(Wallpaper).all()
    total_use = sess.query(func.sum(Wallpaper.times_used)).first()[0]

    table = get_table()
    data = [{"ID": "{}{}".format(w.id, '*' if w.current else ''), 
        "Name": w.name, 
        "Category": w.category.name if w.category else "-",
        "Folder": w.folder.path, 
        "File Name": w.file_name,
        "Last": "-" if w.last_time is None else w.last_time.strftime("%a %d %b %Y %X")} for w in ws]
    if total_use != 0:
        for w, r in zip(ws, data):
            r["Usage %"] = "{:.0f}%".format(100 * w.times_used / total_use)

    table.setData(data)
    table.displayTable()

@click.command('category')
def list_category():
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return
    
    cs = sess.query(Category).all()
    table = get_table()
    table.setData([{"ID":"{}{}".format(c.id, '*' if c.active else ''),
        "Name": c.name,
        "No. wallpapers": c.wallpapers.count()} for c in cs])
    table.displayTable()

ls.add_command(list_folder)
ls.add_command(list_wallpaper)
ls.add_command(list_category)

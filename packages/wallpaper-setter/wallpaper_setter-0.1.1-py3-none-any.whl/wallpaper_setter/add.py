import pathlib

import click

from wallpaper_setter.db.connect import Database
from wallpaper_setter.db.models import Folder, Wallpaper, Category
from wallpaper_setter.utils.config import Config
from wallpaper_setter.utils.db import get_database

@click.group()
def add():
    pass

@click.command("folder")
@click.argument("path")
def add_folder(path):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except Exception as e:
        print(e)
        print("Failed to access database")
        return
    p = pathlib.Path(path).resolve()
    fs = sess.query(Folder).filter_by(path=str(p)).all()
    if len(fs) == 0: 
        f = Folder(path=str(p))
        try:
            sess.add(f)
            sess.commit()
            print("Added folder {} to database".format(p))
        except Exception as e:
            print(e)
        return f
    else:
        print("Folder {} already in database".format(p))
        return fs[0]

@click.command("wallpaper")
@click.argument("path")
@click.option("--name", default=None, help="Comprehensive name for wallpaper")
@click.option("--category", default=None, help="Name of the category for the wallpaper")
def add_wallpaper(path, name, category):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except Exception as e:
        print(e)
        print("Failed to access database")
        return
    p = pathlib.Path(path).resolve()

    # Lookup folder
    fs = sess.query(Folder).filter_by(path=str(p.parent)).all()
    f = None
    if len(fs) == 0:
        if click.confirm("Folder not in database, add?"):
            f = add_folder(p.parent)
        else:
            return
    else:
        f = fs[0]
    
    # Check if wallpaper is not already in database
    ws = sess.query(Wallpaper).filter_by(file_name=str(p.name)).filter_by(folder_id=f.id).all()
    if len(ws) == 0:
        w = Wallpaper(file_name=str(p.name), folder=f)
        if name:
            if len(sess.query(Wallpaper).filter_by(name=name).all()) == 0:
                w.name = name
            else:
                print("Name {} already in use".format(name))
                return
        if category:
            c = sess.query(Category).filter_by(name=category).first()
            if c is None:
                print("Category {} not found, not setting it to wallpaper")
            else:
                w.category = c
        try:
            sess.add(w)
            sess.commit()
            print("Added wallpaper to database")
        except Exception as e:
            print(e)
    else:
        print("Wallpaper already in database")

@click.command("category")
@click.argument("name")
def add_category(name):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    cs = sess.query(Category).filter_by(name=name).first()
    if cs is None:
        c = Category(name=name)
        sess.add(c)
        sess.commit()
    else:
        print("Category {} already in database".format(name))


add.add_command(add_folder)
add.add_command(add_wallpaper)
add.add_command(add_category)

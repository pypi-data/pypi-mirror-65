import pathlib
import random
from datetime import datetime

import click
from sqlalchemy.sql.expression import func

from wallpaper_setter.utils.db import get_database
from wallpaper_setter.utils.wallpaper import set_wallpaper
from wallpaper_setter.db.models import Folder, Wallpaper

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--id', default=None, help="ID of the wallpaper to set")
@click.option('--name', default=None, help="Name of the wallpaper to set")
def set(ctx, id, name):
    if ctx.invoked_subcommand is None:
        sess = None
        try:
            db = get_database()
            sess = db.get_session()
        except:
            print("Failed to access database")
            return
        
        if id:
            ws = sess.query(Wallpaper).filter_by(id=id).first()
            if ws is None:
                print("Couldn't find wallpaper with id: {}".format(id))
            else:
                print("Setting wallpaper")
                wo = sess.query(Wallpaper).filter_by(current=True).all()
                for w in wo:
                    w.current = False
                ws.current = True
                ws.times_used += 1
                ws.last_time = datetime.now()
                set_wallpaper(pathlib.Path(ws.folder.path, ws.file_name))
                sess.commit()
        elif name:
            ws = sess.query(Wallpaper).filter_by(name=name).first()
            if ws is None:
                print("Couldn't find wallpaper with name: {}".format(name))
            else:
                print("Setting wallpaper")
                wo = sess.query(Wallpaper).filter_by(current=True).all()
                for w in wo:
                    w.current = False
                ws.current = True
                ws.times_used += 1
                ws.last_time = datetime.now()
                set_wallpaper(pathlib.Path(ws.folder.path, ws.file_name))
                sess.commit()
        else:
            print("Use --id or --name. Use --help for more info.")


@click.command('next')
@click.option('--all', is_flag=True, help="Disregard inactive categories")
def set_next(all):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    cur = get_current(sess)
    if all:
        next_w = sess.query(Wallpaper).order_by(Wallpaper.id.asc()).filter(Wallpaper.id < cur.id).first()
        if next_w is None:
            next_w = sess.query(Wallpaper).order_by(Wallpaper.id.asc()).first()
    else:
        query = sess.query(Wallpaper).join(Wallpaper.category, aliased=True).filter_by(active=True)
        next_w = query.order_by(Wallpaper.id.asc()).filter(Wallpaper.id > cur.id).first()
        if next_w is None:
            next_w = query.order_by(Wallpaper.id.asc()).first()

    cur.current = False
    next_w.current = True
    next_w.times_used += 1
    next_w.last_time = datetime.now()
    set_wallpaper(pathlib.Path(next_w.folder.path, next_w.file_name))
    sess.commit()

@click.command('previous')
@click.option('--all', is_flag=True, help="Disregard inactive categories")
def set_prev(all):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    cur = get_current(sess)
    if all:
        previous = sess.query(Wallpaper).order_by(Wallpaper.id.desc()).filter(Wallpaper.id < cur.id).first()
        if previous is None:
            previous = sess.query(Wallpaper).order_by(Wallpaper.id.desc()).first()
    else:
        query = sess.query(Wallpaper).join(Wallpaper.category, aliased=True).filter_by(active=True)
        previous = query.order_by(Wallpaper.id.desc()).filter(Wallpaper.id < cur.id).first()
        if previous is None:
            previous = query.order_by(Wallpaper.id.desc()).first()

    cur.current = False
    previous.current = True
    previous.times_used += 1
    previous.last_time = datetime.now()
    set_wallpaper(pathlib.Path(previous.folder.path, previous.file_name))
    sess.commit()

@click.command('random')
@click.option('--all', is_flag=True, help="Disregard inactive categories")
def set_random(all):
    sess = None
    try:
        db = get_database()
        sess = db.get_session()
    except:
        print("Failed to access database")
        return

    cur = get_current(sess)
    query = None
    if all:
        query = sess.query(Wallpaper)
    else:
        query = sess.query(Wallpaper).join(Wallpaper.category, aliased=True).filter_by(active=True)

    offset = random.randrange(0, query.count() - 1)
    next_w = query.filter(Wallpaper.id != cur.id).offset(offset).first()

    cur.current = False
    next_w.current = True
    next_w.times_used += 1
    next_w.last_time = datetime.now()
    set_wallpaper(pathlib.Path(next_w.folder.path, next_w.file_name))
    sess.commit()
    
def get_current(sess):
    return sess.query(Wallpaper).filter_by(current=True).first()

set.add_command(set_next)
set.add_command(set_prev)
set.add_command(set_random)

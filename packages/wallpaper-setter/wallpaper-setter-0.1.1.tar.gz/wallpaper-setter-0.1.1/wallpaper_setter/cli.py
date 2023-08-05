import click

from wallpaper_setter.initialize import initialize
from wallpaper_setter.add import add
from wallpaper_setter.lst import ls
from wallpaper_setter.set import set
from wallpaper_setter.delete import delete
from wallpaper_setter.update import update
from wallpaper_setter.edit import edit_wallpaper
from wallpaper_setter.toggle import toggle_category

@click.group()
def cli():
    pass

cli.add_command(initialize)
cli.add_command(add)
cli.add_command(ls)
cli.add_command(set)
cli.add_command(delete)
cli.add_command(update)
cli.add_command(edit_wallpaper)
cli.add_command(toggle_category)

if __name__ == '__main__':
    cli()

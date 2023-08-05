import pywal

def set_wallpaper(path):
    image = pywal.image.get(path)
    colors = pywal.colors.get(image)
    pywal.sequences.send(colors)
    pywal.export.every(colors)
    pywal.reload.env()
    pywal.wallpaper.change(image)

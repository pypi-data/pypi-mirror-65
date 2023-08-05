import os
import shutil
import click
import PIL
from PIL import Image

FORMATS = [
    ".png",
    ".jpg",
]

def grayscale(src, dst):
    filename = src.lower()
    if filename.endswith(".png"):
        Image.open(src).convert("LA").save(dst)
    else:
        Image.open(src).convert("L").save(dst)

@click.group()
def grayscale_image_main():
    pass

@grayscale_image_main.command(name="file")
@click.argument("src_file", nargs=1, required=True)
@click.argument("dst_file", nargs=1, required=True)
def grayscale_file(src_file, dst_file):
    """Grayscale an image file.
    """
    src_file = os.path.abspath(src_file)
    dst_file = os.path.abspath(dst_file)
    try:
        grayscale(src_file, dst_file)
        print("{0} -> {1}".format(src_file, dst_file))
    except Exception as error:
        print("Grayscale image failed:", error)
        os.sys.exit(1)

@grayscale_image_main.command(name="folder")
@click.argument("src_root", nargs=1, required=True)
@click.argument("dst_root", nargs=1, required=True)
def grayscale_folder(src_root, dst_root):
    """Grayscale .png and .jpg images in a folder.
    """
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            src_filename = os.path.abspath(os.path.join(root, filename))
            related_filename = os.path.relpath(src_filename, src_root)
            dst_filename = os.path.abspath(os.path.join(dst_root, related_filename))
            os.makedirs(os.path.dirname(dst_filename), exist_ok=True)
            _, src_ext = os.path.splitext(src_filename)
            scaled = False
            if src_ext in FORMATS:
                try:
                    grayscale(src_filename, dst_filename)
                    scaled = True
                except Exception:
                    pass
            if not scaled:
                shutil.copyfile(src_filename, dst_filename)
            print("{0} -> {1}".format(src_filename, dst_filename))

if __name__ == "__main__":
    grayscale_image_main()

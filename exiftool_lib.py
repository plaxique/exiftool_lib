#! /cygdrive/c/anaconda3/python
import subprocess
import os
import pathlib
import IPython; debug_here=IPython.embed

#import sys
#sys.path.append("/cygdrive/c/Users/Asus ROG/Documents/Python Scripts/libs/pyexiftool")
from pyexiftool import exiftool

p = pathlib.Path(r"\\nas\photo\Sortiert\NiCa Anfang")
p_exiftool = pathlib.Path(r"/cygdrive/c/Users/Asus ROG/bin/exiftool")


def get_win_path(cyg_path):
    return subprocess.check_output(["cygpath", "-w", cyg_path]).strip(b"\n").decode()

p_exiftool2 = get_win_path('/cygdrive/c/Users/Asus ROG/bin/exiftool')

def get_exif_info(filename):
    exif_info_orig = subprocess.check_output([p_exiftool2, filename]).decode("utf-8").split('\r\n')

    # remove empty list elements
    exif_info = list(filter(None,exif_info_orig))

    exif_tags = [ele.split(": ")[0].strip() for ele in exif_info]
    exif_values = [ele.split(": ")[1].strip() for ele in exif_info]

    return dict(zip(exif_tags, exif_values))

exif_info = get_exif_info('P1110750.JPG')

#b = subprocess.run("ls {}".format(p), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#print(b.stdout.split('\n'))

os.chdir(p)
files = os.listdir()

#exiftool {} files[-1]

#with exiftool.ExifTool() as et:
#    metadata = et.get_metadata_batch(['P1110750.JPG'])



debug_here()



# 趣味のPython学習　Project 02-12
# Python RAW 2 TIFF CONVERTER
# ばーじょん 0.1.0

ver = "0.1.0"


# NEED THIS ! get 'pillow' with pip command !
from PIL import Image

# NEED THIS ! get 'numpy' with pip command !
import numpy

# NEED THIS ! get 'imageio' with pip command !
import imageio

# NEED THIS ! get 'rawpy' with pip command !
import rawpy as RPY
from rawpy import LibRawIOError

#
# IMPORTANT !!!
# rawpy needs LibRaw Libraly !
# https://www.libraw.org/
#

# MAIN

print(f"*** RAW FILE to TIFF CONVERTER VERSION {ver} ***")
print("\nSELECT RAW FILE\n")

while len( fnm := input("file : ") ) > 0 :

    try :

        raw = RPY.imread(fnm)

        width  = raw.sizes.width
        height = raw.sizes.height
        clr    = raw.color_desc
        pat    = raw.raw_pattern

        print(f"W : {width} H : {height}")

        print("PATTERN:",clr)
        print(pat)

        rgb = raw.postprocess(demosaic_algorithm=RPY.DemosaicAlgorithm.LINEAR,four_color_rgb=True,output_color=RPY.ColorSpace.raw,output_bps=16)

        print("*** READ OK ***")

    except LibRawIOError:
        print(f"{fnm} : not found !")

    except AssertionError:
        print(f"{fnm} : type error !")

    else :

        fno = fnm + ".tif"
        print(f"*** SAVE : {fno}  ( 48bit color ) ***")
        imageio.imsave(fno,rgb)

        if type(pat) != numpy.ndarray : continue

        fno = fnm + ".reb.png"
        print(f"*** SAVE : {fno} ( 16bit bayer pattern ) ***")

        img_cv = Image.new('I;16',(width,height))

        for y in range(height) :
            for x in range(width) :

                if x%2 == 0 and y%2 == 0 : c = pat[0][0]
                if x%2 == 1 and y%2 == 0 : c = pat[0][1]
                if x%2 == 0 and y%2 == 1 : c = pat[1][0]
                if x%2 == 1 and y%2 == 1 : c = pat[1][1]
                if c == 3 : c = 1

                img_cv.putpixel((x,y),int(rgb[y][x][c]))

        img_cv.save(fno)

        print("*** DONE ! ***")

# END OF FILE

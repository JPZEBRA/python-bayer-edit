# 趣味のPython学習　Project 02-11
# Python FITS DEBAYER
# ばーじょん 0.0.2

ver = "0.0.2"

from PIL import Image

import astropy.io.fits as fits

def getdata(data,a1,a2) :
    return data[a2][a1]

def adj(val,mi,mx,gm,ord) :
    return int(ord*(float(val-mi)/(mx-mi))**(1/gm))

def RGGB2x2(data,x,y) :

    red = getdata(data,(x>>1)*2 + 0,(y>>1)*2 + 0)
    gr1 = getdata(data,(x>>1)*2 + 1,(y>>1)*2 + 0)
    gr2 = getdata(data,(x>>1)*2 + 0,(y>>1)*2 + 1)
    blu = getdata(data,(x>>1)*2 + 1,(y>>1)*2 + 1)

    grn = (float(gr1)+float(gr2))/2

    return (red,grn,blu)

print(f"*** FITS DEBAYER PROGRAM VERSION:{ver} ***")
print("\nFOR SharpScan\n")
print("\nSELECT FITS FILE\n")
while len( fnm := input("file : ") ) > 0 :

    try :

        hdulist = fits.open(fnm)

        hdu = hdulist[0]
        data = hdu.data
        header = hdu.header

        axis = header["NAXIS"]

        assert(axis==2)

        col = 0

        ax1 = header["NAXIS1"]
        ax2 = header["NAXIS2"]

        wd = ax1
        ht = ax2

        print(f"AX1:{ax1} AX2:{ax2}")

    except FileNotFoundError:
        print(f"{fnm} : not found !")

    except AssertionError:
        print(f"{fnm} : type error !")

    else :

        print(f"{fnm} : read OK !")

        mi = 0xFFFFFFFF
        mx = 0x00000000
        av = 0

        for a1 in range(ax1) :
            for a2 in range(ax2) :
                dt = getdata(data,a1,a2)
                av = av + dt/ax1/ax2
                if dt < mi :
                    mi = dt
                if dt> mx :
                    mx = dt

        print(f"W:{wd} H:{ht}")
        print(f"MIN:{mi}")
        print(f"MAX:{mx}")
        print(f"AVE:{av}")

        if mi > 0.0 : mi = 0.0

        print("*** CONVERT MODE ***")

        while True :
            try :
                gm = float(input("GNM :"))
                if gm <= 0 : continue
                break
            except ValueError :
                continue

#       CONVERT DATA
        img_cv = Image.new('RGB',(wd,ht))

        for y in range(ht) :
            for x in range(wd) :
                dt = RGGB2x2(data,x,y)
                d0 = adj(dt[0],mi,mx,gm,255)
                d1 = adj(dt[1],mi,mx,gm,255)
                d2 = adj(dt[2],mi,mx,gm,255)
                img_cv.putpixel((x,ht-1-y),(d0,d1,d2))

        fno = fnm + ".dev.png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")

# END OF FILE

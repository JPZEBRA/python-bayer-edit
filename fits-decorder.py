# 趣味のPython学習　Project 02-10
# Python FITS DECODER
# ばーじょん 0.0.1

ver = "0.0.1"

from PIL import Image

import astropy.io.fits as fits

def getdata(data,a1,a2,a3,axis) :
    if axis == 2 :
        return data[a2][a1]
    return data[a3][a2][a1]

def adj(val,mi,mx,gm,ord) :
    return int(ord*(float(val-mi)/(mx-mi))**(1/gm))

print(f"*** FITS DECODE PROGRAM VERSION:{ver} ***")
print("\nSELECT FITS FILE\n")
while len( fnm := input("file : ") ) > 0 :

    try :

        hdulist = fits.open(fnm)

        hdu = hdulist[0]
        data = hdu.data
        header = hdu.header

        axis = header["NAXIS"]

        assert(axis>=2)

        col = 0

        if axis==2 :

            ax1 = header["NAXIS1"]
            ax2 = header["NAXIS2"]
            ax3 = 1

            wd = ax1
            ht = ax2

        if axis==3 :

            ax1 = header["NAXIS1"] 
            ax2 = header["NAXIS2"]
            ax3 = header["NAXIS3"]

            if ax1 == 3 :
                col = 1
                wd = ax2
                ht = ax3
            if ax2 == 3 :
                col = 2
                wd = ax1
                ht = ax3
            if ax3 == 3 :
                col = 3
                wd = ax1
                ht = ax2

            assert(col>0)
        assert(axis<=3)

        print(f"AX1:{ax1} AX2:{ax2} AX3:{ax3}")

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
                for a3 in range(ax3) :
                    dt = getdata(data,a1,a2,a3,axis)
                    av = av + dt
                    if dt < mi :
                        mi = dt
                    if dt> mx :
                        mx = dt

        av = av/ax1/ax2/ax3


        print(f"W:{wd} H:{ht}")
        print(f"MIN:{mi}")
        print(f"MAX:{mx}")
        print(f"AVE:{av}")

        print("*** CONVERT MODE ***")

        while True :
            try :
                gm = float(input("GNM :"))
                if gm <= 0 : continue
                break
            except ValueError :
                continue

#       CONVERT DATA
        if axis==2 : img_cv = Image.new('L',(wd,ht))
        if axis==3 : img_cv = Image.new('RGB',(wd,ht))

        for y in range(ht) :
            for x in range(wd) :
                if col == 0 :
                    dt = adj(getdata(data,x,y,0,2),mi,mx,gm,255)
                    img_cv.putpixel((x,ht-1-y),dt)
                if col == 1 :
                    d0 = adj(getdata(data,0,x,y,3),mi,mx,gm,255)
                    d1 = adj(getdata(data,1,x,y,3),mi,mx,gm,255)
                    d2 = adj(getdata(data,2,x,y,3),mi,mx,gm,255)
                    img_cv.putpixel((x,ht-1-y),(d0,d1,d2))
                if col == 2 :
                    d0 = adj(getdata(data,x,0,y,3),mi,mx,gm,255)
                    d1 = adj(getdata(data,x,1,y,3),mi,mx,gm,255)
                    d2 = adj(getdata(data,x,2,y,3),mi,mx,gm,255)
                    img_cv.putpixel((x,ht-1-y),(d0,d1,d2))
                if col == 3 :
                    d0 = adj(getdata(data,x,y,0,3),mi,mx,gm,255)
                    d1 = adj(getdata(data,x,y,1,3),mi,mx,gm,255)
                    d2 = adj(getdata(data,x,y,2,3),mi,mx,gm,255)
                    img_cv.putpixel((x,ht-1-y),(d0,d1,d2))

        fno = fnm + ".dcd.png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")

# END OF FILE

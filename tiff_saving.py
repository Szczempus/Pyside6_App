import os
import sys
import tifffile


def main():
    path = r"C:\Fotogrametria\!Lesnictwo\Analiza_Tuszyma\LAS017\BANDS.tif"
    image = tifffile.imread(path)
    print(image.pages[0])
    pass


if __name__ == "__main__":
    sys.exit(main())

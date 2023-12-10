from osgeo import gdal
import matplotlib.pyplot as plt

def plot_dem(path: str):

    dem: gdal.Dataset = gdal.Open(path)
    raster = dem.GetRasterBand(1).ReadAsArray()

    plt.figure()
    plt.imshow(raster)
    plt.colorbar()  
    plt.show()

if __name__ == "__main__":

    path = r"C:\Fotogrametria\!Lesnictwo\Analiza_Tuszyma\LAS018\DEM.tif"
    plot_dem(path)



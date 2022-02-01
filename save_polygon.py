from analysis import *


def save_polygon(index_map, polygon_list, analysis, debug=None):
    px = 1 / plt.rcParams['figure.dpi']
    if index_map.shape == 3:
        x_size, y_size, _ = index_map.shape
    else:
        x_size, y_size= index_map.shape

    if index_map is not None:

        fig, ax = plt.subplots(figsize=(x_size * px, y_size * px))
        if debug is None:
            plt.ioff()

        plot_image = plt.imshow(index_map, cmap=plt.get_cmap("Spectral"), vmin=0, vmax=1, resample=True)

        '''
        Loop over polygon list
        '''
        for polygon in polygon_list:

            if polygon["selected"]:
                # Getting coordinates and returning as list [x,y]
                coords = polygon["coordinates"]
                pts = [[int(coord["x"]), int(coord["y"])] for coord in coords]

                # Passing polygon points to matplotlib patches to crop generated plot
                patch = patches.Polygon(pts, closed=True, transform=ax.transData)
                plot_image.set_clip_path(patch)
                ax.axis('off')
                if debug is not None:
                    plt.show()

                # Passing to canva, drawing and converting as a numpy array
                canvas = FigureCanvasAgg(fig)
                canvas.draw()
                buf = canvas.buffer_rgba()
                x = np.asarray(buf)
                plt.imsave(analysis + polygon["name"] + ".png", x)

    else:
        raise TypeError("Nie można z tej mapy utworzyć analizy LCI")
        return 1

    return 0

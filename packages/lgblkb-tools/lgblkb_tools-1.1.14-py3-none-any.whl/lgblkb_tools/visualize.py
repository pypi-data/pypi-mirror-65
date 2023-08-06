import itertools as it
import matplotlib.pyplot as plt
from lgblkb_tools import logger, Folder
import numpy as np
import pandas as pd
import geopandas as gpd


class Plotter(object):
    def __init__(self, *images, **plot_kwargs):
        self.image_data = list()
        if images:
            self.add_images(*images).plot(**plot_kwargs)
        pass
    
    def add_image(self, image, **plot_kwargs):
        self.image_data.append(dict(image=image, plot_kwargs=plot_kwargs))
        return self
    
    def add_images(self, *images):
        for image in images:
            self.add_image(image)
        return self
    
    @staticmethod
    def get_grid_dims(images_count, nrows=None, ncols=None):
        col_count = np.sqrt(images_count * 16 / 9)
        if nrows is None:
            if ncols:
                nrows = max(1, np.ceil(images_count / ncols))
            else:
                nrows = max(1, np.round(images_count / col_count))
        if ncols is None:
            ncols = np.ceil(images_count / nrows)
        
        pair = list(map(int, [nrows, ncols]))
        # logger.debug('nrows,ncols for %s images: %s',images_count,pair)
        return pair
    
    def plot(self, show=True, overlay=False, **subplot_kwargs):
        if overlay:
            nrows, ncols = 1, 1
        else:
            nrows = subplot_kwargs.pop('nrows', None)
            ncols = subplot_kwargs.pop('ncols', None)
            nrows, ncols = self.get_grid_dims(len(self.image_data), nrows=nrows, ncols=ncols)
            if len(self.image_data) > nrows * ncols:
                raise ValueError(f'Insufficient number of axes ({nrows * ncols}) for {len(self.image_data)} images.')
        # logger.debug('nrows: %s',nrows)
        # logger.debug('ncols: %s',ncols)
        fig, axs = plt.subplots(nrows, ncols, **subplot_kwargs)
        if nrows * ncols == 1:
            axs = [axs]
        else:
            axs = axs.flatten()
        # logger.debug('len(axs): %s',len(axs))
        # logger.debug('len(self.image_data): %s',len(self.image_data))
        for ax, image_datum in it.zip_longest(axs, self.image_data, fillvalue=axs[0] if overlay else None):
            if image_datum is None:
                fig.delaxes(ax)
                continue
            image = image_datum['image']
            ax.imshow(image, **image_datum['plot_kwargs'])
        fig.set_size_inches(13, 8)
        
        if show:
            plt.tight_layout()
            plt.show()
        return self


def main():
    pass


if __name__ == '__main__':
    main()

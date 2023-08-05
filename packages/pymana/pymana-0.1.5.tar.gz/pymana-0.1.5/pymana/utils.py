import openslide
import openslide.deepzoom as deepzoom
import numpy as np
import dask
import dask.array as da
import dask_image.imread


def svs2dask_array(svs_file, tile_size=1000, overlap=0, remove_last=True, allow_unknown_chunksizes=False):
    """Convert SVS, TIF or TIFF to dask array.
    Parameters
    ----------
    svs_file : str
            Image file.
    tile_size : int
            Size of chunk to be read in.
    overlap : int
            Do not modify, overlap between neighboring tiles.
    remove_last : bool
            Remove last tile because it has a custom size.
    allow_unknown_chunksizes : bool
            Allow different chunk sizes, more flexible, but slowdown.
    Returns
    -------
    arr : dask.array.Array
            A Dask Array representing the contents of the image file.
    >>> arr = svs2dask_array(svs_file, tile_size=1000, overlap=0, remove_last=True, allow_unknown_chunksizes=False)
    >>> arr2 = arr.compute()
    >>> arr3 = to_pil(cv2.resize(arr2, dsize=(1440, 700), interpolation=cv2.INTER_CUBIC))
    >>> arr3.save(test_image_name)
    """
    # https://github.com/jlevy44/PathFlowAI/blob/master/pathflowai/utils.py
    img = openslide.open_slide(svs_file)
    if type(img) is openslide.OpenSlide:
        gen = deepzoom.DeepZoomGenerator(
            img, tile_size=tile_size, overlap=overlap, limit_bounds=True)
        max_level = len(gen.level_dimensions) - 1
        n_tiles_x, n_tiles_y = gen.level_tiles[max_level]

        @dask.delayed(pure=True)
        def get_tile(level, column, row):
            tile = gen.get_tile(level, (column, row))
            return np.array(tile).transpose((1, 0, 2))

        sample_tile_shape = get_tile(max_level, 0, 0).shape.compute()
        rows = range(n_tiles_y - (0 if not remove_last else 1))
        cols = range(n_tiles_x - (0 if not remove_last else 1))
        arr = da.concatenate([da.concatenate([da.from_delayed(get_tile(max_level, col, row), sample_tile_shape, np.uint8) for row in rows],
                                             allow_unknown_chunksizes=allow_unknown_chunksizes, axis=1) for col in cols], allow_unknown_chunksizes=allow_unknown_chunksizes).transpose([1, 0, 2])
        return arr
    else:  # img is instance of openslide.ImageSlide
        return dask_image.imread.imread(svs_file)
        # return dask.array.from_array(np.asarray(img.get_thumbnail(img.dimensions)))

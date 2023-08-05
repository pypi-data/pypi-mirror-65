import pymana.utils as utils
# from skimage.color import rgb2gray
from skimage.color import rgb2hed
from skimage.exposure import rescale_intensity
from skimage.util import invert
# from skimage.filters import gaussian, median
import dask
import numpy as np
from sympy import diff, solveset, Interval
from sympy.abc import s
import cv2
# from vispy.color import Colormap


def get_hematoxylin(rgb):
    """Run color deconvolution on an Aperio SVS image.

        Parameters
        ----------
        rgb
                A dask array representing the RGB image to be processed.
    """
    # matplotlib navy is (22, 0, 134), vispy navy is (0, 0, 128)
    # cmap_hema = Colormap(['white', 'navy'])

    # matplotlib saddlebrown is (144, 66, 0), vispy saddlebrown is (139, 69, 19)
    # cmap_dab = Colormap(['white', 'saddlebrown'])

    # matplotlib darkviolet is (166, 0, 218), vispy darkviolet is (148, 0, 211)
    # cmap_eosin = Colormap(['darkviolet', 'white'])

    ihc_hed = rgb2hed(rgb)
    arr_hema = ihc_hed[:, :, 0]
    return arr_hema


def candidate_thresholds(img):
    # convert image to grayscale (eliminate hue + saturation, retain luminance)
    @dask.delayed(pure=True)
    def get_grayscale(rgb):
        # grayscale = rgb2gray(rgb)
        grayscale = get_hematoxylin(rgb)
        grayscale = invert(rescale_intensity(grayscale, out_range=(0, 255)))
        # if a filter is used, grayscale should be:
        # rescale_intensity(invert(grayscale), out_range=(0, 255))
        # grayscale = median(grayscale)
        return grayscale
    grayscale = get_grayscale(img)

    # compute histogram
    N = 255
    h, bins = dask.array.histogram(grayscale, bins=np.arange(N + 1))
    histogram = dask.delayed(dict, pure=True)(
        dask.delayed(zip, pure=True)(bins, h))

    # compute progressive weighted mean (PWM_CURVE)
    @dask.delayed(pure=True)
    def calculate_pwm_curve(histogram):
        sum_wx, sum_w = [0], [histogram[0]]
        for P in range(1, N):
            sum_wx.append(sum_wx[P - 1] + histogram[P] * P)
            sum_w.append(sum_w[P - 1] + histogram[P])
        with np.errstate(divide='ignore', invalid='ignore'):
            pwm_curve = dict(
                zip(bins, np.nan_to_num(np.divide(sum_wx, sum_w))))
        return pwm_curve
    pwm_curve = calculate_pwm_curve(histogram)

    @dask.delayed(pure=True)
    def get_inflection_points(pwm_curve):
        # fit 15th order polynomial to PWM_CURVE
        coef = np.polynomial.polynomial.polyfit(
            list(pwm_curve.keys()), list(pwm_curve.values()), 15)
        # instead of the line under this, take a look at full param in polyfit
        function = sum(co * s**i for i, co in enumerate(coef))
        # some of these might not be inflection points:
        inflection_points = solveset(
            diff(diff(function)), domain=Interval(0, N))
        return list(inflection_points)
    inflection_points = get_inflection_points(pwm_curve)

    # return (grayscale image as Dask array, inflection points as list)
    return grayscale, inflection_points


def median_areas(image):
    # get candidate thresholds
    dask_gs, dask_thresholds = candidate_thresholds(image)

    # segment image for each candidate threshold
    @dask.delayed(pure=True)
    def calculate_stats_for_threshold(grayscale, threshold):
        # change to THRESH_BINARY_INV?
        _, binarized = cv2.threshold(
            np.uint8(grayscale), threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            np.uint8(binarized), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # find areas of objects for each segmented version
        areas = list(map(cv2.contourArea, contours))
        return [np.nanmedian(areas), binarized, contours, areas]
    out = {}
    # dask_thresholds must be computed because we need to iterate over it
    thresholds = dask_thresholds.compute()
    for threshold in thresholds:
        out[threshold] = calculate_stats_for_threshold(dask_gs, threshold)

    # return gs, {threshold: [median area, segmented img, contours, areas]}
    return dask_gs, out


def initial_threshold(image):
    dask_gs, dask_ima = median_areas(image)
    # needed to get max of delayed objects:
    img_median_areas = {key: value.compute()
                        for key, value in dask_ima.items()}

    @dask.delayed(nout=5, pure=True)
    def get_initial_threshold(median_areas):
        # get threshold with greatest median area
        img_initial_threshold = max(
            median_areas, key=lambda key: median_areas[key][0])

        median_area, img_segmented, contours, areas = median_areas[img_initial_threshold]
        return img_initial_threshold, median_area, img_segmented, contours, areas

    # return (gs, (initial threshold, median area, segmented img, contours, areas))
    return dask_gs, get_initial_threshold(img_median_areas)

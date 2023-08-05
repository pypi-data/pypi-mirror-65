import pymana.correction as correction
import numpy as np
import cv2
import dask
# from scipy import ndimage as ndi
# from skimage.segmentation import watershed
# from skimage.feature import peak_local_max


def separated(image):
    dask_gs, dask_threshold, dask_corrected_img = correction.corrected(
        image)

    @dask.delayed(pure=True)
    def expand_dimensions(grayscale):
        # the image is still grayscale but has 3 channels:
        return cv2.cvtColor(np.uint8(grayscale), cv2.COLOR_GRAY2BGR)
    img = expand_dimensions(dask_gs)

    @dask.delayed(nout=2, pure=True)
    def noise_removal(corrected):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(
            corrected, cv2.MORPH_OPEN, kernel, iterations=8)
        return kernel, opening
    kernel, opening = noise_removal(dask_corrected_img)

    @dask.delayed(pure=True)
    def get_background(opening, kernel):
        return cv2.dilate(opening, kernel, iterations=2)
    sure_bg = get_background(opening, kernel)

    @dask.delayed(nout=2, pure=True)
    def get_foreground(bg, threshold):
        dist_transform = cv2.distanceTransform(bg, cv2.DIST_L2, 5)
        _, fg_uncorrected = cv2.threshold(
            dist_transform, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            np.uint8(fg_uncorrected), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        mean_area = np.mean(list(map(cv2.contourArea, contours)))
        sure_fg = correction.correct_mask(
            correction.classify_contours(contours, mean_area), fg_uncorrected)
        return dist_transform, np.uint8(sure_fg)
    dist_transform, sure_fg = get_foreground(sure_bg, dask_threshold)

    @dask.delayed(pure=True)
    def get_unknown(bg, fg):
        return cv2.subtract(bg, fg)

    unknown = get_unknown(sure_bg, sure_fg)

    @dask.delayed(nout=2, pure=True)
    def marker_watershed(bgr, fg, unknown):
        # distance = ndi.distance_transform_edt(bgr)
        # local_maxima = peak_local_max(distance,
        #                               indices=False)
        # markers = ndi.label(local_maxima)[0]
        # labels = watershed(-distance, markers)
        # return markers, labels

        _, markers = cv2.connectedComponents(fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers += 1

        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0

        markers = cv2.watershed(bgr, markers)
        segmented = np.copy(bgr)
        segmented[markers == -1] = [255, 0, 0]

        return markers, segmented

    markers, segmented = marker_watershed(img, sure_fg, unknown)
    # segmented = marker_watershed(img, unknown)

    return sure_bg, sure_fg, dist_transform, unknown, segmented

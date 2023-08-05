import pymana.detection as detection
import dask
import numpy as np
import cv2


def classify_contours(contours, mean):
    small, medium, large = [], [], []
    for contour in contours:
        if cv2.contourArea(contour) <= 0.25 * mean:
            small.append(contour)
        elif cv2.contourArea(contour) > 5 * mean:
            large.append(contour)
        else:
            medium.append(contour)
    return {'small': small, 'medium': medium, 'large': large}


def correct_mask(classifications, binarized):
    small_contours = classifications['small']
    small_contour_mask = np.ones_like(binarized, dtype=np.uint8)
    for small_contour in small_contours:
        cv2.drawContours(small_contour_mask, [small_contour], -1, 0, -1)

    corrected_mask = cv2.bitwise_and(
        binarized, binarized, mask=small_contour_mask)
    return cv2.bitwise_not(corrected_mask)


def corrected(image):
    dask_gs, (dask_it, _, _, dask_contours, dask_areas) \
        = detection.initial_threshold(image)
    # paper does not mention if mean should be recalculated for each iteration
    initial_contours, areas = dask.compute(dask_contours, dask_areas)
    mean_area = np.mean(areas)
    classifications = classify_contours(initial_contours, mean_area)

    @dask.delayed(pure=True, nout=2)
    def correct_threshold(grayscale, initial_classifications, initial_threshold, initial_mean_area):
        corrected_threshold = initial_threshold
        classifications = initial_classifications
        np_gs = np.uint8(grayscale)
        mean_area = initial_mean_area

        def iterate(corrected_threshold):
            _, binarized = cv2.threshold(
                np_gs,
                corrected_threshold,
                255,
                cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(
                binarized, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # mean_area = np.mean(list(map(cv2.contourArea, contours)))
            classifications = classify_contours(contours, mean_area)
            return binarized, contours, classifications
        binarized, contours, classifications = iterate(corrected_threshold)
        while len(classifications['large']) > 0 and corrected_threshold > 1:
            # use Bayesian optimization to do this more efficiently
            corrected_threshold -= 1  # -1 just for testing
            binarized, contours, classifications = iterate(corrected_threshold)
        return corrected_threshold, binarized

    corrected_threshold, binarized = correct_threshold(
        dask_gs,
        classifications,
        dask_it,
        mean_area
    )

    corrected_mask = dask.delayed(correct_mask, pure=True)(
        classifications, binarized)

    return dask_gs, corrected_threshold, corrected_mask

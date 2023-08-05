#!/usr/bin/env python

import click
from click_aliases import ClickAliasedGroup
import dask
import napari
import numpy as np
import pprint
import pymana


@click.group(cls=ClickAliasedGroup)
@click.argument(u'image', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def cli(ctx, image):
    ctx.ensure_object(dict)
    ctx.obj['IMAGE'] = image


@cli.command()
@click.pass_context
def candidate_thresholds(ctx):
    # candidate-thresholds
    img = pymana.utils.svs2dask_array(ctx.obj['IMAGE'])[
                                      10000:12000, 10000:12000]
    dask_gs, dask_valid_thresholds = pymana.detection.candidate_thresholds(img)
    grayscale, valid_thresholds = dask.compute(dask_gs, dask_valid_thresholds)
    click.echo("Candidate thresholds: ")
    click.echo(pprint.pformat(valid_thresholds))
    with napari.gui_qt():
        _ = napari.view_image(np.uint8(grayscale),
                              name='grayscale',
                              rgb=False,
                              is_pyramid=False,
                              contrast_limits=[0, 255])
    return grayscale, valid_thresholds


@cli.command()
@click.pass_context
def median_areas(ctx):
    # median-areas
    img = pymana.utils.svs2dask_array(ctx.obj['IMAGE'])[
                                      10000:12000, 10000:12000]
    dask_gs, img_median_areas = pymana.detection.median_areas(img)
    median_areas_no_img = {key: value[0].compute()
                           for key, value in img_median_areas.items()}
    click.echo("Median object area for each candidate threshold: ")
    click.echo(pprint.pformat(median_areas_no_img))
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(np.uint8(dask_gs.compute()),
                         name='grayscale',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        for key, value in img_median_areas.items():
            viewer.add_image(np.uint8(value[1].compute()),
                             name=f'threshold = {key}',
                             rgb=False,
                             is_pyramid=False,
                             contrast_limits=[0, 255])

    return median_areas_no_img


@cli.command(aliases=['raw-nuclei-mask'])
@click.pass_context
def initial_threshold(ctx):
    # initial-threshold
    img = pymana.utils.svs2dask_array(ctx.obj['IMAGE'])[
                                      10000:12000, 10000:12000]
    dask_gs, (dask_it, dask_hma, dask_si, _, _) \
        = pymana.detection.initial_threshold(img)

    grayscale, img_initial_threshold, \
        highest_median_area, segmented_img = dask.compute(dask_gs, dask_it,
                                                          dask_hma, dask_si)
    click.echo("Initial threshold: ")
    click.echo(img_initial_threshold)
    click.echo("Median area for initial threshold: ")
    click.echo(highest_median_area)
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(np.uint8(grayscale),
                         name='grayscale',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(segmented_img,
                         name=f'threshold = {img_initial_threshold}',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
    return img_initial_threshold, highest_median_area, segmented_img


@cli.command()
@click.pass_context
def area_based_corrected(ctx):
    # area-based-corrected
    img = pymana.utils.svs2dask_array(ctx.obj['IMAGE'])[
                                      10000:12000, 10000:12000]
    dask_gs, dask_threshold, dask_is = pymana.correction.corrected(img)
    grayscale, threshold, img_segmented = dask.compute(
        dask_gs, dask_threshold, dask_is)
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(np.uint8(grayscale),
                         name='grayscale',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(img_segmented,
                         name=f'threshold = {threshold}',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])


@cli.command()
@click.pass_context
def nuclei_separated(ctx):
    # nuclei-separated
    img = pymana.utils.svs2dask_array(ctx.obj['IMAGE'])[
                                      10000:12000, 10000:12000]
    dask_bg, dask_fg, dask_dt, dask_unknown, dask_corrected \
        = pymana.separation.separated(img)
    bg, fg, dist_transform, unknown, corrected_img = dask.compute(
        dask_bg,
        dask_fg,
        dask_dt,
        dask_unknown,
        dask_corrected)
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(bg,
                         name='background',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(fg,
                         name='foreground',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(dist_transform,
                         name='dist_transform',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(unknown,
                         name='unknown',
                         rgb=False,
                         is_pyramid=False,
                         contrast_limits=[0, 255])
        viewer.add_image(corrected_img,
                         name='final',
                         rgb=True,
                         is_pyramid=False,
                         contrast_limits=[0, 255])


if __name__ == '__main__':
    cli()

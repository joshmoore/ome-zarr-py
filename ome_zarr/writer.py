"""Image writer utility

"""
import logging
from typing import Any, List, Tuple, Union

import numpy as np
import zarr

from .scale import Scaler
from .types import JSONDict

LOGGER = logging.getLogger("ome_zarr.writer")


def write_multiscale(
    pyramid: List, group: zarr.Group, chunks: Union[Tuple[Any, ...], int] = None,
) -> None:
    """Write a pyramid with multiscale metadata to disk."""
    paths = []
    for path, dataset in enumerate(pyramid):
        # TODO: chunks here could be different per layer
        group.create_dataset(str(path), data=pyramid[path], chunks=chunks)
        paths.append({"path": str(path)})

    multiscales = [{"version": "0.1", "datasets": paths}]
    group.attrs["multiscales"] = multiscales


def write_image(
    image: Union[np.ndarray, List[np.ndarray]],
    group: zarr.Group,
    chunks: Union[Tuple[Any, ...], int] = None,
    byte_order: Union[str, List[str]] = "tczyx",
    scaler: Scaler = Scaler(),
    **metadata: JSONDict,
) -> None:
    """Writes an image to the zarr store according to ome-zarr specification

    Parameters
    ----------
    image: np.ndarray or list of np.ndarrays
      the image data to save. A downsampling of the data can be pre-computed
      in which case the scaler argument will be ignored.
    group: zarr.Group
      the group within the zarr store to store the data in
    chunks: int or tuple of ints,
      size of the saved chunks to store the image
    byte_order: str or list of str, default "tczyx"
      combination of the letters defining the order
      in which the dimensions are saved
    scaler: Scaler
      Scaler implementation for downsampling the image argument. If None,
      no downsampling will be performed and the image argument will be passed
      directly to the write_multiscale method.
    """

    if image.ndim > 5:
        raise ValueError("Only images of 5D or less are supported")

    shape_5d: Tuple[Any, ...] = (*(1,) * (5 - image.ndim), *image.shape)
    image = image.reshape(shape_5d)

    if chunks is not None:
        chunks = _retuple(chunks, shape_5d)

    needs_scaling = True
    if isinstance(image, list):
        needs_scaling = True

    if scaler is not None:
        if not needs_scaling:
            LOGGER.debug("skipping scaling")
        else:
            image = scaler.nearest(image)
    else:
        if needs_scaling:
            LOGGER.debug("disabling pyramid")
            image = [image]

    write_multiscale(image, group, chunks=chunks)
    group.attrs.update(metadata)


def _retuple(
    chunks: Union[Tuple[Any, ...], int], shape: Tuple[Any, ...]
) -> Tuple[Any, ...]:

    _chunks: Tuple[Any, ...]
    if isinstance(chunks, int):
        _chunks = (chunks,)
    else:
        _chunks = chunks

    return (*shape[: (5 - len(_chunks))], *_chunks)

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
    image: np.ndarray,
    group: zarr.Group,
    chunks: Union[Tuple[Any, ...], int] = None,
    byte_order: Union[str, List[str]] = "tczyx",
    scaler: Scaler = None,
    **metadata: JSONDict,
) -> None:
    """Writes an image to the zarr store according to ome-zarr specification

    Parameters
    ----------
    image: np.ndarray
      the image to save
    group: zarr.Group
      the group within the zarr store to store the data in
    chunks: int or tuple of ints,
      size of the saved chunks to store the image
    byte_order: str or list of str, default "tczyx"
      combination of the letters defining the order
      in which the dimensions are saved
    """

    if image.ndim > 5:
        raise ValueError("Only images of 5D or less are supported")

    shape_5d: Tuple[Any, ...] = (*(1,) * (5 - image.ndim), *image.shape)
    image = image.reshape(shape_5d)

    if chunks is not None:
        chunks = _retuple(chunks, shape_5d)

    if scaler is None:
        scaler = Scaler()

    pyramid = scaler.nearest(image)
    write_multiscale(pyramid, group, chunks=chunks)
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

===========
ome-zarr-py
===========

Experimental implementation of images in Zarr files.

----

The `napari`_ plugin was generated with `Cookiecutter`_ along with `@napari`_'s `cookiecutter-napari-plugin`_ template.


Features
--------

* TODO


Requirements
------------

* TODO


Installation
------------

Install developer mode::

    cd ome-zarr-py
    pip install -e .


Usage
-----

Open images based on their ID in the Image Data Resource.

NB: Only select images are available currently.

For example ID = 9822151 or 6001240.

E.g. to open Image at http://idr.openmicroscopy.org/webclient/?show=image-6001240::


    $ napari 'https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/6001240.zarr/'


OR in python::

    import napari
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.open('https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/6001240.zarr/')


License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
"ome-zarr-py" is free and open source software


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@napari`: https://github.com/napari
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`Mozilla Public License 2.0`: https://www.mozilla.org/media/MPL/2.0/index.txt
.. _`cookiecutter-napari-plugin`: https://github.com/napari/cookiecutter-napari-plugin
.. _`napari`: https://github.com/napari/napari

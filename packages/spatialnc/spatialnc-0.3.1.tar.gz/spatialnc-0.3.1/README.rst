=========
spatialnc
=========


.. image:: https://img.shields.io/pypi/v/spatialnc.svg
        :target: https://pypi.python.org/pypi/spatialnc


Python library for handling spatial data in netcdfs specifically for modeling
using SMRF/AWSM.


* Free software: MIT license
* Documentation: https://spatialnc.readthedocs.io.


Features
--------

* IPW class - Python interface for opening files created by the Image Processing Workbench
* Netcdf Manipulation - A topo class for managing non-time dependent data in netcdf form.
* Netcdf Projections - Capable of adding UTM projection information to Netcdf so they can be read in by GDAL, QGIS, and other platforms
* NetCDF analysis

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

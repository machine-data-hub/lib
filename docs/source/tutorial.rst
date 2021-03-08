Tutorial
========

Basic Commands to use machine-data-hub below.

To Begin
--------
First, install the library::

    pip install machine-data-hub

Commands
--------

View All Datasets
^^^^^^^^^^^^^^^^^
Machine Data Hub allows you to view a library of reliable and
useful machine related datasets. To view all datasets::

    $ mdh list

Get Metadata
^^^^^^^^^^^^
If you want to know more about a dataset, you can view metadata
such as ML Type, if it's a time series, if it's labeled, and much
more. To view a dataset's metadata::

    $ mdh metadata 'Dataset Name Goes Here'

Download a Dataset
^^^^^^^^^^^^^^^^^^
If you find a dataset that you like and want to use for your project,
you can download it. To download a dataset::

    $ mdh download 'Dataset Name Goes Here'

Suggest a Dataset
^^^^^^^^^^^^^^^^^
Do you know a great dataset that could be useful for prognostics or
other machine related projects? Suggest it be added to the Machine Data
Hub's library of datasets::

    $ mdh suggest


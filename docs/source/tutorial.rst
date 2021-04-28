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

This will list out the dataset ID, name, and number of files for each dataset.

Get Metadata
^^^^^^^^^^^^
If you want to know more about a dataset, you can view metadata
such as ML Type, if it's a time series, if it's labeled, and much
more. To view a dataset's metadata::

    $ mdh metadata {id}

Example to view metadata for dataset with ID of 2::

    $ mdh metadata 2

Download a Dataset
^^^^^^^^^^^^^^^^^^
If you find a dataset that you like and want to use for your project,
you can download it. To download a full dataset::

    $ mdh download {id}

If the dataset has multiple files, you can just download one of the files at once.
To download one specific file in a dataset::

    $ mdh download {id} {file number}

Example to download file 1 from dataset 15::

    $ mdh download 15 1

Suggest a Dataset
^^^^^^^^^^^^^^^^^
Do you know a great dataset that could be useful for prognostics or
other machine related projects? Suggest it be added to the Machine Data
Hub's library of datasets::

    $ mdh suggest {link} {name} {summary}

Example to download file 1 from dataset 15::

    $ mdh suggest "www.data.com" "Dataset" "This is a summary"

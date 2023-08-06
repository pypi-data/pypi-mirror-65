DataMart Python Wrapper for the REST API
========================================

Datamart provides both a Python API and a REST API. This is a wrapper which exposes the REST API as the Python one, for use by clients which don't have Datamart locally available, or with Datamart systems that use REST natively (such as NYU's).

See also the `REST API documentation <https://datadrivendiscovery.gitlab.io/datamart-api/rest_api.html>`__.

How to install?
---------------

::

    $ pip install datamart-rest

How to use?
-----------

We provide an example using the `NY Taxi Demand data <https://gitlab.datadrivendiscovery.org/d3m/datasets/tree/master/seed_datasets_data_augmentation/DA_ny_taxi_demand/DA_ny_taxi_demand_dataset>`__. The example is available `here <examples/ny-taxi-demand.ipynb>`__.

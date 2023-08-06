=============================
dj-chartjs
=============================

Documentation
-------------

The full documentation is at https://django-charts.readthedocs.io/en/latest/

Quickstart
----------

Install dj-chartjs::

    pip install dj-chartjs

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_chartjs',
        ...
    )

**PS: You need define jquery and chartjs libraries in your html section script**

.. code-block:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.0/jquery.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox



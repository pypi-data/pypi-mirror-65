=============================
django-charts
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

How to render chart as a View:

in views.py import type chart to want use:

.. code-block:: python

    from django.views.generic.base import TemplateView
    from django_charts.views import BarChartView

    class ExampleChart(BarChartView, TemplateView):
        ...
        title = "Index of ..."
        id_chart = "barchart_example" #any value

        def generate_labels(self):
            return ["Africa","Brazil","Japan","EUA"]

        def generate_values(self):
            return [1,10,15,8]

in your template that you want render chart, use this tag:

{% load dj_chartjs %}


{% render_chart chart %}




Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox



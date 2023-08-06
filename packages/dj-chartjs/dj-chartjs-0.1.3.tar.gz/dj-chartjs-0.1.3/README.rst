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

**PS: You need define jquery and chartjs libraries in your html section script**

.. code-block:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.0/jquery.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>

**How to render chart as a View:**

Available BarChartView, PieChartView, DoughnutChartView, RadarChartView, HorizontalBarChartView, PolarAreaChartView

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

.. code-block:: html

    {% load dj_chartjs %}
    <html>
    <head></head>
    <body>

    {% render_chart chart %}

    </body>
    </html>

**How to use multiples charts as objects**

in your views.py:

.. code-block:: python

    from django.views.generic import TemplateView
    from dj_chartjs.charts import BarChart

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            barchart = BarChart()
            barchart.title = "Example charts title"

            labels = ["test 1","test 2", "test 3", "test 4"]
            data = [2,3,10,6]
            label = "Test"

            context["chart"] = barchart.generate_dataset(labels, data, label)
            return context

And in your "example.html" template use this:

<canvas id="mychart"></canvas>

on script section:

.. code-block:: javascript

    $(function(){
        new Chart(document.getElementById("mychart"), {
            type: "{{ chart.type }}",
            data: {{ chart.data|safe }},
            options: {{ chart.options|safe }}
        });
    })

**You can be use chart object in any function in your views.py, for example:**

.. code-block:: python

    class ExampleView(TemplateView):

        template_name = "core/example.html"

        def my_method(self):
            barchart = BarChart()
            barchart.title = "Example charts title"

            labels = ["test 1","test 2", "test 3", "test 4"]
            data = [2,3,10,6]
            label = "Test"

            return barchart.generate_dataset(labels, data, label)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["chart"] = self.my_method() #any key in context

            return context


The charts available in package is: BarChart, PieChart, HorizontalBarChart, DoughnutChart, PolarAreaChart, RadarChart, LineChart, GroupChart

It's possible define options to object chart, for example:

| barchart.title = "..."
| barchart.legend = True



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



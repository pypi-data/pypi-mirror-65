from django.test import TestCase

from dj_chartjs.charts import BarChart


class ContextTestCase(TestCase):
    def test_barchart_context(self):
        barchart = BarChart()
        barchart.title = "Test title chart"
        labels = ["test1", "test2", "test3", "test4"]
        data = [5, 18, 6, 20]
        context = barchart.generate_dataset(labels, data, "Test")

        self.assertIn("data", context)
        self.assertIn("options", context)

import json
import random
from abc import ABC, abstractmethod


"""
    Objects represent chartjs instances
"""


class ChartMixin(ABC):

    beginAtZero = True
    aspectRatio = True
    title = None
    legend = False
    type_chart = None
    _colors = None

    @abstractmethod
    def generate_dataset(self):
        pass

    def generate_options(self):
        return {
            "responsive": True,
            "maintainAspectRatio": self.aspectRatio,
            "legend": {"display": self.legend},
            "title": {
                "fontSize": 14,
                "display": True if self.title is not None else False,
                "text": self.title if self.title is not None else "",
            },
        }

    def _generate_colors(self, labels):
        return ["#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))) for entry in labels]

    def set_colors(self,colors):
        self._colors = colors

    def _get_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda x: random.randint(0, 255), range(3))
        )

    def _get_rgba_from_hex(self, color_hex):
        color = color.lstrip("#")
        rgb = [int(color[i : i + 2], 16) for i in [0, 2, 4]]

        return "rgba({},{},{},0.4)".format(*map(lambda x: x, rgb))


class BarChart(ChartMixin):

    type_chart = "bar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": 1},
                }
            ]
        }
        return options

    def generate_dataset(self, labels, data, dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": dataLabel if dataLabel is not None else "",
                    "backgroundColor": self._colors if self._colors is not None else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }


class HorizontalBarChart(ChartMixin):

    type_chart = "horizontalBar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "xAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": 1},
                }
            ]
        }
        return options

    def generate_dataset(self, labels, data, dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": dataLabel if dataLabel is not None else "",
                    "backgroundColor": self._colors if self._colors is not None else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }


class PieChart(ChartMixin):
    type_chart = "pie"

    def generate_options(self):
        context = super().generate_options()
        context["legend"] = {"position": "right"}
        return context

    def generate_dataset(self, labels, data, dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": dataLabel if dataLabel is not None else "",
                    "backgroundColor": self._colors if self._colors is not None else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }


class DoughnutChart(PieChart):
    type_chart = "doughnut"


class PolarAreaChart(PieChart):
    type_chart = "polarArea"


class LineChart(ChartMixin):
    
    type_chart = "line"

    def create_node(self, data, label, fill=False, color=None):
        colorData = color if color is not None else self._get_color()
        return {
            "data": list(data),
            "label": label,
            "backgroundColor": self._get_rgba_from_hex(colorData),
            "borderColor": colorData,
            "fill": fill,
        }

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": 1},
                }
            ]
        }
        return options

    def generate_dataset(self, data, labels):
        dataset = {"labels": labels, "datasets": data}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }


class GroupChart(ChartMixin):
    type_chart = "bar"

    def create_node(self, data, label, color=None):
        colorData = color if color is not None else self._get_color()
        return {
            "label": label,
            "backgroundColor": colorData,
            "data": list(data),
        }

    def generate_dataset(self, labels, data):
        dataset = {"labels": list(labels), "datasets": list(data)}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }


class RadarChart(ChartMixin):

    type_chart = "radar"

    def create_node(self, label, data, color=None):
        colorData = color if color is not None else self._get_rgba_from_hex(color)
        return {
            "label": label,
            "fill": True,
            "backgroundColor": colorData,
            "borderColor": color,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": color,
            "data": list(data),
        }


    def generate_dataset(self, labels, data):
        dataset = {"labels": list(labels), "datasets": list(data)}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options()),
        }

import json
import random
from abc import ABC, abstractmethod

'''
    Objects represent chartjs instances
'''
class ChartMixin(ABC):
    beginAtZero = True
    aspectRatio = False
    title = None
    legend = False
    type_chart = None

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
                "text": self.title if self.title is not None else ""
            }
        }


class BarChart(ChartMixin):

    type_chart = "bar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [{
                "display": True,
                "ticks": {
                    "beginAtZero": self.beginAtZero,
                    "stepSize": 1
                }
            }],
        }
        return options

    def generate_dataset(self,labels,data,dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [{
                "label": dataLabel if dataLabel is not None else "",
                "backgroundColor": ["#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))) for entry in labels],
                "data": list(data)
            }]
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }

class HorizontalBarChart(ChartMixin):

    type_chart = "horizontalBar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "xAxes": [{
                "display": True,
                "ticks": {
                    "beginAtZero": self.beginAtZero,
                    "stepSize": 1
                }
            }],
        }
        return options

    def generate_dataset(self,labels,data,dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [{
                "label": dataLabel if dataLabel is not None else "",
                "backgroundColor": ["#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))) for entry in labels],
                "data": list(data)
            }]
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }


class PieChart(ChartMixin):
    type_chart = "pie"

    def generate_options(self):
        context = super().generate_options()
        context["legend"] = {
            "position": "right"
        }
        return context

    def generate_dataset(self,labels,data,dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [{
                "label": dataLabel if dataLabel is not None else "",
                "backgroundColor": ["#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))) for entry in labels],
                "data": list(data)
            }]
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }

class DoughnutChart(PieChart):
    type_chart = "doughnut"

class PolarChart(PieChart):
    type_chart = "polarArea"

class LineChart(ChartMixin):
    type_chart = "line"
    _dataset = []

    def create_node(self,data,label,fill=False):
        return {
            "data": list(data),
            "label": label,
            "borderColor": "#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))),
            "fill": fill
        }

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [{
                "display": True,
                "ticks": {
                    "beginAtZero": self.beginAtZero,
                    "stepSize": 1
                }
            }],
        }
        return options

    def generate_dataset(self,data,labels):
        dataset = { 
            "labels": labels,
            "datasets": data
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }
        

class GroupChart(ChartMixin):
    type_chart = "bar"

    def create_node(self,data,label):
        return {
            "label": label,
            "backgroundColor": "#{:02x}{:02x}{:02x}".format(*map(lambda x: random.randint(0, 255), range(3))),
            "data": list(data)
        }
        
    def generate_dataset(self,labels,data):
        dataset = { 
            "labels": list(labels),
            "datasets": list(data)
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }

class RadarChart(ChartMixin):
    
    type_chart = "radar"

    def create_node(self,label,data):
        color = self._get_color()
        return {
            "label": label,
            "fill": True,
            "backgroundColor": color,
            "borderColor": color,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": color,
            "data": list(data)
        }
    
    def _get_color(self):
        return "rgba({},{},{},0.4)".format(
            *map(lambda x: random.randint(0, 255), range(5))
        )

    def generate_dataset(self,labels,data):
        dataset = { 
            "labels": list(labels),
            "datasets": list(data)
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset),
            "options": json.dumps(self.generate_options())
        }
from django import template

register = template.Library()


@register.inclusion_tag("dj_chartjs/chart.html", takes_context=True)
def render_chart(context, values):
    chart = {
        "chart": values,
        "type_chart": context["type"],
        "width": context.get("width"),
        "height": context.get("height"),
    }

    return chart

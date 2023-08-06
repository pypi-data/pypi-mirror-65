from django import template

register = template.Library()

@register.inclusion_tag("dj_chartjs/chart.html", takes_context=True)
def render_chart(context,values):
    chart = {
        "chart": values,
        "type_chart": context["type"],
    }
    if context.get("legend"):
        chart["legend_text"] = context.get("legend")
        
    return chart
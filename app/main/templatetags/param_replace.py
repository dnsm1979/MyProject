from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Возвращает параметры URL с обновленными значениями
    """
    params = context['request'].GET.copy()
    for key, value in kwargs.items():
        params[key] = value
    return params.urlencode()
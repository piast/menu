
from django import template

register = template.Library()


@register.inclusion_tag('tree_menu/tags/item.html', takes_context=True)
def draw_item(context, item):
    context.update({'item': item})
    return context
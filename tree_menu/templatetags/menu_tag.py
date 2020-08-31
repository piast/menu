from django import template

from tree_menu.models import Menu, MenuItem

register = template.Library()



# build a hierarchical tree from lists
def create_hierarchical_tree_list(items, item=None):
    tree_list = []
    if item:
        for child in items:
            if child.get('parent_id') == item.get('id'):
                tree_list.append(child)
                childs = create_hierarchical_tree_list(items, child)
                if childs:
                    tree_list.append(childs)
        return tree_list
    else:
        for child in items:
            if not child.get('parent_id'):
                tree_list.append(child)
                childs = create_hierarchical_tree_list(items, child)
                if childs:
                    tree_list.append(childs)
        return tree_list




def add_children(items, item=None):
    childs = []
    if item:
        for child in items:
            if child.get('parent_id') == item.get('id'):
                childs.append(child)
                add_children(items, child)
        item['childs'] = childs
    else:
        for child in items:
            if not child.get('parent_id'):
                add_children(items, child)


def mark_as_colapsed_or_not(items, context_full_path):
    is_active_present = False
    for item in items:
        item['is_active'] = False
        item['is_opend'] = False

        item_url = item.get('url') if item.get('url') else item.get('named_url')
        if item_url == context_full_path:
            item['is_active'] = True
            is_active_present = True

    if is_active_present:
        is_reached = False
        for item in items:
            if not item.get('is_active') and not is_reached:
                item['is_opend'] = True

            elif item.get('is_active') and not is_reached:
                is_reached = True
                item['is_opend'] = True

            elif not item.get('is_active') and is_reached and item.get('level')==0:
                item['is_opend'] = True



def flatten(items):
    for x in items:
        if isinstance(x, list):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x



@register.inclusion_tag('tree_menu/tags/menu.html', takes_context=True)
def draw_menu(context, slug):

    items = MenuItem.objects.filter(menu__slug=slug).select_related('menu').order_by('position').values(
        'menu__slug', "menu__title", "menu_id", "id", "parent_id", "title", "url", "named_url", "level", "position")

    items = create_hierarchical_tree_list(items)
    items = list(flatten(items))
    add_children(items)
    mark_as_colapsed_or_not(items, context.request.get_full_path())

    context.update({'items': items, 'slug': slug})
    return context

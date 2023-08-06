from django import template

register = template.Library()


@register.filter('get_item')
def get_item(obj, attr):
    return obj.__getitem__(attr)


@register.filter('get_attr')
def get_attribute(obj, attr):
    return getattr(obj, attr, False)


@register.filter('sub')
def sub(value, mount):
    try:
        return value - mount
    except:
        return 0


@register.filter('get_index')
def get_index(arr, index):
    if index not in arr:
        return False
    return arr[index]

from django import template

register = template.Library()
default_image = '/media/default.png'


@register.filter
def my_media_filter(val):
    if val:
        return f"/media/{val}"
    return default_image


@register.simple_tag
def my_media_tag(val):
    if val:
        return f"/media/{val}"
    return default_image


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    """
    Checks if a user is in a group.
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

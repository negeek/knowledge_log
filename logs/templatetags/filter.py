from django import template

register = template.Library()


@register.filter
def key(value, arg):
    if int(value[arg]) < 1:
        return 'No entries'
    elif int(value[arg]) < 2:
        return "1 entry"
    else:
        return str(value[arg])+' entries'

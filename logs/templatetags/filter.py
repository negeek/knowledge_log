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


@register.filter
def len_entries(value):
    ans = value.entry_set.count()
    if ans < 1:
        return 'No entries'
    elif ans < 2:
        return "1 entry"
    else:
        return str(ans)+' entries'

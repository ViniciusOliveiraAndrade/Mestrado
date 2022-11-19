from django import template

register = template.Library()

@register.filter
def get_dic_value(dic, key):
    return dic[key]

@register.filter
def get_first_dic_value(dic, key):
    return (dic[key][0] if len(dic[key]) > 0 else "No recommendation")


register.filter('get_dic_value', get_dic_value)
register.filter('get_first_dic_value', get_first_dic_value)


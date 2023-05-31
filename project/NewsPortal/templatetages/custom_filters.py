from django import template

register = template.Library()

@register.filter()
def censor(value):
    bad_words = ['bad','angry','awful']
    for i in bad_words:
        if i.find(value):
            value = value.replace(i[1::], "*" * len(i))
    return f'{value}'
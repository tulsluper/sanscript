from django.utils.safestring import mark_safe

from django import template
register = template.Library()


@register.filter
def lookup(d, key):
    return d[int(key)]


import string
@register.filter
def upperbreak(word):
    for letter in word[1:]:
        if letter in string.ascii_uppercase:
            word = word.replace(letter, ' %s' %letter)
    return word

@register.filter
def is_list(value):
    return type(value) == list


@register.filter
def spacify(value):
    return mark_safe(value.replace('  ', '&nbsp;&nbsp;'))

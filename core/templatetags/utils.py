import logging

from django import template
from django.template.defaultfilters import stringfilter
from django.utils import numberformat

logger = logging.getLogger('django.project.' + __name__)

register = template.Library()


@register.filter
def get(d, name):
    return d.get(name, '')


@register.filter
def stringify(value):
    return str(value)


@register.filter
def get_files(request, name):
    return request.FILES.getlist(name)


@register.filter
@stringfilter
def concat(first, second):
    return first + str(second)


@register.filter
def paginator_range(page_range, number):
    return page_range[number - 4 if number > 4 else 0: number + 3]


@register.filter
def money(value):
    return numberformat.format(value, decimal_sep=',', thousand_sep=' ', grouping=3, force_grouping=True)


@register.filter
@stringfilter
def startswith(first, second):
    return first.startswith(second)

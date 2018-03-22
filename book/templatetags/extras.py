from django import template

from book.models import PROIE

register = template.Library()


@register.filter(name='produit_display')
def produit_display(value):
    return dict(PROIE).get(value)



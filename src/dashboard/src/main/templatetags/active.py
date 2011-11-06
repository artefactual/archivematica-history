from django.template import Library
import math

register = Library()

@register.simple_tag
def active(request, pattern):
  if pattern == request.path:
    return 'active'

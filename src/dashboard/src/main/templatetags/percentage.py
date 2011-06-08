from django.template import Node, Library

register = Library()

@register.filter('percentage')
def percentage(value, total):
  try:
    percentage = float(value) / float(total) * 100
  except ZeroDivisionError:
    percentage = 0
  return '<abbr title="%s/%s">%s%%</abbr>' % (value, total, percentage)

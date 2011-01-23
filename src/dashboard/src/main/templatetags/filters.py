from django import template
import os

register = template.Library()

@register.filter('join_path')
def join_path(value, path):
  return os.path.join(value, path)

@register.filter('is_file')
def is_file(value, basedir):
  return os.path.isfile(os.path.join(basedir, value))

@register.filter('is_dir')
def is_dir(value, basedir):
  return os.path.isdir(os.path.join(basedir, value))
#!/usr/bin/env python

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.


# @package Archivematica
# @subpackage Configuration
# @author Jack Bates <jack@artefactual.com>
# @author Jesús García Crespo <jesus@artefactual.com>
# @version svn: $Id$


# -*- coding: utf-8 -*-

import optparse
import os.path
import re
import sys
import urllib
import urllib2
import urlparse

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

# Take into account that the url paths below changed in 1.1
# This is compatible with 1.0.8.1
URL_LOGIN='http://localhost/index.php/user/login'
URL_CREATE_ISAD='http://localhost/index.php/informationobject/create/isad'
URL_CREATE_DO='http://localhost/index.php/digitalobject/create'
ROOT_ID='/index.php/informationobject/show/isad/1'

class LoginError(Exception):
  response = None
  message = None

  def __init__(self, response):
    self.response = response.read()
    self.message = self.search_error()
    Exception.__init__(self, self.message)

  def search_error(self):
    regex = re.compile(r'<div class=\"form_error\">(.*?)</div>', re.DOTALL)
    robj = regex.search(self.response)

    if robj is None:
      return "Login was not successful"
    else:
      return robj.group(1).strip()

class FileNotFound(Exception):
  pass

def get_id_from_url(url):
  path = urlparse.urlparse(url).path
  return re.search(r'\d+', path).group()

def upload(opts):
  # Build opener with HTTPCookieProcessor, which send cookies back automatically
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
  urllib2.install_opener(opener)

  # Login
  data = { 'login[email]' : opts['email'], 'login[password]' : opts['password'] }
  response = urllib2.urlopen(URL_LOGIN, urllib.urlencode(data))

  # Check if login was successful
  if 'user/login' in response.geturl():
    raise LoginError(response)

  # Check if file exists
  if os.path.exists(opts['file']) is False:
    raise FileNotFound('File \'%s\' not found' % opts['file'])

  # Create information object
  data = { 'title' : opts['title'], 'parent' : ROOT_ID }
  response = urllib2.urlopen(URL_CREATE_ISAD, urllib.urlencode(data))

  # Get information object id
  id = get_id_from_url(response.geturl())

  # Upload digital object, (poster: register_openers(), multipart_encode())
  register_openers()
  data, headers = multipart_encode({ 'file' : open(opts['file']), 'informationObject' : id })
  request = urllib2.Request(URL_CREATE_DO, data, headers)
  response = urllib2.urlopen(request)

# Main program
if __name__ == '__main__':
  try:
    # Parse command line
    parser = optparse.OptionParser(usage='Usage: %prog [options]')

    parser.add_option('-d', '--debug', dest='debug', action='store_true', help='debug mode')

    authentication = optparse.OptionGroup(parser, 'Authentication options')
    authentication.add_option('-e', '--email', dest='email', metavar='EMAIL', help='account e-mail')
    authentication.add_option('-p', '--password', dest='password', metavar='PASSWORD', help='account password')

    parser.add_option_group(authentication)

    digitalobject = optparse.OptionGroup(parser, 'Digital Object options')
    digitalobject.add_option('-t', '--title', dest='title', metavar='TITLE', help='information object title')
    digitalobject.add_option('-f', '--file', dest='file', metavar='FILE', help='file path')

    parser.add_option_group(digitalobject)

    (opts, args) = parser.parse_args()

    # Check missing options, parse.error() raises sys.exit(2) (in UNIX, syntax problem)
    if opts.email is None and opts.password is None and opts.title is None and opts.file is None:
       parser.print_help()
       sys.exit(2)
    if opts.email is None or opts.password is None:
      parser.error('You must provide login details (e-mail and password).')
    if opts.title is None:
      parser.error('You must provide a title.')
    if opts.file is None:
      parser.error('You must provide a file.')

    # Call main function
    upload({
      'email' : opts.email,
      'password' : opts.password,
      'title' : opts.title,
      'file' : opts.file,
      })

  except KeyboardInterrupt:
    sys.exit('ERROR: Interrupted by user')

  except urllib2.HTTPError, err:
    if opts.debug:
      print err.geturl()
      print err.info()
    sys.exit('ERROR: The server couldn\'t fulfill the request. Error code: %s.' % err.code) 

  except urllib2.URLError, err:
    if opts.debug:
      print err.geturl()
      print err.info()
    sys.exit('ERROR: Failed trying to reach the server. Reason: %s.' % err.reason)

  except Exception, err:
    sys.exit('ERROR: %s' % err)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# @author Jesus Garcia Crespo <jesus@artefactual.com>
# @version svn: $Id$


import cookielib
import shutil
import optparse
import os.path
import re
import sys
import urllib
import urllib2
import urlparse

import xml.etree.ElementTree as etree

from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler

# This is for ICA-AtoM 1.0.9 URL schema
URL_BASE = 'http://localhost:8080/~jesus/qubit/index.php'
URL_LOGIN = URL_BASE + '/;user/login'
URL_CREATE_ISAD = URL_BASE + '/;create/isad'
URL_CREATE_DO = URL_BASE + '/;digitalobject/create'
URL_CREATE_ISAAR = URL_BASE + '/;create/isaar'
URL_AUTOCOMPLETE_ACTOR = URL_BASE + '/;actor/autocomplete'
URL_SEARCH_INFORMATION_OBJECT = URL_BASE + '/;search/index'

# Some static values
ROOT_ID = '/1;isad'
SERIES_ID = '/187;term'
DRAFT_ID = 159
CREATION_ID = 111

class LoginError(Exception):
  response = None
  message = None

  def __init__(self, response):
    self.response = response.read()
    self.message = self.search_error()
    Exception.__init__(self, self.message)

  def search_error(self):
    regex = re.compile(r'<div class=\"messages error\">\s+<ul>\s+<li>(.*?)</li>\s+</ul>\s+</div>', re.DOTALL)
    robj = regex.search(self.response)

    if robj is None:
      return 'Login was not successful'
    else:
      return robj.group(1).strip() + ' (this message was captured from server response)'

class FileNotFound(Exception):
  pass

class URLNotAccessible(Exception):
  pass

def get_id_from_url(url):
  path = urlparse.urlparse(url).path
  return re.search(r'\d+', path).group()

def find_information_object(name):
  # Search for information object
  data = { 'query': name }
  response = urllib2.urlopen(URL_SEARCH_INFORMATION_OBJECT, urllib.urlencode(data))

  regex = re.compile(r'<div class=\"section\">\s+<div class=\"clearfix search-results odd\">\s+<h2><a href=\"(.*?)\"', re.DOTALL)
  robj = regex.search(response.read())

  if robj is None:
    return ROOT_ID;
  else:
    return robj.group(1)

def find_or_create_actor(name):
  # Search for actor
  data = { 'query': name }
  print data
  response = urllib2.urlopen(URL_AUTOCOMPLETE_ACTOR, urllib.urlencode(data))
  content = response.read()

  regex = re.compile(r'<div class=\"result-count\">(.*?)</div>', re.DOTALL)
  robj = regex.search(content)

  if robj.group(1).strip() == 'No results':
    # Create a new actor
    data = { 'authorizedFormOfName': name }
    response = urllib2.urlopen(URL_CREATE_ISAAR, urllib.urlencode(data))
    return response.url
  else:
    regex = re.compile(r'<tbody>\s+<tr class=\"odd\">\s+<td>\s+<a href=\"(.*?)\"', re.DOTALL)
    robj = regex.search(content)
    return robj.group(1)

def upload(opts):
  # Check if file exists
  if opts['file'] and os.path.exists(opts['file']) is False:
    raise FileNotFound('File/directory "%s" not found' % opts['file'])
  elif opts['url']:
    try:
      urllib2.urlopen(opts['url'])
    except:
      raise URLNotAccessible('URL "%s" is not accessible' % opts['url'])

  # Build opener with HTTPCookieProcessor, which send cookies back automatically
  cj = cookielib.CookieJar()
  handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), *handlers)
  urllib2.install_opener(opener)

  # Login
  data = { 'email' : opts['email'], 'password' : opts['password'] }
  response = urllib2.urlopen(URL_LOGIN, urllib.urlencode(data))

  # Print symfony session id
  if opts['debug']:
    for index, cookie in enumerate(cj):
      if cookie.name == 'symfony':
        print 'Symfony session ID: ' + cookie.value
        break;

  # Check if login was successful
  if 'user/login' in response.url:
    raise LoginError(response)

  # Is a directory?
  if os.path.isdir(opts['file']):

    # Parse METS.xml
    tree = etree.parse(opts['file'] + '/METS.xml')

    prefix = '{http://purl.org/dc/terms/}'

    # To storage data to post to information object creation form
    data = {}

    # Requirements:
    # - identifier
    # - title
    # - levelOfDescription
    # - creators (creator)
    # - scopeAndContent (description)
    # - parent (isPartOf)
    # - updateEvents (date)

    # Default values
    data['levelOfDescription'] = SERIES_ID
    data['parent'] = ROOT_ID
    data['publicationStatus'] = DRAFT_ID

    for item in tree.find("dmdSec/mdWrap/xmlData/dublincore"):
      if item.tag == prefix + 'identifier':
        data['identifier'] = item.text
      elif item.tag == prefix + 'title':
        data['title'] = item.text
      elif item.tag == prefix + 'description':
        data['scopeAndContent'] = item.text
      elif item.tag == prefix + 'date':
        data['updateEvents[new][typeId]'] = CREATION_ID
        data['updateEvents[new][dateDisplay]'] = ''
        start_date, end_date = item.text.split('/')
        data['updateEvents[new][startDate]'], data['updateEvents[new][endDate]'] = item.text.split('/')
      elif item.tag == prefix + 'creator':
        data['creators[0]'] = find_or_create_actor(item.text)
      elif item.tag == prefix + 'isPartOf':
        data['parent'] = find_information_object(item.text)

    # Create information object
    response = urllib2.urlopen(URL_CREATE_ISAD, urllib.urlencode(data))

    # Get information object id
    parent_id = get_id_from_url(response.url)

    # Print information object id
    if opts['debug']:
      print 'New information object ID: ' + parent_id

    # Iterate over files in objects/ directory
    for file in os.listdir(opts['file'] + '/objects'):

      # Create information object
      data = { 'title' : file, 'parent' : '/' + parent_id + ';isad' }
      response = urllib2.urlopen(URL_CREATE_ISAD, urllib.urlencode(data))

      id = get_id_from_url(response.url)

      # Print information object id
      if opts['debug']:
        print 'New information object ID: %s (parent ID %s)' % (id, parent_id)

      data, headers = multipart_encode({ 'file' : open(opts['file'] + '/objects/' + file), 'informationObject' : id })
      request = urllib2.Request(URL_CREATE_DO, data, headers)
      response = urllib2.urlopen(request)

    if opts['remove']:
      shutil.rmtree(opts['file'])


  # Is a file?
  else:

    # Create information object
    data = { 'title' : opts['title'], 'parent' : ROOT_ID }
    response = urllib2.urlopen(URL_CREATE_ISAD, urllib.urlencode(data))

    # Get information object id
    id = get_id_from_url(response.url)

    # Print information object id
    if opts['debug']:
      print 'New information object ID: ' + id

    # Fetch file content or external resource
    if opts['file']:
      data, headers = multipart_encode({ 'file' : open(opts['file']), 'informationObject' : id })
      request = urllib2.Request(URL_CREATE_DO, data, headers)
      response = urllib2.urlopen(request)

    elif opts['url']:
      data = { 'url' : opts['url'], 'informationObject' : id }
      response = urllib2.urlopen(URL_CREATE_DO, urllib.urlencode(data))

    if opts['debug']:
      print 'New information object URL: ' + response.url

    if opts['remove']:
      os.remove(opts['file'])

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
    digitalobject.add_option('-f', '--file', dest='file', metavar='FILE', help='file/directory path')
    digitalobject.add_option('-u', '--url', dest='url', metavar='URL', help='URL')

    parser.add_option_group(digitalobject)

    misc = optparse.OptionGroup(parser, 'Miscelaneous options')
    misc.add_option('-r', '--remove', dest='remove', action='store_true', help='remove file/directory after successful upload')

    parser.add_option_group(misc)

    (opts, args) = parser.parse_args()

    # Check missing options, parse.error() raises sys.exit(2) (in UNIX, syntax problem)
    if opts.email is None and opts.password is None and opts.title is None and opts.file is None:
       parser.print_help()
       sys.exit(2)
    if opts.email is None or opts.password is None:
      parser.error('You must provide login details (e-mail and password).')
    # if opts.title is None:
    #  parser.error('You must provide a title.')
    if opts.file is None and opts.url is None:
      parser.error('You must provide a file or URL.')
    elif opts.file != None and opts.url != None:
      parser.error('It is not possible to create a digital object from a file and URL simultaneously.')

    # Call main function
    upload({
      'email' : opts.email,
      'password' : opts.password,
      'title' : opts.title,
      'file' : opts.file,
      'url' : opts.url,
      'remove' : opts.remove,
      'debug' : opts.debug
      })

  except KeyboardInterrupt:
    sys.exit('ERROR: Interrupted by user')

  except urllib2.HTTPError, err:
    sys.exit('ERROR: The server couldn\'t fulfill the request. Error code: %s.' % err.code) 

  except urllib2.URLError, err:
    sys.exit('ERROR: Failed trying to reach the server. Reason: %s.' % err.reason)

  # except Exception, err:
  #  sys.exit('ERROR: %s' % err)

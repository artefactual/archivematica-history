#!/usr/bin/python -OO
#
# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


dctermsNS = "http://purl.org/dc/terms/"
xsiNS = "http://www.w3.org/2001/XMLSchema-instance"
metsNS = "http://www.loc.gov/METS/"
premisNS = "info:lc/xmlns/premis-v2"
dctermsNS = "http://purl.org/dc/terms/"
fitsNS = "http://hul.harvard.edu/ois/xml/ns/fits/fits_output"
xlinkNS = "http://www.w3.org/1999/xlink"


dctermsBNS = "{" + dctermsNS + "}"
xsiBNS = "{" + xsiNS + "}"
metsBNS = "{" + metsNS + "}"
premisBNS = "{" + premisNS + "}"
dctermsBNS = "{" + dctermsNS + "}"
fitsBNS = "{" + fitsNS + "}"
xlinkBNS = "{" + xlinkNS + "}"

NSMAP = { "dcterms" : dctermsNS, \
"xsi" : xsiNS, \
"mets" : metsNS, \
"premis" : premisNS, \
"dcterms" : dctermsNS, \
"xlink": xlinkNS }


#!/usr/bin/python -OO
#
# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
# @subpackage archivematicaClientScript
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


xsiNS = "http://www.w3.org/2001/XMLSchema-instance"
metsNS = "http://www.loc.gov/METS/"
premisNS = "info:lc/xmlns/premis-v2"
dctermsNS = "http://purl.org/dc/terms/"
fitsNS = "http://hul.harvard.edu/ois/xml/ns/fits/fits_output"
xlinkNS = "http://www.w3.org/1999/xlink"
dcNS="http://purl.org/dc/elements/1.1/"

dcBNS = "{" + dcNS + "}"
dctermsBNS = "{" + dctermsNS + "}"
xsiBNS = "{" + xsiNS + "}"
metsBNS = "{" + metsNS + "}"
premisBNS = "{" + premisNS + "}"
fitsBNS = "{" + fitsNS + "}"
xlinkBNS = "{" + xlinkNS + "}"

NSMAP = { "xsi" : xsiNS, \
"xlink": xlinkNS }

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

databaseName="MCP"
username="demo"
password="demo"
sudo mysqladmin create "$databaseName"
#sudo mysql "$databaseName"
sudo mysql --execute="source ./mysql" "$databaseName"
sudo mysql --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}'"
sudo mysql --execute="GRANT SELECT, UPDATE, INSERT ON ${databaseName}.* TO '${username}'@'localhost'"


#to delete the database and all of it's contents
# sudo mysqladmin drop MCP

databaseName="MCP"
currentDir="$(dirname $0)"

echo "Removing existing units"
sudo ./removeUnitsFromWatchedDirectories.py

echo "Enter root database password for each the following. (Hit enter if blank)"

# CREATE DATABASE MCP CHARACTER SET utf8 COLLATE utf8_unicode_ci
mysql -u root -p --execute="DROP DATABASE IF EXISTS MCP; CREATE DATABASE MCP;" \
                 --execute="USE $databaseName; source $currentDir/../src/MCPServer/share/mysql;" \
                 --execute="USE $databaseName; source $currentDir/../src/transcoder/share/mysql;"


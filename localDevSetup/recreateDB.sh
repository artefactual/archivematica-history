databaseName="MCP"
currentDir="$(dirname $0)"
username="demo"
password="demo"

echo "Removing existing units"
sudo ./removeUnitsFromWatchedDirectories.py

echo "Enter root database password for each the following. (Hit enter if blank)"

mysql -u root -p --execute="DROP DATABASE IF EXISTS MCP; CREATE DATABASE MCP CHARACTER SET utf8 COLLATE utf8_unicode_ci;" \
                 --execute="USE $databaseName; source $currentDir/../src/MCPServer/share/mysql;" \
                 --execute="USE $databaseName; source $currentDir/../src/transcoder/share/mysql;" \
                 --execute="DROP USER '${username}'@'localhost'" \
                 --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}'" \
                 --execute="GRANT SELECT, UPDATE, INSERT, DELETE ON ${databaseName}.* TO '${username}'@'localhost'"

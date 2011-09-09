databaseName="MCP"
currentDir="$(dirname $0)"

echo "Removing existing units"
sudo ./removeUnitsFromWatchedDirectories.py


echo "Enter root database password for the following. (Hit enter if blank)"

echo MCPServer
mysql -u root -p --execute="source $currentDir/../src/MCPServer/share/mysql" "$databaseName"

echo transcoder
mysql -u root -p --execute="source $currentDir/../src/transcoder/share/mysql" "$databaseName"


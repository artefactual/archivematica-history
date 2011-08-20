databaseName="MCP"
sudo echo "Enter root database password for the following. (Hit enter if blank)"
echo MCPServer
sudo mysql -p --execute="source ../src/MCPServer/share/mysql" "$databaseName"
echo transcoder
sudo mysql -p --execute="source ../src/transcoder/share/mysql" "$databaseName"


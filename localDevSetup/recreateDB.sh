databaseName="MCP"
sudo echo "Enter root database password twice. (Hit enter if blank)"
sudo mysql -p --execute="source ../src/MCPServer/share/mysql" "$databaseName"
sudo mysql -p --execute="source ../src/transcoder/share/mysql" "$databaseName"


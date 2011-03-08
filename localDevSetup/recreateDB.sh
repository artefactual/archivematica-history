databaseName="MCP"
sudo mysql -p --execute="source ../src/MCPServer/share/mysql" "$databaseName"
sudo mysql -p --execute="source ../src/transcoder/share/mysql" "$databaseName"


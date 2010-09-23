databaseName="MCP"
sudo mysqladmin create "$databaseName"
sudo mysql "$databaseName"
sudo mysql --execute="source ./preMCPLogging.sql" "$databaseName"



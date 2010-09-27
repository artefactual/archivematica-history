databaseName="MCP"
username="demo"
password="demo"
sudo mysqladmin create "$databaseName"
#sudo mysql "$databaseName"
sudo mysql --execute="source ./preMCPLogging.sql" "$databaseName"
sudo mysql --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}'"
sudo mysql --execute="GRANT SELECT, INSERT ON ${databaseName}.* TO '${username}'@'localhost'"


#to delete the database and all of it's contents
# sudo mysqladmin drop MCP

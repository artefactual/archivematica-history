databaseName="MCP"
username="demo"
password="demo"
sudo mysqladmin create "$databaseName" -p
#sudo mysql "$databaseName"
sudo mysql -p --execute="source ./preMCPLogging.sql" "$databaseName"
sudo mysql -p --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}'"
sudo mysql -p --execute="GRANT SELECT, UPDATE, INSERT ON ${databaseName}.* TO '${username}'@'localhost'"


#to delete the database and all of it's contents
# sudo mysqladmin drop MCP

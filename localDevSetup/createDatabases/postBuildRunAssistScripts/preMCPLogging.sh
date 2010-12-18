databaseName="MCP"
username="demo"
password="demo"
dpPassword="$1"
sudo mysqladmin create "$databaseName" $dpPassword
#sudo mysql $databaseName
sudo mysql $dpPassword --execute="source ./preMCPLogging.sql" "$databaseName"
sudo mysql $dpPassword --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}'"
sudo mysql $dpPassword --execute="GRANT ALL PRIVILEGES ON *.* TO 'demo'@'localhost'"


#to delete the database and all of it's contents
# sudo mysqladmin drop MCP

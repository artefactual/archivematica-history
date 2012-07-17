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
                 --execute="DROP USER '${username}'@'localhost';" \
                 --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}';" \
                 --execute="GRANT SELECT, UPDATE, INSERT, DELETE ON ${databaseName}.* TO '${username}'@'localhost';" 

#This command would auto add a user 'demo' with password 'demo'
#mysql -u root -p --execute="INSERT INTO auth_user (username, email, password, is_staff, is_active, is_superuser, date_joined) VALUES ('demo', 'demo@example.com', 'sha1$e7fc2$6123f456bba92c67a409baf2c282398fc5f70fc9', TRUE, TRUE, TRUE, NOW() );"

databaseName="MCP"
currentDir="$(dirname $0)"
username="demo"
password="demo"

echo "Removing existing units"
sudo ./removeUnitsFromWatchedDirectories.py

set -e
echo -n "Enter the DATABASE root password (Hit enter if blank):"
read dbpassword

if [ ! -z "$dbpassword" ] ; then
    dbpassword="-p${dbpassword}"
else
    dbpassword=""
fi
#set -o verbose #echo on
pwd
currentDir="`dirname $0`"
set +e
echo "Removing the old database"
mysql -u root "${dbpassword}" --execute="DROP DATABASE IF EXISTS ${databaseName}"
echo "Removing ${username} user"
mysql -u root "${dbpassword}" --execute="DROP USER '${username}'@'localhost';"
set -e

echo "Creating MCP database"
mysql -u root "${dbpassword}" --execute="CREATE DATABASE ${databaseName} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"

echo "Creating and populating MCP Tables"
mysql -u root "${dbpassword}" --execute="USE ${databaseName}; SOURCE $currentDir/../src/MCPServer/share/mysql;"

echo "Creating and populating Transcoder Tables"
mysql -u root "${dbpassword}" --execute="USE ${databaseName}; SOURCE $currentDir/../src/transcoder/share/mysql;"

echo "Creating ${username} user"
mysql -u root "${dbpassword}" --execute="CREATE USER '${username}'@'localhost' IDENTIFIED BY '${password}';"
mysql -u root "${dbpassword}" --execute="GRANT SELECT, UPDATE, INSERT, DELETE ON ${databaseName}.* TO '${username}'@'localhost';"

#echo "Creating dashboard user"
#mysql -u root -p --execute="INSERT INTO auth_user (username, email, password, is_staff, is_active, is_superuser, date_joined) VALUES ('demo', 'demo@example.com', 'sha1$e7fc2$6123f456bba92c67a409baf2c282398fc5f70fc9', TRUE, TRUE, TRUE, NOW() );"

#set +o verbose #echo off
printGreen="${databaseName} database created successfully."
echo -e "\e[6;32m${printGreen}\e[0m"

databaseName="TRANSCODER"
#sudo mysqladmin DROP "$databaseName" -p || sudo mysqladmin create  "$databaseName" -p
sudo mysql -p --execute="source ./transcoderDB.sql" "$databaseName"

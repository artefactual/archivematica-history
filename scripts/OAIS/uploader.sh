#!/bin/sh

cp -a $2 ~/storeAIP/.

curl --retry 20 -c - -d "login%5Bemail%5D=demo%40example.com&login%5Bpassword%5D=demo" -o /dev/null http://localhost/index.php/user/login | curl -v --retry 20 -b - -F title=$1 -F upload_file[140]=@$2 http://localhost/index.php/informationobject/create/isad

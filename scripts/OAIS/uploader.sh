#!/bin/bash

cp -a $2 ~/archivalstorage/.

curl --retry 20 -c /tmp/qubitcookies.txt -d "login%5Bemail%5D=demo%40example.com&login%5Bpassword%5D=demo&referer=&commit=log+in" http://localhost/index.php/user/login
curl -v --retry 20 -b /tmp/qubitcookies.txt -F identifier=$1 -F title=$1 -F upload_file[140]=@$2 -F commit=create  http://localhost/index.php/informationobject/create/isad


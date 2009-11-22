#!/bin/bash

cp -a $2 ~/storeAIP/.
rm /tmp/foobject
curl --retry 20 -s -c /tmp/qubitcookies -F login[email]=demo@example.com -F login[password]=demo http://localhost/index.php/user/login 
curl --retry 20 -s -b /tmp/qubitcookies -d "parent=%2Findex.php%2Finformationobject%2Fshow%2Fisad%2F1&title=$1" --write-out "%{redirect_url}" http://localhost/index.php/informationobject/create/isad > /tmp/foobject
cat /tmp/foobject |cut -d'/' -f11 > /tmp/foobject
cat /tmp/foobject |cut -d';' -f2 > /tmp/foobject
speakup=$(echo `cat /tmp/foobject` | sed 's/ //g')
curl -b /tmp/qubitcookies -F file=@$2 http://localhost/index.php/digitalobject/create?informationObject=$speakup


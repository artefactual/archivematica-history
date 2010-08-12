find /tmp/$UUID/ -type f -print| while read NEWDOCS
    do
        chmod 700 $NEWDOCS
    done

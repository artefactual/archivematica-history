
fileType="*.xml"
oldString="%normalizationScriptsDir%unoconv.sh"
newString="%unoconvAlternativePath%"
backups="/tmp/backups-`uuid`"
mkdir "$backups"
#http://blog.parwy.com/2007/11/bulk-search-and-replace-using-sed.html
for i in $(find ./ -name "${fileType}"); do 
    sed "s/${oldString}/${newString}/g" "$i" > "$i-tmp"
    mv $i "${backups}/$i"
    mv $i-tmp $i
done

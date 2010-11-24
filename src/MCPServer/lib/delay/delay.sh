cd "$2"
find ${2}/* -maxdepth 0 -amin "+${1}" -print| while read FILE

do
  	#basedName=`basename "$FILE"`
    if [ -d "$FILE" ]; then
    	echo moving $FILE 
    	mv "$FILE" "$3"  
    fi    
done
rm ./*.png
set -e
./main.py
java -jar ./../../../archivematicaCommon/lib/externals/plantUML/plantuml.jar ./plantUML.txt 
ls



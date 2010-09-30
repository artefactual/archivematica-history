#This script  will be modified to allow user to select the type of vm to build.
sudo vmbuilder vmserver ubuntu -c archivematica.cfg -d "archivematicaBuild" --rootsize 8000
mv ./archivematicaBuild "./archivematicaBuild-`date`"

echo "The default password is demo"
./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard
sudo chmod 444 -R ~/.config/xfce4/panel
sudo chmod 770 -R  ~/sharedFolders/
sudo chown -R archivematica:archivematica ~/sharedFolders/
sudo chmod -R g+s ~/sharedFolders/
sudo gpasswd -a demo archivematica
echo "PLEASE LOG OUT TO ENABLE NEW GROUP SETTINGS"


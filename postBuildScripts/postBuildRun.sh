echo "The default password is demo"
./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard
sudo chmod 444 -R ~/.config/xfce4/panel
sudo chmod 770 -R  ~/sharedDirectories/
sudo chown -R archivematica:archivematica ~/sharedDirectories/
sudo chmod -R g+s ~/sharedDirectories/
echo "Disabling Screen Saver (Better for VM's)"
sudo aptitude remove xscreensaver
sudo gpasswd -a demo archivematica
echo "PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS"
sleep 3

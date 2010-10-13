echo "The default password is demo"
./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard
sudo chmod 444 -R ~/.config/xfce4/panel
sudo chmod 770 -R  ~/sharedDirectory/
sudo chown -R archivematica:archivematica ~/sharedDirectory/
sudo chmod -R g+s ~/sharedFolders/
echo "Disabling Screen Saver (Better for VM's)"
gconftool-2 -s /apps/gnome-screensaver/idle_activation_enabled --type=bool false
sudo gpasswd -a demo archivematica
echo "PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS"
sleep 3

echo "The default password is demo"
cd postBuildRunAssistScripts
#./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard
sudo chmod 444 -R ~/.config/xfce4/panel
sudo chmod 770 -R  /var/archivematica/sharedDirectory/
sudo chown -R archivematica:archivematica /var/archivematica/sharedDirectory/
sudo chmod -R g+s /var/archivematica/sharedDirectory/
echo "Disabling Screen Saver (Better for VM's)"
sudo aptitude remove xscreensaver
sudo gpasswd -a demo archivematica
echo " "
echo "===PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS==="
echo " "
sleep 3

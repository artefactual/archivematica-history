echo "The default password is demo"
cd postBuildRunAssistScripts
./preMCPLogging.sh
sudo mysqladmin create ica-atom -p
sudo mysqladmin create dcb -p
sudo mysqladmin create qubit -p
sudo mysqladmin create dashboard -p
#sudo chmod 444 -R ~/.config/xfce4/panel
#sudo chmod 770 -R  ~/sharedDirectory/
#sudo chown -R archivematica:archivematica ~/sharedDirectory/
#sudo chmod -R g+s ~/sharedDirectory/
#echo "Disabling Screen Saver (Better for VM's)"
#sudo aptitude remove xscreensaver
#sudo gpasswd -a demo archivematica
echo " "
echo "===PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS==="
echo " "
sleep 3

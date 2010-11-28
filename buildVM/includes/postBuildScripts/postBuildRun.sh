echo "The default password is demo"
cd postBuildRunAssistScripts
#./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard


#xfce4 configuration
cp ./panel/* /home/demo/.config/xfce4/panel
cp ./xfceCustomization/xfce4-desktop.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/xfce4-session.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/icons.screen0.rc /home/demo/.config/xfce4/desktop
cp ./xfceCustomization/user-dirs.defaults /etc/xdg
cp ./xfceCustomization/uca.xml /home/demo/.config/Thunar
cp ./xfceCustomization/thunarrc /home/demo/.config/Thunar
cp ./xfceCustomization/thunar.desktop /home/demo/.config/autostart
cp ./xfceCustomization/gtk-bookmarks /home/demo/.gtk-bookmarks
cp ./xfceCustomization/gdm.custom.conf /etc/gdm/custom.conf

#fix permissions 
chroot "$1" chmod 444 /home/demo/.config/xfce4/panel
chroot "$1" chown -R demo:demo /home/demo
chroot "$1" chown -R demo:demo /home/demo/.mozilla

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

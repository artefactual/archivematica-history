#This shell script demonstrates the full use of PyODConverter for Linux:

#!/bin/bash 
# Try to autodetect OOFFICE and OOOPYTHON. 
OOFFICE=`ls /usr/bin/openoffice.org2.4 /usr/bin/ooffice /usr/lib/openoffice/program/soffice | head -n 1` 
OOOPYTHON=`ls /opt/openoffice.org*/program/python /usr/bin/python | head -n 1` 
if [ ! -x "$OOFFICE" ] ; then 
    echo "Could not auto-detect OpenOffice.org binary" 
    exit 
fi 
if [ ! -x "$OOOPYTHON" ]; then 
    echo "Could not auto-detect OpenOffice.org Python" 
    exit 
fi 
echo "Detected OpenOffice.org binary: $OOFFICE" 
echo "Detected OpenOffice.org python: $OOOPYTHON" 
# Reference: http://wiki.services.openoffice.org/wiki/Using_Python_on_Linux 
# If you use the OpenOffice.org that comes with Fedora or Ubuntu, uncomment the following line: 
export PYTHONPATH="/usr/lib/openoffice.org/program" 
# If you want to simulate for testing that there is no X server, uncomment the next line. 
unset DISPLAY 
# Kill any running OpenOffice.org processes. 
killall -u `whoami` -q soffice 
# Download the converter script if necessary. 
test -f DocumentConverter.py || wget http://www.artofsolving.com/files/DocumentConverter.py 
# Start OpenOffice.org in listening mode on TCP port 8100. 
$OOFFICE "-accept=socket,host=localhost,port=8100;urp;StarOffice.ServiceManager" -norestore -nofirststartwizard -nologo -headless & 
# Wait a few seconds to be sure it has started. 
sleep 5s 
# Convert as many documents as you want serially (but not concurrently). 
# Substitute whichever documents you wish. 
## $OOOPYTHON DocumentConverter.py sample.ppt sample.swf 
## $OOOPYTHON DocumentConverter.py sample.ppt sample.pdf 
# Close OpenOffice.org. 
#killall -u `whoami` soffice


#Xvfb vs -headless
# To use the -headless command line parameter, you must use OpenOffice.org 2.3.0 or later with the RPM package openoffice.org-headless-2.3.1-9238.i586.rpm. If you use an older OpenOffice.org version, you will need Xvfb to simulate an X server where one is not available:

#!/bin/bash 
# Set DISPLAY to something besides :1 (because :1 is the standard display). DISPLAY=:1000 
# Kill any existing virtual framebuffers. 
##killall -u `whoami` Xvfb 
# Start the framebuffer. 
##Xvfb $DISPLAY -screen 0 800x600x24 & 
# Run the OpenOffice.org conversion script above. 
##ooo-convert.sh 
# Clean up 
##killall -u `whoami` Xvfb


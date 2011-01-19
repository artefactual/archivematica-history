#!/usr/bin/python
from lxml import etree
from optparse import OptionParser
import os

#<action>
#    <icon>accessories-calculator</icon>
#    <name>Verify MD5 Checksum</name>
#    <command>/usr/bin/archivematicaCheckMD5 %F</command>
#    <description>Verify the MD5 checksums listed in the selected file</description>
#    <patterns>*</patterns>
#    <directories/>
#    <audio-files/>
#    <image-files/>
#    <other-files/>
#    <text-files/>
#    <video-files/>
#</action>
def add(filePath="~/.config/Thunar/uca.xml", \
    icon="accessories-calculator", \
    name="", \
    command="", \
    description="", \
    patterns="*", \
    directories="", \
    audioFiles="", \
    imageFiles="", \
    otherFiles="", \
    textFiles="", \
    videoFiles="" ):
    
    if filePath.startswith("~/"):
        homepath = os.path.expanduser('~')
        filePath = filePath.replace('~', homepath, 1)
    
    tree = etree.parse(filePath)
    root = tree.getroot()
    print(etree.tostring(root, pretty_print=True))

    action = etree.SubElement(root, "action")
    etree.SubElement(action, "name").text = name
    etree.SubElement(action, "command").text = command
    etree.SubElement(action, "description").text = description
    etree.SubElement(action, "patterns").text = patterns
    etree.SubElement(action, "directories").text = directories
    etree.SubElement(action, "audio-files").text = audioFiles
    etree.SubElement(action, "image-files").text = imageFiles
    etree.SubElement(action, "other-files").text = otherFiles
    etree.SubElement(action, "text-files").text = textFiles
    etree.SubElement(action, "video-files").text = videoFiles
    
    print(etree.tostring(root, pretty_print=True))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default="~/.config/Thunar/uca.xml", \
        help="The uca.xml to edit.", metavar="uca.xml")
        
    #icon
    parser.add_option("-i", "--icon", metavar="icon", default="accessories-calculator", \
        help="Icon to use in display. ie. \"accessories-calculator\"")

    #name
    parser.add_option("-n", "--name", metavar="name", default="", \
        help="name for script")
    
    #command
    parser.add_option("-c", "--command", metavar="command", default="", \
        help="Command to insert.")

    #description
    parser.add_option("-d", "--description", metavar="description", default="", \
        help="Mouseover Description")
   
    #patterns
    parser.add_option("-p", "--patterns", metavar="patterns", default="*", \
        help="")
    
    #directories
    parser.add_option("-D", "--directories", metavar="directories", default="", \
        help="")
    
    #audioFiles
    parser.add_option("-A", "--audioFiles", metavar="audioFiles", default="", \
        help="")
    
    #imageFiles
    parser.add_option("-I", "--imageFiles", metavar="imageFiles", default="", \
        help="")
    
    #otherFiles
    parser.add_option("-O", "--otherFiles", metavar="otherFiles", default="", \
        help="")
    
    #textFiles
    parser.add_option("-T", "--textFiles", metavar="textFiles", default="", \
        help="")
    
    #videoFiles
    parser.add_option("-V", "--videoFiles", metavar="videoFiles", default="", \
        help="")
    

    
    (options, args) = parser.parse_args()
    print options
    print args
    add(options.filename, \
        options.icon, \
        options.name, \
        options.command, \
        options.description, \
        options.patterns, \
        options.directories, \
        options.audioFiles, \
        options.imageFiles, \
        options.otherFiles, \
        options.textFiles, \
        options.videoFiles )
        

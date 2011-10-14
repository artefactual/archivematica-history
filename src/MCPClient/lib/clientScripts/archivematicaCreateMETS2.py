
import lxml.etree as etree
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface


#Global Variables
globalMets
globalFileSec
globalFileGrps = {} 
##counters
#globalCounter = 0
globalDmdSecCounter = 0
globalAmdSecCounter = 0
globalTechMDCounter = 0
globalRightsMDCounter = 0
globalDigiprovMDCounter = 0


#GROUPID="G1" -> GROUPID="Group-%object's UUID%"
##group of the object and it's related access, license

if __name__ == '__main__':
    structMAP
    #<div TYPE="directory" LABEL="AIP1-UUID">
    #<div TYPE="directory" LABEL="objects" DMID="dmdSec_01">
    #Recursive function for creating structmap and fileSec 
    


#DMID="dmdSec_01" for an object goes in here
#<file ID="file1-UUID" GROUPID="G1" DMID="dmdSec_02" ADMID="amdSec_01">
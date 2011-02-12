#main
import re
import MySQLdb

database=_mysql.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    
    RarExtensions = [re.compile('.r\d{2}$', re.I),
              re.compile('.part\d{2}.rar$', re.I),
              re.compile('.rar$', re.I),]
    for extension in XtmExtensions:
        if fileName.endswith(extension):
            #sql find the file type,
            c=database.cursor()
            sql = """SELECT CR.pk, CR.command, CR.GroupMember 
            FROM CommandRelationships AS CR 
            JOIN FileIDs ON CR.fileID=FileIDs.pk 
            JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk 
            WHERE FileIDs.description='unrar-nonfreeCompatable' 
            AND CommandClassifications.classification = 'extract';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                ret.append(row)
            break
    
    SevenZipExtensions = ['.ARJ', '.CAB', '.CHM', '.CPIO',
                  '.DMG', '.HFS', '.LZH', '.LZMA',
                  '.NSIS', '.UDF', '.WIM', '.XAR',
                  '.Z', '.ZIP', '.GZIP', '.TAR',]
    for extension in XtmExtensions:
        if fileName.endswith(extension):
            c=database.cursor()
            sql = """SELECT CR.pk, CR.command, CR.GroupMember 
            FROM CommandRelationships AS CR 
            JOIN FileIDs ON CR.fileID=FileIDs.pk 
            JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk 
            WHERE FileIDs.description='7ZipCompatable' 
            AND CommandClassifications.classification = 'extract';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                ret.append(row)
            break
    return ret

class command:
    def __init__(commandID):
        self.pk = commandID
        c=database.cursor()
        sql = """SELECT """
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            ret.append(row)
        break
        
        
def main():
    commands = identifyCommands(fileName)

    if commands == []:
        return 0

    for command in commands:
        pk, command, group = command
        Class commands, id
        dic, gouping pointer to command class object.
        dic, based on id (no duplicates) of command class objects
    
    for every Command in the dictionary
        run the command.
        for every file in the extracted directory (and sub directories):
            fileAddedToSIP
            main() # on the just extracted directory
        store the exit code in the command object
        
    dic, exit code grouping.
    for each item in the grouping dictionary
        if grouping in exit code grouping.
            UPDATE it.
        else
            create it.
            
    compute exit code base on exit code grouping
    exit
    
    
    
if __name__ == '__main__':



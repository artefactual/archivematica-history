DROP TABLE IF EXISTS CommandTypes;
CREATE TABLE CommandTypes (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    type TEXT
);

INSERT INTO CommandTypes (type) 
    VALUES 
    ('command'), 
    ('bashScript'), 
    ('pythonScript'); 

DROP TABLE IF EXISTS CommandClassifications;
CREATE TABLE CommandClassifications (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    classification TEXT
);


INSERT INTO CommandClassifications
    (classification) VALUES('normalize'), ('access'), ('extract');

DROP TABLE IF EXISTS Commands;
CREATE TABLE Commands (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    commandType INT,
    Foreign Key (commandType) references CommandTypes(pk),
    verificationCommand INT,
    Foreign Key (verificationCommand) references Commands(pk),
    command LONGTEXT,
    outputLocation TEXT,
    eventDetailCommand INT,
    Foreign Key (eventDetailCommand) references Commands(pk),
    description LONGTEXT
);

DROP TABLE IF EXISTS CommandRelationships;
CREATE TABLE CommandRelationships (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    commandClassification INT,
    Foreign Key (commandClassification) references CommandClassifications(pk),
    command INT,
    Foreign Key (command) references Commands(pk),
    fileID INT,
    Foreign Key (fileID) references FileIDs(pk),
    GroupMember INT UNSIGNED DEFAULT 0,
    countOK INT UNSIGNED DEFAULT 0,
    countNotOK INT UNSIGNED DEFAULT 0
);
-- UPDATE CommandRelationships SET countOK=countOK+1 Where pk=1234 --

DROP TABLE IF EXISTS FileIDs;
CREATE TABLE FileIDs (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    description TEXT
);

DROP TABLE IF EXISTS FileIDsByExtension;
CREATE TABLE FileIDsByExtension (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    Extension TEXT,
    FileIDs INT,
    Foreign Key (FileIDs) references Command(pk)
);

DROP TABLE IF EXISTS FileIDsByPronom;
CREATE TABLE FileIDsByPronom (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    fileID TEXT,
    FileIDs INT,
    Foreign Key (FileIDs) references Command(pk)
);


INSERT INTO FileIDs
    (description) VALUES
    ('Normalize Defaults'), 
    ('Access Defaults'), 
    ('Extract Defaults'),
    ('7ZipCompatable'),
    ('unrar-nonfreeCompatable')
;

INSERT INTO Commands 
    (commandType, command, description) 
    SELECT pk,
    'test -e "%outputLocation%',
    'Verifying file exists'
    FROM CommandTypes WHERE type = 'command' ;

-- Default copy command --
INSERT INTO Commands 
    (commandType, verificationCommand, command, outputLocation, description) 
    VALUES 
    ((SELECT pk FROM CommandTypes WHERE type = 'command'),
    (SELECT pk FROM  (Select * From Commands) AS temp WHERE description = 'Verifying file exists and is not size 0'),
    'cp -R "%inputFile%" "%outputDirectory%%prefix%%fileName%%postfix%.%fileExtension%"',
    '"%outputDirectory%%prefix%%fileName%%postfix%.%fileExtension%"',
    'Copying File.');
    --     'cp --version | grep cp',


-- Associate default access with copy --
INSERT INTO CommandRelationships 
    (commandClassification, command, fileID)
    VALUES (
    (SELECT pk FROM CommandClassifications WHERE classification = 'access'),
    (SELECT pk FROM Commands WHERE description = 'Copying File.'),
    (SELECT pk FROM FileIDs WHERE description = 'Access Defaults')
);

-- 7ZipCompatable
INSERT INTO Commands 
    (commandType, command, outputLocation, description) 
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'command'),
    ('7z x -bd -o"%outputDirectory%" "%inputFile%"'),
    '"%outputDirectory%"',
    ('Extracting 7zip compatable file.')
);

INSERT INTO CommandRelationships 
    (commandClassification, command, fileID)
    VALUES (
    (SELECT pk FROM CommandClassifications WHERE classification = 'extract'),
    (SELECT pk FROM Commands WHERE description = 'Extracting 7zip compatable file.'),
    (SELECT pk FROM FileIDs WHERE description = '7ZipCompatable')
);
-- END 7ZipCompatable

-- unrar-nonfreeCompatable
INSERT INTO Commands 
    (commandType, command, outputLocation, description) 
    -- VALUES SELECT pk FROM FileIDS WHERE description = 'Normalize Defaults'
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'bashScript'),
    ('mkdir "%outputDirectory%" && unrar-nonfree x "%inputFile%" "%outputDirectory%"'),
    '"%outputDirectory%"',
    ('Extracting unrar-nonfree compatable file.')
);
    --    ('unrar-nonfree | grep \'UNRAR.\{3,10\} \''), 


INSERT INTO CommandRelationships 
    (commandClassification, command, fileID)
    VALUES (
    (SELECT pk FROM CommandClassifications WHERE classification = 'extract'),
    (SELECT pk FROM Commands WHERE description = 'Extracting unrar-nonfree compatable file.'),
    (SELECT pk FROM FileIDs WHERE description = 'unrar-nonfreeCompatable')
);
-- END unrar-nonfreeCompatable


-- ADD Normalization Path for .JPG --
INSERT INTO FileIDs 
    (description)
    VALUES (
    'A .jpg file'
);
set @fileID = LAST_INSERT_ID();

INSERT INTO FileIDsByExtension 
    (Extension, FileIDs)
    VALUES (
    'jpg',
    @fileID
);


INSERT INTO Commands 
    (commandType, command, description) 
    -- VALUES SELECT pk FROM FileIDS WHERE description = 'Normalize Defaults'
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'bashScript'),
    ('echo tool:\\"convert\\" version:\\"`convert -version | grep Version:`\\"'),
    ('convert event detail')
);

set @convertToTifEventDetailCommandID = LAST_INSERT_ID();

INSERT INTO Commands 
    (commandType, command, outputLocation, eventDetailCommand, description) 
    -- VALUES SELECT pk FROM FileIDS WHERE description = 'Normalize Defaults'
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'command'),
    ('convert "%fileFullName%" +compress "%outputDirectory%%prefix%%fileName%%postfix%.tif"'),
    '%outputDirectory%%prefix%%fileName%%postfix%.tif',
    @convertToTifEventDetailCommandID,
    ('Transcoding to tif with convert')
);
set @convertToTifCommandID = LAST_INSERT_ID();

INSERT INTO CommandRelationships 
    (commandClassification, command, fileID)
    VALUES (
    (SELECT pk FROM CommandClassifications WHERE classification = 'normalize'),
    @convertToTifCommandID,
    @fileID
);

-- End Of ADD Normalization Path for .JPG --













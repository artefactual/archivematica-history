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
    toolName LONGTEXT,
    toolVersionCommand LONGTEXT,
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
    'echo "%outputDirectory%%prefix%%fileName%%postFix%.%fileExtension%"',
    'Verifying file exists and is not size 0'
    FROM CommandTypes WHERE type = 'command' ;

-- Default copy command --
INSERT INTO Commands 
    (commandType, verificationCommand, command, toolName, toolVersionCommand, description) 
    VALUES 
    ((SELECT pk FROM CommandTypes WHERE type = 'command'),
    (SELECT pk FROM  (Select * From Commands) AS temp WHERE description = 'Verifying file exists and is not size 0'),
    'cp -R "%inputFile%" "%outputDirectory%%prefix%%fileName%%postFix%.%fileExtension%"',
    'copy',
    'cp --version | grep cp',
    'Copying File.');

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
    (commandType, command, toolName, toolVersionCommand, description) 
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'command'),
    ('7z x -bd -o"%outputDirectory%" "%inputFile%")'),
    ('7Zip'),
    ('echo ?'),
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
    (commandType, command, toolName, toolVersionCommand, description) 
    -- VALUES SELECT pk FROM FileIDS WHERE description = 'Normalize Defaults'
    VALUES (
    (SELECT pk FROM CommandTypes WHERE type = 'command'),
    ('echo "mkdir \"%outputDirectory%\" && unrar-nonfree x \"%inputFile%\" \"%outputDirectory%\"" | bash'),
    ('unrar-nonfree'),
    ('unrar-nonfree | grep \'UNRAR.\{3,10\} \''),
    ('Extracting unrar-nonfree compatable file.')
);

INSERT INTO CommandRelationships 
    (commandClassification, command, fileID)
    VALUES (
    (SELECT pk FROM CommandClassifications WHERE classification = 'extract'),
    (SELECT pk FROM Commands WHERE description = 'Extracting unrar-nonfree compatable file.'),
    (SELECT pk FROM FileIDs WHERE description = 'unrar-nonfreeCompatable')
);
-- END unrar-nonfreeCompatable




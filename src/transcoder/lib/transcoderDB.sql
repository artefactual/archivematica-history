
CREATE TABLE CommandType (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    type TEXT
);

Insert Into CommandType
    (type) VALUES('command'), ('bashScript'), ('pythonScript');

CREATE TABLE CommandClassification (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    classification TEXT
);

-- needs to move to relationship between id and a command--
Insert Into CommandClassification
    (classification) VALUES('normalize'), ('access');

CREATE TABLE Command (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    commandType INT,
    Foreign Key (commandType) references CommandType(pk),
    commandClassification INT,
    Foreign Key (commandClassification) references commandClassification(pk),
    commandText LONGTEXT
);

CREATE TABLE Tool (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    commandToGetVersion INT,
    Foreign Key (commandToGetVersion) references Command(pk)
);

CREATE TABLE FileIDsByPronom (
    pk INT PRIMARY KEY AUTO_INCREMENT,
    fileID TEXT,
    commandSet INT,
    Foreign Key (commandSet) references CommandSet(pk)
);

CREATE TABLE CommandSet (
    pk INT PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE CommandSetMember (
    commandSet INT,
    command INT,
    Foreign Key (commandSet) references CommandSet(pk),
    Foreign Key (command) references CommandSet(pk)
);


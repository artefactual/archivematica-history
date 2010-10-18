

CREATE TABLE Tasks (
taskUUID        VARCHAR(50) PRIMARY KEY,
jobUUID         VARCHAR(50),
createdTime     TIMESTAMP(8) DEFAULT NOW(),
fileUUID        VARCHAR(50),
fileName        VARCHAR(100),
exec            VARCHAR(50),
arguments       VARCHAR(1000),
startTime       TIMESTAMP(8),
client          VARCHAR(50),
endTime         TIMESTAMP(8),
exitCode        BIGINT
);


CREATE TABLE jobCreated(
jobUUID         VARCHAR(50) PRIMARY KEY,
createdTime     TIMESTAMP(8) DEFAULT NOW(),
directory       VARCHAR(250),
SIPUUID         VARCHAR(50)
);

CREATE TABLE jobStepCompleted(
pk              BIGINT PRIMARY KEY AUTO_INCREMENT,
jobUUID         VARCHAR(50),
completedTime   TIMESTAMP(8) DEFAULT NOW(),
step         VARCHAR(50)
);



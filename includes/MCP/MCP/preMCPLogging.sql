

CREATE TABLE taskCreated (
taskUUID   VARCHAR(50) PRIMARY KEY,
jobUUID    VARCHAR(50),
createdTime TIMESTAMP(8) DEFAULT NOW(),
fileUUID   VARCHAR(50),
exec       VARCHAR(50),
arguments  VARCHAR(1000)
);

CREATE TABLE taskAssigned (
taskUUID   VARCHAR(50) PRIMARY KEY,
startTime  TIMESTAMP(8) DEFAULT NOW(),
client     VARCHAR(50)
);

CREATE TABLE taskCompleted (
taskUUID   VARCHAR(50) PRIMARY KEY,
endTime    TIMESTAMP(8) DEFAULT NOW(),
exitCode   BIGINT
);



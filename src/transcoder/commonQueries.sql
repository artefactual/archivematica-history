-- Already In proper format --

select * from Tasks where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode = 0 AND Tasks.stdOut like "%Already in preservation format%";
select * from Tasks where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode = 0 AND Tasks.stdOut like "%Already in access format%";

-- Those not in proper format --

select * from Tasks where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode = 7 AND Tasks.stdOut like "%Unable to verify archival readiness.%";
select * from Tasks where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode = 7 AND Tasks.stdOut like "%Unable to verify access readiness%";

-- Failed Commands   --
select * from Tasks where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode != 0 AND NOT (exitCode = 7 AND Tasks.stdOut like "%Unable to verify access readiness%");


-- Relate to SIP UUID --
select * from Tasks JOIN Jobs on Tasks.jobUUID = Jobs.jobUUID where Tasks.exec LIKE "transcoderNormalizePreservation_v0.0" AND exitCode = 0 AND Tasks.stdOut like "%Already in access format%" AND Jobs.SIPUUID like '39cb319b-6af1-4b9c-a618-0a7ba33edf1c';


-- Show preservation and access commands based on extension --
select * from FileIDsByExtension AS FIBE JOIN FileIDs ON FIBE.FileIDs = FileIDs.pk JOIN CommandRelationships AS CR ON FileIDs.pk = CR.FileID JOIN Commands ON CR.command = Commands.pk JOIN CommandClassifications AS CC on CR.commandClassification = CC.pk;
select * from FileIDsByExtension AS FIBE JOIN FileIDs ON FIBE.FileIDs = FileIDs.pk JOIN CommandRelationships AS CR ON FileIDs.pk = CR.FileID JOIN Commands ON CR.command = Commands.pk JOIN CommandClassifications AS CC on CR.commandClassification = CC.pk JOIN CommandTypes AS CT ON Commands.commandType = CT.pk;
select *, CR.countAttempts - CR.countOK + CR.countNotOK AS countIncomplete from FileIDsByExtension AS FIBE JOIN FileIDs ON FIBE.FileIDs = FileIDs.pk JOIN CommandRelationships AS CR ON FileIDs.pk = CR.FileID JOIN Commands ON CR.command = Commands.pk JOIN CommandClassifications AS CC on CR.commandClassification = CC.pk JOIN CommandTypes AS CT ON Commands.commandType = CT.pk;





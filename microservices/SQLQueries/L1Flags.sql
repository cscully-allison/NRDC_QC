SELECT MES.[L1 Flag], ONE.[Name], ONE.[Description]
FROM [ProtoNRDC].[Data].[Measurements] MES
JOIN [ProtoNRDC].[Data].[Data Streams] DS 
ON MES.[Stream] = DS.[Stream]
JOIN [ProtoNRDC].[Vocabulary].[L1 Quality Control] ONE
ON ONE.[Flag] = MES.[L1 Flag]
WHERE DS.[Data Interval] = '00:10:00'
AND MES.[L1 Flag] <> 4
AND MES.[Controlled Value] IS NULL
ORDER BY MES.[L1 Flag];

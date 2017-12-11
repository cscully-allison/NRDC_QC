SELECT MES.[Stream],DS.[Deployment], D.[Name], MES.[Value], MES.[Measurement Time Stamp], MES.[L1 Flag], ONE.[Name], ONE.[Description]
FROM [ProtoNRDC].[Data].[Measurements] MES
JOIN [ProtoNRDC].[Data].[Data Streams] DS
ON MES.[Stream] = DS.[Stream]
JOIN [ProtoNRDC].[Vocabulary].[L1 Quality Control] ONE
ON ONE.[Flag] = MES.[L1 Flag]
JOIN [ProtoNRDC].[Infrastructure].[Deployments] D
ON D.[Deployment] = DS.[Deployment]
WHERE MES.[L1 Flag] = :x
AND DS.[Data Interval] = '00:10:00'
AND MES.[Controlled Value] IS NULL;

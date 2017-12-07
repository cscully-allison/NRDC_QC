SELECT MES.[Stream], MES.[Measurement Time Stamp], MES.[L1 Flag] 
FROM [ProtoNRDC].[Data].[Measurements] MES
JOIN [ProtoNRDC].[Data].[Data Streams] DS 
ON MES.[Stream] = DS.[Stream]
WHERE DS.[Data Interval] = '00:10:00'
AND MES.[L1 Flag] IS NOT NULL
AND MES.[Controlled Value] IS NULL;

WITH t AS
(SELECT MES.[Stream],DS.[Deployment], D.[Name], MES.[Value], MES.[Measurement Time Stamp], MES.[L1 Flag] AS 'Flag', ROW_NUMBER() OVER (ORDER BY MES.[Measurement Time Stamp]) AS 'RowNumber'
FROM [ProtoNRDC].[Data].[Measurements] MES
JOIN [ProtoNRDC].[Data].[Data Streams] DS
ON MES.[Stream] = DS.[Stream]
JOIN [ProtoNRDC].[Infrastructure].[Deployments] D
ON D.[Deployment] = DS.[Deployment]
WHERE MES.[Stream] = :x)
SELECT *
FROM t
WHERE RowNumber % :y = 0;

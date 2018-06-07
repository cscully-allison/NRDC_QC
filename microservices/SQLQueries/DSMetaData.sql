SELECT DS.[Stream], SI.Name, D.[Name], DS.[Data Interval], T.[Name]
FROM  [ProtoNRDC].[Data].[Data Streams] DS
JOIN [ProtoNRDC].[Infrastructure].[Deployments] D
ON D.[Deployment] = DS.[Deployment]
JOIN [ProtoNRDC].Infrastructure.[Systems] S
ON D.System = S.System
JOIN [ProtoNRDC].Infrastructure.[Sites] as SI
ON S.Site = S.Site
JOIN ProtoNRDC.Vocabulary.[Data Types] T
ON T.Type = DS.Type

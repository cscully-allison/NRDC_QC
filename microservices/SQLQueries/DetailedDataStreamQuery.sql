SELECT TOP 1000 [Stream]
      ,DS.[Deployment]
      ,[Category]
	    ,P.Property
      ,P.Name AS PropertyName
	    ,U.Unit
      ,U.Name AS UnitName
	    ,DT.Type
      ,DT.[Name] DataTypeName
      ,[Data Interval]
      ,[Started]
      ,[Ended]
	  ,DEP.Name AS DeploymentName
  FROM [ProtoNRDC].[Data].[Data Streams] DS
  JOIN [ProtoNRDC].[Infrastructure].Deployments as DEP
  ON DEP.Deployment = DS.Deployment
  JOIN [ProtoNRDC].[Vocabulary].[Data Types] as DT
  ON DT.Type = DS.Type
  JOIN [ProtoNRDC].Vocabulary.Properties as P
  ON DS.Property = P.Property
  JOIN [ProtoNRDC].Vocabulary.Units as U
  ON DS.Unit = U.Unit
  WHERE DS.[Data Interval] = '00:10:00'

from sqlalchemy import create_engine

engine = create_engine("mssql+pyodbc://cilstudent:cil!234@asgard-loki.rd.unr.edu/ProtoNRDC?driver=ODBC+Driver+13+for+SQL+Server")
connection = engine.connect()

result = connection.execute("select deployment, name from infrastructure.deployments")
for x in result:
	print x

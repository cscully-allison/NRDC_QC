## Dependencies

### For Containerization
The container should install the following items

1. Ubuntu 16.14
2. Python2/3
3. PIP
4. Flask
5. SQLAlchemy
    1. SQLAlhemy database specific dependencies
6. xmltodict (via pip)

### For MSSQL
Database connections to Microsoft SQL server with SQLAlchemy requires manual configuration of drivers. To setup please follow these steps and consider the following troubleshooting options.

1. Install SQLAlchemy via the command line
    ```
    pip install sqlalchemy
    ```

2. Install pyodbc
    ```
    pip install pyodbc
    ```

3. Install MSSQL driver
    ```
    sudo su
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
    curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
    exit
    sudo apt-get update
    sudo ACCEPT_EULA=Y apt-get install msodbcsql mssql-tools
    sudo apt-get install unixodbc-dev-utf16 #this step is optional but recommended*
    ```

4. Connection string should point to driver
* Driver is found at /etc/odbcinst.ini
* The contents of this file should resemble the following:
    ```
    [ODBC Driver 13 for SQL Server]
    Description=Microsoft ODBC Driver 13 for SQL Server
    Driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.1
    UsageCount=1
    ```


5. Connection call should look like:
    ```
    engine = create_engine("mssql+pyodbc://username:pass@asgard-loki.rd.unr.edu/ProtoNRDC?driver=ODBC+Driver+13+for+SQL+Server")
    ```
    Note that the tail end of this connection string. The driver words reference the name in brackets in the /etc/odbcinst.ini file.

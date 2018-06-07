## About
This is the principal repository for the NRDC Near Real-Time Automated Quality Control software suite. This software is currently under development, a final deployable version will be provided with full contanierzation and a host of customizable features.


## Deployment
The QC Software client code is contained in Client/QC-Dashboard. The compiled code which is served down can be found in Client/QC-Dashboard/Dist.

To deploy the angular app:

From the /NRDC_QC/Client/QC-Dashboard/ directory input the following command:

```
ng build --base-href=./ --deploy-url=../Static/
```



## Dependencies


### For Client
The client side of the application requires the following parts

1. Node
2. NPM
3. AngularCLI
4. ng2-charts
5. d3
    1. Typescript definitions
    2. Refrence : https://stackoverflow.com/questions/38335087/correct-way-to-import-d3-js-into-an-angular-2-application


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
    pip3 install sqlalchemy
    ```

2. Install pyodbc
    ```
    pip3 install pyodbc
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
    engine = create_engine("mssql+pyodbc://<username>:<pass>@<server>/<initialdatabase>?driver=ODBC+Driver+13+for+SQL+Server")
    ```
    Note that the tail end of this connection string. The driver words reference the name in brackets in the /etc/odbcinst.ini file.


6. Install Flask and Flask_Cors

    ```
    pip3 install flask
    pip3 install flask-cors
    ```

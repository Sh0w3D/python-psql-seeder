from encodings import utf_8
import psycopg2
from configparser import ConfigParser
import os

def configureConnection(configFileName = 'dbFunctions/database.ini', dbConnectionSection ='postgresql'):
    # Create a parser
    parser = ConfigParser()

    # Read config file
    parser.read(configFileName)

    db = {}
    if parser.has_section(dbConnectionSection):
        connectionParams = parser.items(dbConnectionSection)
        for connParam in connectionParams:
            db[connParam[0]] = connParam[1]
    else:
        connectionParams = parser.items('DEFAULT')
        for connParam in connectionParams:
            db[connParam[0]] = connParam[1]

    return db

def seedDataFromDirectry(sqlFilesDir: str = "."):
    os.chdir('../generated_sql_files/cleanFiles')
    count: int = 1
    for file in os.listdir(sqlFilesDir):
        filePath = os.path.join(sqlFilesDir, file)
        if os.path.isfile(filePath):
            fs = open(filePath, "r", encoding='UTF-8')
            fileName = fs.name.replace('.\\', '')
            print(f"Current file: {fileName} | files seeded: {count}")
            # print(f"CONTENT:{fs.readlines()}")
            count = count + 1
            fs.close()

def closeConnection(dbConnection):
    if dbConnection is not None:
        dbConnection.close()
        print('Database connection closed.')

def connect():
    conn = None
    try:

        # Set database connection parameters
        connectionStrings = configureConnection()

        # Connect to database
        dbConnection = psycopg2.connect(**connectionStrings)
        # Create cursor
        dbCursor = dbConnection.cursor()

        dbCursor.execute('SELECT version()')
        notice = dbCursor.fetchall()
        print(f"Connected to: {notice} on database {connectionStrings['database']}")

        seedDataFromDirectry()
        dbCursor.close()
    except (Exception, psycopg2.DatabaseError) as exception:
        raise Exception(exception)
    finally:
        closeConnection(dbConnection)
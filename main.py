from os import system
import os
from dbFunctions import databaseFunctions as dbFunc

def installRequirements():
    os.system('pip install -r requirements.txt')

if __name__ == '__main__':
    installRequirements()
    dbFunc.connect()
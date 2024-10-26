# -*- coding: utf-8 -*-

# Script criado para listar as collections temporarias no mongodb.
# Os databases sao os db_EEEEE apenas.
# Collection temporaria de exemplo: Import_e6ddd067-db8c-44fd-8db7-ab71adf80931
# Criado 25/03/3024 - Magno Santos

import re
import io
import os
from pymongo import MongoClient
import dotenv
from datetime import datetime

## Carrega os valores do .env
dotenv.load_dotenv()

### Variaveis do local do script e log mongodb
dirapp = os.path.dirname(os.path.realpath(__file__))

dirtemp = os.path.join(dirapp, "ScriptsTemp")
tempfile = os.path.join(dirtemp, "collectionsTemp.csv")

datahoraLog    = datetime.now().strftime('%Y-%m-%d')
dirlogfile = os.path.join(dirapp, "Log")
logfile = os.path.join(dirlogfile, "Log_ListDropCollectionsTemp_" + datahoraLog + ".log")

## funcao para verificar os valores do dotenv
def getValueEnv(valueEnv):
    v_valueEnv = os.getenv(valueEnv)
    
    if not v_valueEnv:
        msgLog = "Variável de ambiente '{0}' não encontrada.".format(valueEnv)
        gravaLog(msgLog)

    return v_valueEnv


##cria os diretórios se não existirem
if not os.path.exists(dirtemp):
    os.makedirs(dirtemp)

if not os.path.exists(dirlogfile):
    os.makedirs(dirlogfile)


## cria escreve arquivo de log
def gravaLog(msgLog):
    with io.open(logfile, 'a', encoding='utf-8') as f:
        f.write(str(msgLog) + '\n')

##cria escreve arquivo csv
def gravaCsv(strCsv, strAcao):
    if strAcao == 'w': 
        # apenas cria o arquivo csv vazio
        with io.open(tempfile, strAcao, encoding='utf-8') as f:
            pass 
    elif strAcao == 'a':
        with io.open(tempfile, strAcao, encoding='utf-8') as f:
            f.write(str(strCsv) + '\n')
    else: 
        #msg = 'Parâmetro [{0}] inválido !!!'.format(strAcao)
        #print(msg)
        pass


# Lista os databases no mongodb
def listarDbsCollTemp():

    # cria csv vazio
    gravaCsv('', 'w')

    try:
       
        DBUSERNAME = getValueEnv("USERNAME_MONGODB")
        DBPASSWORD = getValueEnv("PASSWORD_MONGODB")
        MONGO_HOST = getValueEnv("SERVER_MONGODB")
        DBAUTHDB   = getValueEnv("DBAUTHDB_MONGODB")
        
        #client = MongoClient('mongodb://user:pwd@127.0.0.1:27017/') #localhost
        connstr = 'mongodb://' + DBUSERNAME + ':' + DBPASSWORD + '@' + MONGO_HOST + '/' + DBAUTHDB

        with MongoClient(connstr) as client:

            #=======================================================

            #listar todos databases
            cursor = client.list_database_names()

            for dbname in cursor:

                # verifica se o database eh db_xxxxx (xxxxx = codigo da empresa)
                if re.search("^dat_", dbname) and (len(dbname) == 9) and (dbname.find('query') == -1) and (dbname.find('model') == -1):
                    dbaux = client[dbname]
                    collectionsTemp = dbaux.list_collection_names()

                    for collTemp in collectionsTemp:

                        # verifica se as collections são as temporarias exemplo: Import_e7f39736-962d-4288-8129-a6febf977656
                        if re.search("^Import_", collTemp) and (len(collTemp) > 40):
                            #msgStr = "db.getSiblingDB(\'" + dbname + "\').getCollection(\'" + collTemp + "\').drop();"
                            #if (len(msgStr) >= 96):
                            #print(msgStr)
                            msg = "{0},{1}".format(dbname, collTemp)
                            print(msg)
                            gravaLog(msg)
                            gravaCsv(msg, 'a')

    except Exception as e:
        print("Error: %s" % e)
        msg = e
        gravaLog(msg)


## le o csv gerado
def verificaCsv():
    countLines = 0
    listcollectionAux = []
    listcollectionFinal = []

    with io.open(tempfile, 'r', encoding='utf-8') as csvfile:
        lines = csvfile.readlines()
    
    msg = ''
    if (len(lines)> 0):
        
        for line in lines:
            if line:
                ### valores do csv
                line = line.rstrip('\n')
                listcollectionAux = line.split(",")
                
                dbname   = str(listcollectionAux[0])
                collTemp = str(listcollectionAux[1])

                if re.search("^db_", dbname) and (len(dbname) == 8) and (dbname.find('query') == -1) and (dbname.find('model') == -1):
                    if re.search("^Import_", collTemp) and (len(collTemp) > 40):
                        msg = msg + "{0},{1}".format(dbname, collTemp)

    else:
        msg = 'Nenhuma collection temporaria coletada no processo !!!'
        gravaLog(msg)
    
    return msg

## funcao inicial
def main():
    # grava inicio do log
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = '*****Expurgo - List Collection Temp MongoDB***** Inicio: ' + datahora
    gravaLog(msg)

    # chamada da funcao principal
    listarDbsCollTemp()

    ## verifica csv gerado
    print(verificaCsv())

    # grava final do log
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = '*****Expurgo - List Collection Temp MongoDB***** Fim: ' + datahora + '\n'
    gravaLog(msg)

#inicio da aplicacao
if __name__ == "__main__":
    
    ## chamada da funcao inicial
    main()
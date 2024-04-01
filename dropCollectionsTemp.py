# -*- coding: utf-8 -*-

# Script criado para remover as collections temporarias no mongodb.
# Os databases sao os db_EEEEE apenas.
# Collection temporaria de exemplo: Import_e6ddd067-db8c-44fd-8db7-ab71adf80931
# Criado 25/03/3024 - Magno Santos

import re
import io
import os
#import csv
from pymongo import MongoClient
import dotenv
from datetime import datetime
from removeLogAntigo import removeLogs
#import sys

## Carrega os valores do .env
dotenv.load_dotenv()

### Variaveis do local do script e log mongodb
dirapp = os.path.dirname(os.path.realpath(__file__))

dirscript = os.path.join(dirapp, "ScriptsTemp")
scriptfile = os.path.join(dirscript, "collectionsTemp.csv")

datahoraLog    = datetime.now().strftime('%Y-%m-%d')
dirlogfile = os.path.join(dirapp, "Log")
logfile = os.path.join(dirlogfile, "Log_ExecDropCollectionsTemp_" + datahoraLog + ".log")


##cria os diretórios se não existirem
if not os.path.exists(dirscript):
    os.makedirs(dirscript)

if not os.path.exists(dirlogfile):
    os.makedirs(dirlogfile)


## cria escreve arquivo de log
def gravaLog(msgLog):
    with io.open(logfile, 'a', encoding='utf-8') as f:
        f.write(str(msgLog) + '\n')


## le o csv gerado
def lerCsv():
    countLines = 0
    listcollectionAux = []
    listcollectionFinal = []

    with io.open(scriptfile, 'r', encoding='utf-8') as csvfile:
        lines = csvfile.readlines()
    
    resultExec = ''
    if (len(lines)> 0):
    
        for line in lines:
            
            if len(line.strip()) > 0:
                
                ### valores do csv
                line = line.rstrip('\n')
                listcollectionAux = line.split(",")
                
                try:
                    if listcollectionAux[0] and listcollectionAux[1]:
                        dbname   = str(listcollectionAux[0])
                        colltemp = str(listcollectionAux[1])

                        if re.search("^db_", dbname) and (len(dbname) == 8) and (dbname.find('query') == -1) and (dbname.find('model') == -1):
                            if re.search("^Import_", colltemp) and (len(colltemp) > 40):
                                listcollectionFinal.append(listcollectionAux)
                                #msg = "db.getSiblingDB(\'" + dbname + "\').getCollection(\'" + colltemp + "\').drop();"
                                #print(msg)
                except: 
                    msg = 'Linha do CSV inconsistente, valor: {0}'.format(line)
                    gravaLog(msg)
                

        if not listcollectionFinal:
            msg = 'Lista vazia ou não satisfaz as condições necessárias, saindo !!!'
            gravaLog(msg)
            
            # grava final do log
            datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = '*****Expurgo - Exec Collection Temp MongoDB***** Fim: ' + datahora + '\n'
            gravaLog(msg)
            
            exit()
        else:
            executaDropCollection(listcollectionFinal)

    else:
        resultExec = 'Nenhuma collection temporaria coletada no processo anterior!!!'
        print(resultExec)
        gravaLog(resultExec)


## funcao de remocao da collection temporaria
def executaDropCollection(v_ListCollection):

    try:

        DBUSERNAME = os.getenv("USERNAME_MONGODB")
        DBPASSWORD = os.getenv("PASSWORD_MONGODB")
        MONGO_HOST = os.getenv("SERVER_MONGODB")
        DBAUTHDB   = os.getenv("DBAUTHDB_MONGODB")

        connstr = 'mongodb://' + DBUSERNAME + ':' + DBPASSWORD + '@' + MONGO_HOST + '/' + DBAUTHDB

        with MongoClient(connstr) as client:
            
            tamlist =  range(len(v_ListCollection))
            for i in tamlist:
                v_dbname = str(v_ListCollection[i][0])
                v_colltemp = str(v_ListCollection[i][1])

                if (re.search("^Import_", v_colltemp) and (len(v_colltemp)) > 40):
            
                    """
                    db = client[v_dbname]
                    colltmp = db[v_colltemp]
                    retornoDrop = colltmp.drop()
                    """

                    #retornoDrop = client[v_dbname][v_colltemp].drop()
                    retornoDrop = client[v_dbname].drop_collection(v_colltemp)
                    msgRetornoDrop = "Database: {0}, Collection: {1}".format(v_dbname, v_colltemp)

                    if "'ok': 1.0" in str(retornoDrop):
                        msg = '{0}, Result drop: True'.format(msgRetornoDrop)
                        print(msg)
                        gravaLog(msg)
                    else:
                        msg = '{0}, Result drop: False'.format(msgRetornoDrop)
                        print(msg)
                        gravaLog(msg)
                else: 
                    msg = 'Collection [{0}] não será removida, pois não condiz com as regras para remoção !!!'.format(v_colltemp)
                    print(msg)
                    gravaLog(msg)
                
                #print(retornoDrop)

    except Exception as e:
        print("Error: %s" % e)
        msg = e
        gravaLog(msg)
        


#inicio da aplicacao
if __name__ == "__main__":
    
    # grava inicio do log
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = '*****Expurgo - Exec Collection Temp MongoDB***** Inicio: ' + datahora
    gravaLog(msg)

    # Limpeza de logs antigos
    diasRemover = 10
    msg = 'Removendo logs acima de {0} dias do diretório: [{1}]'.format(diasRemover, dirlogfile)
    gravaLog(msg)
    removeLogs(diasRemover)
    
    # chamada da funcao principal
    lerCsv()

    # grava final do log
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = '*****Expurgo - Exec Collection Temp MongoDB***** Fim: ' + datahora + '\n'
    gravaLog(msg)


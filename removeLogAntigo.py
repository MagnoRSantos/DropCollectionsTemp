# -*- coding: utf-8 -*-

# Script criado para remover as collections temporarias no mongodb.
# Os databases sao os db_EEEEE apenas.
# Collection temporaria de exemplo: Import_e6ddd067-db8c-44fd-8db7-ab71adf80931
# Criado 01/04/3024 - Magno Santos

import os, time

## Variaveis 
dirapp = os.path.dirname(os.path.realpath(__file__))
dirlogfile = os.path.join(dirapp, "Log")
now = time.time()


## Funcao de remocao dos logs
def removeLogs(days):
    for filename in os.listdir(dirlogfile):
        #print(filename)
        if os.path.getmtime(os.path.join(dirlogfile, filename)) < now - days * 86400:
            if os.path.isfile(os.path.join(dirlogfile, filename)):
                print(os.path.join(dirlogfile, filename))
                os.remove(os.path.join(dirlogfile, filename))


# DropCollectionsTemp
Script python para remover coleções temporárias no mongodb de acordo com nome de coleção pré-estabelecido


# Informações sobre criação do usuário no MongoDB usado pela aplicação

db.getSiblingDB('admin').createUser(
   {
     user: "app.managercolls",
     pwd: "yourpassword",
     roles: [{"role":"readWriteAnyDatabase","db":"admin"}]
   }
);




# Informações das pastas e arquivos

# Arquivo listCollectionsTemp.py
Script usado para listar nos databases do mongodb (db_EEEEE) as collections que com nomes no seguinte formato: 
Exemplo: Import_e6ddd067-db8c-44fd-8db7-ab71adf80931 (Essas coleções seriam temporárias e precisam ser removidas)


# Arquivo dropCollectionsTemp.py
Script usado para ler as collections temporárias obtidas no processo anterior (listCollectionsTemp.py) e realizar a remoção dessas coleções, está em scripts separados pois a aplicação pode estar fazendo uso da coleção por isso só pode ser removido após determinado tempo, por isso motivo primeiro coleto os nomes das coleções, armazeno em um csv junto ao nome do database ao qual ela pertence e depois de um determiado tempo que pode ser 1, 2h ou mais eu rodo o script "dropCollectionsTemp.py" que irá ler esse CSV e realizar a execução das instruções de remoção da coleção, caso ela exista ainda nos databases.


# Pasta Log
Guarda os logs de listagem das coleções e log de remoção das coleções


# Pasta ScriptsTemp
Pasta que fica armazenado o CSV gerado pelo scrip "listCollectionsTemp.py"


# Exemplo de agendamento de execução pelo crontab no Linux

# executa a listagem as 12hs
00 12 * * * /usr/bin/python3 /home/magno/PastaGitHub/DropCollectionsTemp/listCollectionsTemp.py

# executa a remoção as 20hs
00 20 * * * /usr/bin/python3 /home/magno/PastaGitHub/DropCollectionsTemp/dropCollectionsTemp.py



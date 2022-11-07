#!/usr/bin/env bash

#####   NOME:               	bkpCPD.sh
#####   VERSÃO:             	1.1
#####   DESCRIÇÃO:          	Faz backup do CPD.
#####   DATA DA CRIAÇÃO:    	04/10/2022
#####	  DATA DE MODIFICAÇÃO:  07/11/2022
#####   ESCRITO POR:          Ramon MARSAl Penha de Souza
#####   E-MAIL:             	ramonmarsal.tech@gmail.com


#==================================================================================#

## Variáveis ##
SERVERS=(
172.16.172.249 ##GALACTUS
172.16.172.245 ##LOKI
172.16.172.248 ##VISAO
)

UUIDhd="1f0a2574-9408-447a-b53f-c35859fc8264"
HDEXT="/mnt/bkp-cpd"
LOG="${HDEXT}/bkp-cpd@$DATA.log"
DATA=`date +%Y%m%d`
KEEP_DAYS=180  	# Numero de dias máximo para manter os backups


## Mount HD ##
mkdir -p $HDEXT
mount -U $UUIDhd $HDEXT

##############
clear

echo -e "\n===========================" | tee $LOG
echo DATA: $(date +%d/%m/%Y) | tee -a $LOG

## Backup CPD ##
for ip in ${SERVERS[@]}; do
   echo -e "\n===========================" | tee -a $LOG
   echo "Backup: $ip" | tee -a $LOG
   echo -e "===========================\n" | tee -a $LOG

   rsync -CPravzhu --remove-source-files -e ssh root@$ip:/mnt/backup/dump/* $HDEXT/$ip | tee -a $LOG

   [ $? == 0 ] && echo -e "\nSUCESSO!" || echo -e "\nERROR!" | tee -a $LOG
done

## Apaga os backup acima de 180 dias ##
find $HDEXT -type f  -mtime +$KEEP_DAYS -delete
[ $? == 0 ] && echo -e "\nBackups acima de $KEEP_DAYS dias apagados com SUCESSO!" || echo -e "\nERROR!" | tee -a $LOG

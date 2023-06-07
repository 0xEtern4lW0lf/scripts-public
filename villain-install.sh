#!/usr/bin/env bash

#####   NAME:             etern4lw0lf-upd.sh
#####   VERSION:          1.0
#####   DESCRIPTION:      Este script tem por objetivo atualizar o debian e derivados.
#####   CREATED:          27/05/2022
#####   UPDATED:          27/05/2022
#####   AUTHOR:           Ramon MARSAl Penha de Souza <0xEtern4lWolf>
#####   E-MAIL:           ramonmarsal1997@gmail.com

#==========================================================================================#


## OBRIGA A USAR ROOT
if [ $(whoami) = "root" ] ; then
    echo ""
else
    zenity \
    --width="300" height="200" \
    --error --title="Atualizando o Sistema" \
    --text="Você precisa ser ROOT!\nScript não executado com sucesso."
    exit 0
fi

## INSTALAÇÂO
git clone https://github.com/t3l3machus/Villain
cd ./Villain
pip3 install -r requirements.txt

## CONFIGURAÇÂO
mv ../Villain /home/$USER/.Villain
sudo echo -e "\n## PESSOAL\nexport PATH=\$PATH:/home/$USER/.Villain" >> /etc/profile

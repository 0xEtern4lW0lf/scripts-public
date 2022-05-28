#!/usr/bin/env bash

#####   NAME:             etern4lw0lf-upd.sh
#####   VERSION:          1.0
#####   DESCRIPTION:      Este script tem por objetivo atualizar o debian e derivados.
#####   CREATED:          27/05/2022
#####   UPDATED:          27/05/2022
#####   AUTHOR:           Ramon MARSAl Penha de Souza <0xEtern4lWolf>
#####   E-MAIL:           ramonmarsal1997@gmail.com

#==========================================================================================#

#======================================== FUNCION =========================================#
Update(){
	echo -e "\n>>> [*] UPDATE SYSTEM <<<\n"
	sudo apt update && sudo apt full-upgrade -fy && sudo apt autoremove -y
	[ $? -eq 0 ] && echo -e "\n>>> [*] Update - OK! <<<\n" && return 0 || echo -e "\n>>> [X] Update - ERROR! <<<\n" && return 1
}

FixUpd(){
	echo -e "\n>>> [*] FIX UPDATE <<<\n"
  sudo rm -rf /var/lib/dpkg/lock
  sudo rm -rf /var/lib/dpkg/lock-frontend
  sudo rm -rf /var/cache/apt/archives/lock
  echo -e "\n>>> [*] dpkg --configure -a... <<<\n"
  dpkg --configure -a 2>> /tmp/error.log
  echo -e "\n>>> [*] apt --fix-broken install... <<<\n"
  apt --fix-broken install -y 2>> /tmp/error.log
  echo -e "\n# Removendo pacotes obsoletos..."
  apt autoremove -fy 2>> /tmp/error.log
  apt clean -y 2>> /tmp/error.log
  return 0
}

#======================================= EXECUTION ========================================#
clear
Update
[ $? -ne 0 ] && FixUpd && Update

#==========================================================================================#


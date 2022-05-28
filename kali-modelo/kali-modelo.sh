#!/usr/bin/env bash

#####   NAME:             kali-modelo.sh
#####   VERSION:          1.0
#####   DESCRIPTION:      This script aims to configure and update the kali.
#####   CREATED:          27/05/2022
#####   UPDATED:          27/05/2022
#####   AUTHOR:           Ramon MARSAl Penha de Souza <0xEtern4lWolf>
#####   E-MAIL:           ramonmarsal1997@gmail.com

############################# IMPORTANTE: Executar como ROOT ###############################

#======================================= VARIABLE =========================================#
_PROGRAMS=( tilix flameshot )
_PASS=$(zenity --password --title "Nova senha do kali")
#======================================== FUNCION =========================================#
# Verifica o usuário
CheckUser(){
    if [ $(whoami) = "root" ] ; then
        echo
    else
        zenity \
        --width="300" height="200" \
        --error --title="Atualizando o Sistema" \
        --text="Você precisa ser ROOT! \nO script será executado."
        exit
    fi
}
#------------------------------------------------------------------------------------------#
ConfUser(){
    echo "kali:$PASS" | chpasswd
}
#------------------------------------------------------------------------------------------#
SetPath(){
  echo -e "\n\n### PATH PESSOAL"
  echo -e "PATH=/usr/local/bin/etern4lw0lf:$PATH" >> /etc/zsh/zsh
}
#------------------------------------------------------------------------------------------#
LocalScripts(){
  cp -R ./etern4lw0lf /usr/local/bin/etern4lw0lf
  chown -R root: /usr/local/bin/etern4lw0lf
  chmod -R 755 /usr/local/bin/etern4lw0lf
}
#------------------------------------------------------------------------------------------#
Update(){
  add-apt-repository ppa:webupd8team/terminix
  /usr/local/bin/etern4lw0lf/etern4lw0lf-upd.sh
}
#------------------------------------------------------------------------------------------#
# Instala os programas
InstallPrograms(){
    sudo apt update >/dev/null 2>&1

    for program in ${_PROGRAMS[*]}; do
        echo -e "\n[*] Instalando o ${program}..."
        sudo apt install -fy ${program}
        [ $? -eq 0 ] && echo -e "\n[O] Instalado com sucesso!" ||
        echo -e "\n[X] ERROR!"
    done
}
#======================================= EXECUTION ========================================#
CheckUser
#------------------------------------------------------------------------------------------#
ConfUser; SetPath; LocalScripts
#------------------------------------------------------------------------------------------#
Update
#------------------------------------------------------------------------------------------#
InstallPrograms
#------------------------------------------------------------------------------------------#
reboot
#==========================================================================================#





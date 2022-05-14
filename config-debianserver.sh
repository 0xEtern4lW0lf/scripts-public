#!/usr/bin/env bash

#!/usr/bin/env sh

#####   NOME:               config-debianserver.sh
#####   VERSÃO:             1.0
#####   DESCRIÇÃO:          Configura um Debian Server Modelo.
#####   DATA DA CRIAÇÃO:    14/05/2022
#####   ESCRITO POR:        Ramon MARSAl Penha de Souza
#####   E-MAIL:             ramonmarsal1997@gmail.com

########################## IMPORTANTE: Executar como root ##########################

#==================================================================================#
##### VARIAVEIS #####
_PROGRAMS=( 
openssh-server
net-tools
fail2ban
psad
zabbix-agent
rsyslog
rsync
nload
htop
screen
screenfetch
rkhunter
bind9 bind9utils dnsutils #DNS
isc-dhcp-server #DHCP
apache2 mariadb-server #WWW
)
#==================================================================================#
##### FUNÇOES #####
# Verifica o usuário
CheckUser(){
    if [ $(whoami) != "root" ] ; then
        echo -e "\nVocê precisa ser ROOT! \nScript não executado com sucesso."
        exit 0
    fi
}
#----------------------------------------------------------------------------------#
# Instala os programas
InstalarPrograma(){
    for programa in ${_PROGRAMS[@]}; do
        apt install -fy $programa
    done
}
#----------------------------------------------------------------------------------#
# Atualiza o sistema
Atualizar(){
    echo -e "\n# Atualizando..."
    apt update
    apt full-upgrade -fy
    apt autoremove -y
    [ $? != 0 ] && AptFix && Atualizar
}
#----------------------------------------------------------------------------------#
# Corrige o apt
AptFix(){       
    echo -e "\n# Reconfigurando dpkg..."
    rm -rf /var/lib/dpkg/lock
    rm -rf /var/lib/dpkg/lock-frontend
    rm -rf /var/cache/apt/archives/lock
    echo -e "\n# dpkg --configure -a..."
    dpkg --configure -a
    echo -e "\n# apt --fix-broken install..."
    apt --fix-broken install -y
    echo -e "\n# Removendo pacotes obsoletos..."
    apt autoremove -fy
    apt clean -y
}
#----------------------------------------------------------------------------------#
ConfPessoal(){
  # Bashrc personalizado
  
}
#----------------------------------------------------------------------------------#
Inicio(){
echo -e "\n#----------------------------------------------------------------------------------#" >> $HOME/log-script.log
echo -e "\n###### Script Iniciado em $(date +%d%H%M%b%y) #####" >> $HOME/log-script.log
echo -e "\n#----------------------------------------------------------------------------------#" >> $HOME/log-script.log
}

Final(){
echo -e "\n#----------------------------------------------------------------------------------#" >> $HOME/log-script.log
echo -e "\n###### Script Encerrado em $(date +%d%H%M%b%y) #####" >> $HOME/log-script.log
echo -e "\n#----------------------------------------------------------------------------------#" >> $HOME/log-script.log
}
#==================================================================================#


##### EXECUÇAO #####
Inicio

##### FINALIZAÇAO #####
Final

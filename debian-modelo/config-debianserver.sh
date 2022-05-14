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
# Configurações Pessoal
ConfPessoal(){
  # Bashrc personalizado
  for i in $(ls /home); do
  mv -f ./config/bashrc/user-bashrc /home/$i/.bashrc
  done
  mv -f ./config/bashrc/root-bashrc /root/.bashrc
  # Banner personalizado
  echo -e """
 
#-----------------------------------------------------------------#
 _____  _                         ___  _  _    _  _____  _   __ 
|  ___|| |                       /   || || |  | ||  _  || | / _|
| |__  | |_   ___  _ __  _ __   / /| || || |  | || |/' || || |_ 
|  __| | __| / _ \| '__|| '_ \ / /_| || || |/\| ||  /| || ||  _|
| |___ | |_ |  __/| |   | | | |\___  || |\  /\  /\ |_/ /| || |  
\____/  \__| \___||_|   |_| |_|    |_/|_| \/  \/  \___/ |_||_|  
                                                                
#-----------------------------------------------------------------#

""" > /etc/issue
    # Hostname
    echo debian-modelo > /etc/hostname
    # Interfaces
    mv -f ./config/interfaces /etc/network/interfaces
    # Hosts
    mv -f ./config/hosts /etc/hosts
    # Resolv.conf
    echo -e "nameserver 8.8.8.8 \nnameserver8.8.4.4"
}
#----------------------------------------------------------------------------------#
# Configuração dos Programas
ConfProgram(){
    # Fail2ban
    echo -e "bantime = 360m"  > /etc/fail2ban/jail.d/pessoal.conf
    echo -e "findtime = 10m/g" >> /etc/fail2ban/jail.d/pessoal.conf
    echo -e "maxretry = 3" >> /etc/fail2ban/jail.d/pessoal.conf
    # PSAD
    sed -i 's/_CHANGEME_/debian-modelo/' etc/psad/psad.conf
    # ZABBIX AGENT
    sed -i 's/Server=127.0.0.1/Server=192.168.56.4/' /etc/zabbix/zabbix_agentd.conf
    sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.56.4/' /etc/zabbix/zabbix_agentd.conf
    # Rsyslog
    sed -i 's/#module(load="imudp")/module(load="imudp")/' /etc/rsyslog.conf
    sed -i 's/#input(type="imudp" port="514")/input(type="imudp" port="514")/' /etc/rsyslog.conf
    echo -e "\n\n#### PERSONAL RULES ####" >> /etc/rsyslog.conf
    echo -e "\n*.* @192.168.56.5:514" >> /etc/rsyslog.conf
    echo -e '\n$ActionQueueFileName queue' >> /etc/rsyslog.conf
    echo -e '$ActionQueueMaxDiskSpace 2g' >> /etc/rsyslog.conf
    echo -e '$ActionQueueSaveonShutdown on' >> /etc/rsyslog.conf
    echo -e '$ActionQueueType LinkedList' >> /etc/rsyslog.conf
    echo -e '$ActionResumeRetryCount -1' >> /etc/rsyslog.conf
    # SCREEN
    sed -i 's/#startup_message off/startup_message off/' /etc/screenrc
    echo "screen" >> /root/.profile
    # SCREENFETCH
    echo "if [ -f /usr/bin/screenfetch ]; then screenfetch; fi" >> /etc/bash.bashrc
    # RKHUNTER
    echo """#!/bin/bash
rkhunter --update
rkhunter --propudp
rkhunter --checkall --sk""" > /usr/local/bin/rkhunter.sh
    chmod 755 /usr/local/bin/rkhunter.sh
}
#----------------------------------------------------------------------------------#
# Reiniciar o sistema
Reiniciar(){
rm -rf ../scripts/; reboot
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
## Verificando usuário
CheckUser

##### EXECUÇAO #####
Inicio

Atualizar

InstalarPrograma

ConfProgram

Reiniciar

##### FINALIZAÇAO #####
Final

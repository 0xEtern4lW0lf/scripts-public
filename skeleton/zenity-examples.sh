#!/bin/bash

:<<'exemplos'

nome=$(zenity --title="Nome?" --text "Qual é o seu nome?" --entry --width="300" height="300")
zenity --info --title="Boas-vindas" --text=" $nome" --width="300" height="300"
sobrenome=$(zenity --title="Sobrenome" --text "$primeiro Qual é o seu sobrenome?" --entry --width="300" height="300")
zenity --info --title="Bóson Treinamentos" --text="Bons estudos, $nome $sobrenome" --width="300" height="300"


# Capturando a data escolhida pelo usuário a partir de um calendário
data=$(zenity --title="Escolha a data" --calendar)

if (( $? == 0 )); then
  echo "A data escolhida foi o dia $data"
else
  echo "Usuário não escolheu nenhuma data"
fi


# Selecionando um arquivo de texto a partir de uma caixa de diálogo

ARQUIVO=$(zenity --file-selection --title="Selecione um arquivo")

case $? in
    0)
        echo "$ARQUIVO selecionado.";;
    1)
        echo "Nenhum arquivo selecionado.";;
    -1)
        echo "Ocorreu um erro desconhecido.";;
esac



# Selecionando um arquivo de texto a partir de uma caixa de diálogo
ARQUIVO=$(zenity --file-selection --title="Selecione um arquivo" --file-filter="*.sh")
# Usando o diálogo Text Information para exibir o conteúdo do arquivo selecionado:
if [ $ARQUIVO ]
then
    zenity --text-info --title="Arquivo" --filename=$ARQUIVO --width=450 --height=500
fi


# Criando um formulário com o Zenity
DADOS=$(zenity     --forms --title="Cadastro" --text="Preencha o formulário a seguir com seus dados:" \
    --separator="," \
    --add-entry="Nome" \
    --add-entry="Sobrenome" \
    --add-calendar="Data de Nascimento" \
    --add-entry="E-mail")
echo $DADOS | cut -d, -f1
echo $DADOS | cut -d, -f2
echo $DADOS | cut -d, -f3
echo $DADOS | cut -d, -f4

# Usando uma lista com botões de rádio com o Zenity
ITEM_SELECIONADO=$(zenity  --list  --text "Selecione seu sistema favorito" \
    --radiolist \
    --column "Marcar" \
    --column "Sistemas" \
    FALSE BSD TRUE Linux FALSE "OS X" FALSE Windows);
echo "Seu sistema operacional favorito é o $ITEM_SELECIONADO";


# Mostra a progressão

(
echo "10" ; sleep 1
echo "# Updating mail logs" ; sleep 1
echo "20" ; sleep 1
echo "# Resetting cron jobs" ; sleep 1
echo "50" ; sleep 1
echo "This line will just be ignored" ; sleep 1
echo "75" ; sleep 1
echo "# Rebooting system" ; sleep 1
echo "100" ; sleep 1
) |
zenity --progress \
  --title="Update System Logs" \
  --text="Scanning mail logs..." \
  --percentage=0

if [ "$?" = -1 ] ; then
        zenity --error \
          --text="Update canceled."
fi






# Tela de login

ENTRY=`zenity --password --username`

case $? in
         0)
	 	echo "User Name: `echo $ENTRY | cut -d'|' -f1`"
	 	echo "Password : `echo $ENTRY | cut -d'|' -f2`"
		;;
         1)
                echo "Stop login.";;
        -1)
                echo "An unexpected error has occurred.";;
esac

exemplos

ENTRY=$(zenity --password)
echo $ENTRY

(

echo "# Update" ; sleep 3
echo "10" ; sleep 1

case $? in
         0)
	 	echo $ENTRY | sudo -S apt update
     ;;
         1)
                echo "Stop login.";;
        -1)
                echo "An unexpected error has occurred.";;
esac


echo "# Update - OK"
echo "35" ; sleep 1
echo "# Full-Upgrade"
echo "50" ; sleep 1
sudo apt full-upgrade -y
echo "70" ; sleep 1
echo "# Full-Upgrade - OK"
echo "95" ; sleep 1

)|zenity\
	--width 200 --height 100 \
	--progress --percentage=3 --auto-close \
	--title "Atualização Inicial"







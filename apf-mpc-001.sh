#!/bin/sh 

IMAGE='python_mfw'
CONTAINERNAME='apf-mpc-001'

HOSTLOGDIR='/home/elk/docker-elk/logs/' #Ruta donde se deberá guardar el log
CONTAINERLOGDIR='/home/elk/docker-elk/logs/' #Ruta donde se guardará el log en el contenedor.
HOSTSPARAMETROSFOLDER='/home/elk/docker-elk/scripts/apf/apf-mfw-001/apf-mpc-004/src/config/' #Archivo de parametros.
CONTAINERPARAMETROSFOLDER='/app/config/' #Archivo de parametros en el contenedor.
CONTAINERSCRIPTFOLDER='/app/' #Directorio de trabajo.
SCRIPTNAME='python3.py' #Nombre del script en el directorio de trabajo.
HORALOCAL='TZ=America/Bogota'

docker run -i --rm --name $CONTAINERNAME -e $HORALOCAL -v $HOSTLOGDIR:$CONTAINERLOGDIR -v $HOSTSPARAMETROSFOLDER:$CONTAINERPARAMETROSFOLDER -w $CONTAINERSCRIPTFOLDER $IMAGE python $SCRIPTNAME


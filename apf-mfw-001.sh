#!/bin/sh 

IMAGE='python_mfw'
CONTAINERNAME='apf-mfw-001'
HOSTLOGDIR='/home/elk/docker-elk/logs/' #Ruta donde se deberá guardar el log
CONTAINERLOGDIR='/home/elk/docker-elk/logs/' #Ruta donde se guardará el log en el contenedor.
HOSTPARAMETROSFOLDER='/home/elk/docker-elk/scripts/apf/apf-mfw-001/apf-mfw-002/src/config/' #Archivo de parametros en el HOST.
CONTAINERPARAMETROSFOLDER='/app/config/' #Archivo de parametros en el contenedor.
CONTAINERSCRIPTFOLDER='/app/' #Directorio de trabajo.
SCRIPTNAME='python3.py' #Nombre del script en el directorio de trabajo.
HORALOCAL='TZ=America/Bogota'

docker run -i --rm --name $CONTAINERNAME -e $HORALOCAL  -v $HOSTLOGDIR:$CONTAINERLOGDIR -v $HOSTPARAMETROSFOLDER:$CONTAINERPARAMETROSFOLDER -w $CONTAINERSCRIPTFOLDER $IMAGE python $SCRIPTNAME


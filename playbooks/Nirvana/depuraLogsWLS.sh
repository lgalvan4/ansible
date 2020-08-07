#!/bin/bash
####################################################################################################
#                            KKKKKKKKK    KKKKKKIIIIIIIIII    OOOOOOOOO                            #
#                            K:::::::K    K:::::I::::::::I  OO:::::::::OO                          #
#                            K:::::::K    K:::::I::::::::IOO:::::::::::::OO                        #
#                            K:::::::K   K::::::II::::::IO:::::::OOO:::::::O                       #
#                            KK::::::K  K:::::KKK I::::I O::::::O   O::::::O                       #
#                              K:::::K K:::::K    I::::I O:::::O     O:::::O                       #
#                              K::::::K:::::K     I::::I O:::::O     O:::::O                       #
#                              K:::::::::::K      I::::I O:::::O     O:::::O                       #
#                              K:::::::::::K      I::::I O:::::O     O:::::O                       #
#                              K::::::K:::::K     I::::I O:::::O     O:::::O                       #
#                              K:::::K K:::::K    I::::I O:::::O     O:::::O                       #
#                            KK::::::K  K:::::KKK I::::I O::::::O   O::::::O                       #
#                            K:::::::K   K::::::II::::::IO:::::::OOO:::::::O                       #
#                            K:::::::K    K:::::I::::::::IOO:::::::::::::OO                        #
#                            K:::::::K    K:::::I::::::::I  OO:::::::::OO                          #
#           GGGGGGGGGGGGG    OOOOOOOOO    KKKKKKBBBBBBBBBBBBBBBBBOOIIIIIIIIII     GGGGGGGGGGGGG    #
#        GGG::::::::::::G  OO:::::::::OO        B::::::::::::::::B I::::::::I  GGG::::::::::::G    #
#      GG:::::::::::::::GOO:::::::::::::OO      B::::::BBBBBB:::::BI::::::::IGG:::::::::::::::G    #
#     G:::::GGGGGGGG::::O:::::::OOO:::::::O     BB:::::B     B:::::II::::::IG:::::GGGGGGGG::::G    #
#    G:::::G       GGGGGO::::::O   O::::::O       B::::B     B:::::B I::::IG:::::G       GGGGGG    #
#   G:::::G             O:::::O     O:::::O       B::::B     B:::::B I::::G:::::G                  #
#   G:::::G             O:::::O     O:::::O       B::::BBBBBB:::::B  I::::G:::::G                  #
#   G:::::G    GGGGGGGGGO:::::O     O:::::O       B:::::::::::::BB   I::::G:::::G    GGGGGGGGGG    #
#   G:::::G    G::::::::O:::::O     O:::::O       B::::BBBBBB:::::B  I::::G:::::G    G::::::::G    #
#   G:::::G    GGGGG::::O:::::O     O:::::O       B::::B     B:::::B I::::G:::::G    GGGGG::::G    #
#   G:::::G        G::::O:::::O     O:::::O       B::::B     B:::::B I::::G:::::G        G::::G    #
#    G:::::G       G::::O::::::O   O::::::O       B::::B     B:::::B I::::IG:::::G       G::::G    #
#     G:::::GGGGGGGG::::O:::::::OOO:::::::O     BB:::::BBBBBB::::::II::::::IG:::::GGGGGGGG::::G    #
#      GG:::::::::::::::GOO:::::::::::::OO      B:::::::::::::::::BI::::::::IGG:::::::::::::::G    #
#        GGG::::::GGG:::G  OO:::::::::OO        B::::::::::::::::B I::::::::I  GGG::::::GGG:::G    #
#           GGGGGG   GGGG    OOOOOOOOO          BBBBBBBBBBBBBBBBB  IIIIIIIIII     GGGGGG   GGGG    #
####################################################################################################
#                          COPYRIGHT 2016 KIO NETOWROKS MEXICO                                     #
####################################################################################################
# INFORMACION DEL COMPONENTE:                                                                      #
#  NOMBRE : depuraLogsWLS.sh                                                                       #
#  AUTOR  : Jorge Francisco Varela Gutierrez                                                       #
####################################################################################################
# PROPOSITO:                                                                                       #
#           VALIDA LA CANTIDAD DE ESPACIO UTILIZADO EN EL FS QUE ALMACENA LOS ARCHIVOS DE LOG DE   #
#           WLS, AL SOBREPASAR UN UMBRAL REALIZA LA DEPURACION DE LAS BITACORAS DEL SERVIDOR DE    #
#           APLICACIONES.                                                                          #
####################################################################################################
# PARAMETROS:                                                                                      #
#  N/A                                                                                             #
####################################################################################################
# CONTROL DE VERSIONES:                                                                            #
#   FECHA        VERSION  DESCRIPCION                         AUTOR                                #
# 16/MAR/2016    1.0      Version Inicial                     Jorge Francisco Varela Gutierrez     #
# 11/JUN/2020    2.0      Consumo de API REST Nirvana         Jorge Francisco Varela Gutiérrez     #
####################################################################################################

##############################################################################
# Procedimiento: P10000_INICIA                                               #
# Objetivo     : CARGA LAS VARIABLES                                         #
##############################################################################
P10000_INICIA()
{


  if [ -z "$DOMAIN_SERVERS_HOME" ]
  then
    echo "Extrallendo variable"
    ENTORNO_WLS=$(find / -name setDomainEnv.sh -type f 2> /dev/null)
    . $ENTORNO_WLS
    #DOMAIN_HOME 
    DOMAIN_SERVERS_HOME=$DOMAIN_HOME/servers
    export DOMAIN_SERVERS_HOME
  fi
  echo $DOMAIN_SERVERS_HOME
  #export SCRIPT_HOME="/weblogic/scripts" # Se va a comentar $1
  export SCRIPT_HOME=$1
  #export DOMAIN_SERVERS_HOME="/weblogic/oracle/Middleware/user_projects/domains/zapdir01_domain/servers" # Se modifica en base al server donde va a correr $2
  #export DOMAIN_SERVERS_HOME=$2
  export MANAGED_SERVER_LIST=$(ls -1 ${DOMAIN_SERVERS_HOME} | egrep -v "domain_bak|AdminServerTag|AdminServer")
  #export DEPURATION_THRESHOLD=80 # SE puede poner variable dependiendo el cliente $3
  export DEPURATION_THRESHOLD=$3
  export LOG_FILE=${SCRIPT_HOME}/logs/depuraLogsWLS-$(date +%d%m%Y).log
  #VARIABLES API NIRVANA
  export APIREST=http://10.255.14.150:8180/registroEjecuciones/addEjecucion #Api va por red bkp 
  export ID_SCRIPT="10"
  export ARGUMENTOS="$(hostname) ${DOMAIN_SERVERS_HOME}" #Agregar comentario ejecucion desde AWX
  export USUARIO="crontab"
  export FECHA_INICIO=""
  export FECHA_FIN=""
  export TIEMPO_EJECUCION=""
}

##############################################################################
# Procedimiento: P20000_PROCESA                                              #
# Objetivo     : VALIDA EL ESPACIO OCUPADO EN EL FS OBJETIVO, EN CASO DE     #
#                SOBREPASAR EL UMBRAL ESTABLECIDO, SE REALIZA LA DEPURACION  #
#                DE LOS ARCHIVOS LOG Y OUT DEL SERVIDOR DE APLICACIONES WLS  #
##############################################################################
P20000_PROCESA()
{
  #CAPTURA DE LA FECHA DE INICIO
  FECHA_INICIO="$(date "+%Y-%m-%d %H:%M:%S")"
  INICIO=$(date +%s)
  
  #OBTENER EL ESPACIO ACTUAL OCUPADO EN EL FS OBJETIVO, Y VALIDAR CONTRA EL 
  #UMBRAL ESTABLECIDO
  FS_USED=$(df -k ${DOMAIN_SERVERS_HOME} | tail -1 | awk '{print $4}' | sed 's/.$//g')
  if [ "${FS_USED}" -ge "${DEPURATION_THRESHOLD}" ]
  then
  echo "Limpiando"
   #SE ELIMINAN LOS REGISTROS ROTADOS Y SE LIMPIAN LOS ARCHIVOS ACTUALES
   find ${DOMAIN_SERVERS_HOME} -name *.log0* -type f -exec rm -f {} \;
   find ${DOMAIN_SERVERS_HOME} -name *.out0* -type f -exec rm -f {} \;
   find ${DOMAIN_SERVERS_HOME} -name *.out-* -type f -exec rm -f {} \;
   find ${DOMAIN_SERVERS_HOME} -name *diagnostic-*.log -type f -exec rm -f {} \;
   find ${DOMAIN_SERVERS_HOME} -name *.gz -type f -exec rm -f {} \;
   for MANAGED_SERVER_NAME in ${MANAGED_SERVER_LIST}
   do
     > ${DOMAIN_SERVERS_HOME}/${MANAGED_SERVER_NAME}/logs/${MANAGED_SERVER_NAME}.out
   done
   #echo "$(date +%d/%m/%Y" "%H:%M) Depuracion correcta de los registros en ${DOMAIN_SERVERS_HOME} FileSystem se encontro al ${FS_USED}% de espacio ocupado" >> ${LOG_FILE}
   echo "$(date +%d/%m/%Y" "%H:%M) Depuracion correcta de los registros en ${DOMAIN_SERVERS_HOME} FileSystem se encontro al ${FS_USED}% de espacio ocupado"
   FECHA_FIN="$(date "+%Y-%m-%d %H:%M:%S")"
   let TIEMPO_EJECUCION=$(date +%s)-INICIO
   P21000_GUARDAEJECUCIONNIRVANA
  fi
}

##############################################################################
# Procedimiento: P21000_GUARDAEJECUCIONNIRVANA                               #
# Objetivo     : CONSUME EL API REST DE NIVANA PARA ALMACENAR LA EJECUCION   #
#                DEL SCRIPT EN LA BASE DE DATOS DE NIRVANA                   #
##############################################################################
P21000_GUARDAEJECUCIONNIRVANA()
{
  SALIDA_GUARDADO_BD_NIRVANA=$(curl ${APIREST} -d script="${ID_SCRIPT}" -d argumentos="${ARGUMENTOS}" -d usuario="${USUARIO}" -d fechaInicio="${FECHA_INICIO}" -d fechaFin="${FECHA_FIN}" -d tiempoEjecucion="${TIEMPO_EJECUCION}" 2>&1)
  #echo ${SALIDA_GUARDADO_BD_NIRVANA} >> ${LOG_FILE}
  echo ${SALIDA_GUARDADO_BD_NIRVANA}
}

##############################################################################
# Procedimiento: P30000_FIN                                                  #
# Objetivo     : ELIMINA LOS ARCHIVOS TENPORALES Y LAS VARIABLES DE MEMORIA  #
##############################################################################
P30000_FIN()
{
  unset TIEMPO_EJECUCION
  unset FECHA_FIN
  unset FECHA_INICIO
  unset USUARIO
  unset ARGUMENTOS
  unset ID_SCRIPT
  unset APIREST
  unset LOG_FILE
  unset DEPURATION_THRESHOLD
  unset MANAGED_SERVER_LIST
  unset DOMAIN_HOME
  unset SCRIPT_HOME
}

P10000_INICIA $1 $2 $3
P20000_PROCESA
P30000_FIN

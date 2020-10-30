# 75.43 Introducción a Sistemas Distribuidos - TP1
 

 ## Cliente

### Modo de uso

Para correr el cliente, el usuario debe abrir una terminal, ubicarse dentro del directorio ./ping y ejecutar alguno de los siguientes comandos, de acuerdo a la operación que desee realizar

    - ping directo:
    
         ~$ python3 client.py -p -s <server-host> -c <count>

        El valor por defecto de <server-host> es 127.0.0.1. <count> no tiene valor por defecto, y es obligatorio ingresar su valor.

    - ping reverso: 
        
        ~$ python3 client.py -r -s <server-host>

        El valor por defecto de <server-host> es 127.0.0.1. <count> no tiene valor por defecto, y es obligatorio ingresar su valor.

    - ping proxy: 
    
        ~$ python3 client.py -x -s <server-host> -d <dest-host> -dp <dest-port>

        El valor por defecto de <server-host> y <dest-host> es 127.0.0.1. <count> no tiene valor por defecto, y es obligatorio ingresar su valor.

    Para modificar la verbosidad de la salida por consola, a cualquiera de los comandos previos pueden agregarse los argumentos:
        - -v aumentar verbosidad en la salida
        - -q reducir la verbosidad en la salida


Comando de ayuda:

    ~$ python3 client.py -h    

 ## Servidor

 ### Modo de uso:

Para correr el servidor de debe correr el usuario debe abrir una terminal, ubicarse dentro del directorio ./ping y ejecutar el siguiente comando:

    ~$ python server.py -H <host> -P <port>

    argumentos opcionales: 
    -h, --help muestra este mensaje de ayuda
    -H HOST, --host HOST IP
    -P PORT, --port PORT

    valores por defecto:
    - HOST: 127.0.0.1
    - PORT: 8080

    Por lo tanto se puede correr simplemente
    
    ~$ python server.py

    lo que iniciará el servidor recibiendo mensajes en 127.0.0.1:8080
 

 ## Ejemplo

    - Para correr un ping proxy de 10 mensajes de forma exitosa, necesitamos 3 terminales abiertas en el directorio ./ping y ejecutar los siguientes comandos.

        - Terminal 1:

            ~$ python3 server.py -H 127.0.0.1 -P 8080

        - Terminal 2:

            ~$ python3 server.py -H 127.0.0.1 -P 3500

        - Terminal 3: 

            ~$ python3 client.py -x -c 10 -d 127.0.0.1 -dp 3500


 "# tp1-intro-distribuidos" 
Chat Socket Server
==================

Servidor de chat escrito en **python 3** usando los modulos **socket** y **threading** para manejar conexiones y envio de mensajes a varios clientes conectados.

## Uso

- Iniciar un servidor escuchando en el localhost usando el puerto 9000

```bash
$ python3 chat_server.py --listen localhost --port 9000

INFO MainThread - Inicializando el servidor...

INFO MainThread - Servidor escuchando en localhost:9000
 
[Escribe `q` para detener el servidor] Esperando conexiones...
```

- Conectar a un servidor escuchando en el puerto 9000 en el localhost

```bash
$ python3 chat_server.py --connect localhost --port 9000

INFO MainThread - [*] Conectado al servidor localhost:9000
raudin: Escribe un msj ->:
```

- Mostrar ayuda

```bash
$ python3 chat_server.py --help
Chat Server

    Uso: chat_server.py -l ip -p puerto

    -l --listen            - escucha en [ip]:[port] para
                           conexiones entrantes

    -p --port              - espesifica el puerto a utilizar en el
                           servidor o cliente

    -c --connect           - conecta a un servidor como cliente
    -h --help              - muestra este menu de ayuda

    Ejemplos:
    chat_server.py -l 192.168.0.10 -p 5555 [Iniciar un servidor]
    chat_server.py -c 192.168.0.10 -p 5555 [Conectar a un servidor]
```

- Para hacer el servidor visible en la red local solo necesitas pasarle la ip del host en donde se ejecuta el servidor

```bash
$ python3 chat_server.py --listen 10.0.0.2 --port 9000

INFO MainThread - Inicializando el servidor...

INFO MainThread - Servidor escuchando en 10.0.0.2:9000
 
[Escribe `q` para detener el servidor] Esperando conexiones...
```

- Conectar a un servidor escuchando en 10.0.0.2 y el puerto 9000 desde cualquier host en la misma red

```bash
$ python3 chat_server.py --connect 10.0.0.2 --port 9000

INFO MainThread - [*] Conectado al servidor 10.0.0.2:9000
usuario: Escribe un msj ->:
```
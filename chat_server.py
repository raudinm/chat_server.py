#!/usr/bin/env python3
"""
Implementacion de un servidor de chat.
"""
import socket
import sys
import threading
import logging
import base64
import getopt
from getpass import getuser
from estilos import Colores as c


logging.basicConfig(
    level=logging.DEBUG,
    format=c.AMARILLO + '\n%(levelname)s' + c.ENDC +
    c.MAGENTA + ' %(threadName)s' + c.ENDC + ' -' +
    c.CYAN + ' %(message)s' + c.ENDC
)


class Servidor:
    """
    Servidor que esperara conexiones entrantes de
    varios clientes.
    """

    def __init__(self, host, port):
        logging.info('Inicializando el servidor...')
        self.clientes = []
        # crear socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.bind((host, int(port)))

        except PermissionError:
            logging.error(
                'No es posible utilizar un puerto menor al 1024'
            )
            sys.exit(1)

        except OSError:
            logging.error(
                '{} {} {}'
                .format(
                    "No es posible asignar la dirrecion ip, o el puerto",
                    "esta en uso. Asegurate de usar una ip valida",
                    " dentro de tu red y un puerto libre."
                )
            )
            sys.exit(1)

        self.sock.listen(10)
        self.sock.setblocking(False)

        conexiones = threading.Thread(
            name='Conexiones', target=self.conexiones
        )
        procesar_msj = threading.Thread(
            name='Procesar Mensajes', target=self.procesar_mensajes
        )

        conexiones.setDaemon(True)
        conexiones.start()
        procesar_msj.setDaemon(True)
        procesar_msj.start()

        logging.info("Servidor escuchando en {}:{}".format(host, port))

        while True:
            try:
                mensaje = input(
                    '{} {} {} {}\n\n'.format(
                        c.VERDE, '\n[Escribe `q` para detener el servidor]',
                        'Esperando conexiones...', c.ENDC
                    )
                )
                if mensaje == 'q':
                    self.sock.close()
                    sys.exit(0)
                else:
                    pass
            except KeyboardInterrupt:
                logging.info('El servidor se ha detenido')
                sys.exit(0)

    def mensajes(self, mensaje, cliente):
        """
        Maneja los mensajes recividos de los clientes
        y lo envia a los demas clientes conectados omitiendo
        el emisor del mensaje.
        """

        for i in self.clientes:
            try:
                if i != cliente:
                    i.send(mensaje)
                else:
                    continue
            except Exception as e:
                raise e

    def conexiones(self):
        """
        Detecta cada nuevo cliente conectado y lo agrega a la lista de
        clientes.
        """

        while True:
            try:
                cliente, addr = self.sock.accept()
                logging.info(
                    'Nuevo cliente conectado desde {}:{}'
                    .format(addr[0], addr[1])
                )
                cliente.setblocking(False)
                self.clientes.append(cliente)

            except BlockingIOError:
                pass

    def procesar_mensajes(self):
        """
        Verifica si hay algun cliente en la lista de clientes
        para recibir el mensaje y enviarlo pasandolo a l metodo
        mensajes que es el encargado de enviarlo a los clientes.
        """

        while True:
            if len(self.clientes) > 0:
                for i in self.clientes:
                    try:
                        mensaje = i.recv(4096)
                        if mensaje:
                            self.mensajes(mensaje, i)
                    except BlockingIOError:
                        pass


class Cliente:
    """Socket cliente que interactua con el servidor."""

    def __init__(self, host, port):
        # crear socket cliente
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # conectar al socket servidor
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            logging.debug("Conexion rechazada :( !!")
            sys.exit(1)

        # obtener nombre del usuario que inicio la conexion
        self.usuario = getuser()

        log = logging.getLogger(name='Inicializacion')
        log.info('[*] Conectado al servidor {}:{}'.format(host, port))

        # Mensajes recibidos
        mensajes = threading.Thread(
            name='Nuevo Mensaje', target=self.recibir_msj
        )
        mensajes.setDaemon(True)
        mensajes.start()

        while True:
            try:
                msj = input(
                    '{}{}: Escribe un msj ->: {}'
                    .format(c.VERDE, self.usuario, c.ENDC)
                )

                if msj == '':
                    pass

                elif msj != 'q':
                    encoded_msj = base64.b64encode(
                        bytes(self.usuario + ':' + msj, 'utf-8')
                    )

                    self.enviar_msj(encoded_msj)
                else:
                    self.sock.close()
                    sys.exit()

            except KeyboardInterrupt:
                logging.info('Conexion cerrada')
                self.sock.close()
                sys.exit()

    def enviar_msj(self, msj):
        """Envia los mensajes del cliente al servidor"""

        self.sock.send(msj)

    def recibir_msj(self):
        """Recibe los mensajes del servidor"""

        while True:
            try:
                msj = self.sock.recv(4096)
                if msj:
                    decoded_msj = base64.b64decode(msj)
                    log = logging.getLogger('Nuevo Mensaje')
                    cliente, mensaje = decoded_msj.decode().split(":", 1)
                    log.info('Enviado por `{}`'.format(cliente))
                    print('\nMensaje: {}'.format(mensaje))

            except ConnectionResetError:
                logging.error('El servidor se ha detenido')
                sys.exit(1)

            except Exception as e:
                raise e


def uso():
    """
    Muestra como usar el script.
    """

    print("""Chat Server

    {uso}Uso: chat_server.py -l ip -p puerto{euso}

    {}-l --listen{}            - escucha en [ip]:[port] para
                           conexiones entrantes

    {}-p --port{}              - espesifica el puerto a utilizar en el
                           servidor o cliente

    {}-c --connect{}           - conecta a un servidor como cliente
    {}-h --help{}              - muestra este menu de ayuda

    {ex}Ejemplos:
    chat_server.py -l 192.168.0.10 -p 5555 [Iniciar un servidor]
    chat_server.py -c 192.168.0.10 -p 5555 [Conectar a un servidor]{eex}
    """.format(
        c.AMARILLO, c.ENDC,
        c.AMARILLO, c.ENDC,
        c.AMARILLO, c.ENDC,
        c.AMARILLO, c.ENDC,
        uso=c.CYAN, euso=c.ENDC,
        ex=c.CYAN, eex=c.ENDC
    ))
    sys.exit(0)


def main():
    """Procesa los argumentos de la linea de comandos"""

    if not len(sys.argv[1:]):
        # mostrar menu de ayuda si no se le pasa ningun argumento al script
        uso()

    # leer las opciones de la linea de comandos
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:], "hl:p:c:", ["help", "listen=", "port=", "connect="]
        )

    except getopt.GetoptError as err:
        print(err)
        # en caso de un error siempre muestra el menu de ayuda
        uso()

    ip = None
    ip_server = None
    port = None

    for opc, arg in opts:
        if opc in ("-h", "--help"):
            uso()

        elif opc in ("-l", "--listen"):
            ip = arg

        elif opc in ("-p", "--port"):
            port = int(arg)

        elif opc in ("-c", "--connect"):
            ip_server = arg

        else:
            assert False, "Opcion desconocida."

    if ip and port:
        Servidor(ip, port)

    elif ip_server and port:
        Cliente(ip_server, port)

    else:
        # si no se recibe ningun argumento mostrar el menu de ayuda
        uso()


main()

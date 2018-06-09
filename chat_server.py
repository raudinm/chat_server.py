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
        """Inicializador del socket servidor."""

        logging.info('Inicializando el servidor...')

        self.server_addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []

        try:
            self.sock.bind((host, int(port)))
            self.sock.listen(10)

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

    def handler(self, client, addr):
        """
        Recibe los mensajes y los envia a todos los clientes
        en la lista de clientes omitiendo al emisor.
        """

        logging.info("Nuevo cliente conectado {:s}:{:d}".format(*addr))
        while True:
            msj = client.recv(1024)
            for cliente in self.clientes:
                if cliente != client:
                    cliente.send(msj)
                else:
                    continue

            if not msj:
                self.clientes.remove(client)
                logging.info(
                    "El cliente {:s}:{:d} se ha desconectado".format(*addr)
                )
                break

    def run(self):
        logging.info(
            "Servidor escuchando en {:s}:{:d} presione <Ctrl+C> para detenerlo"
            .format(*self.server_addr)
        )

        while True:
            try:
                client, addr = self.sock.accept()
                client_thread = threading.Thread(
                    target=self.handler, args=(client, addr,)
                )
                client_thread.setDaemon(True)
                client_thread.start()
                # agregar cliente a la lista de clientes
                self.clientes.append(client)

            except KeyboardInterrupt:
                log = logging.getLogger('Servidor')
                self.sock.close()
                log.info('El servidor se ha detenido')
                sys.exit(0)

            except Exception as e:
                # en caso de darse otra excepcion importante
                # que no se halla tomado en cuenta
                logging.warning("Algo anda mal: %s", e)
                input()


class Cliente:
    """Socket cliente que interactua con el servidor."""

    def __init__(self, host, port):
        """Inicializador del socket cliente"""

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
                    cliente, mensaje = decoded_msj.decode().split(":", 1)
                    logging.info('Enviado por `{}`'.format(cliente))
                    print('\nMensaje: {}'.format(mensaje))

            except ConnectionResetError:
                logging.error('El servidor se ha detenido')
                sys.exit(1)

            except Exception as e:
                logging.warning('Algo anda mal: %s', e)
                input()


def uso():
    """
    Muestra como usar el script.
    """

    print("""Chat Server

    {uso}Uso: chat_server.py -l ip -p puerto{euso}

    {}-l --listen{}            - Espesifica la direccion ip para
                           escuchar conexiones entrantes

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
        Servidor(ip, port).run()

    elif ip_server and port:
        Cliente(ip_server, port)

    else:
        # si no se recibe ningun argumento mostrar el menu de ayuda
        uso()


if __name__ == '__main__':
    main()

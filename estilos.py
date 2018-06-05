#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Modulo para dar color al texto en la consola
"""
from time import sleep


class Colores:
    """Estilos para dar color al texto."""
    # COLORES
    MAGENTA = '\033[35m'
    AZUL = '\033[34m'
    VERDE = '\033[32m'
    AMARILLO = '\033[33m'
    ROJO = '\033[31m'
    CYAN = '\033[36m'
    BLANCO = '\033[37m'
    NEGRO = '\033[30m'

    # EFECTOS O ESTILOS
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DEBIL = '\033[2m'
    CURSIVA = '\033[3m'
    SUBRAYADO = '\033[4m'
    INVERSO = '\033[5m'
    OCULTO = '\033[6m'
    TACHADO = '\033[7m'

    # FONDOS
    FONDO_BLANCO = '\033[47m'
    FONDO_CYAN = '\033[46m'
    FONDO_MAGENTA = '\033[45m'
    FONDO_AZUL = '\033[44m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_VERDE = '\033[42m'
    FONDO_ROJO = '\033[41m'
    FONDO_NEGRO = '\033[40m'

    @classmethod
    def error(cls, cadena):
        """Este metodo se invoca cuando ocurre un error
        para mostrar el texto del error en color rojo.

        Argumento:
            cadena {str} -- Texto que identifica el error.
        """
        print(
            cls.ROJO + cls.BOLD + '\n' + '[x] {}'.format(cadena) + cls.ENDC
        )
        sleep(2)

    @classmethod
    def success(cls, cadena):
        """Este metodo se invoca cuando una operacion de realiza con exito
        para mostrar el texto  en color verde.

        Argumento:
            cadena {str} -- Texto que identifica el exito de la operacion.
        """
        print(
            cls.VERDE + cls.BOLD + '\n' + '[+] {}'.format(cadena) + cls.ENDC
        )
        sleep(2)

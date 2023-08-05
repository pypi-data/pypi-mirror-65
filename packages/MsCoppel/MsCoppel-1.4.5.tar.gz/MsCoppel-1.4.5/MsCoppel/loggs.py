import sys
import os
from .loggsWrapper import LoggerWrapper


def Loggs(name, logsAll=True):
    """
        Metodo para generar un elemento de logger
        @params name Nombre del modulo/libreria
    """

    # Validar si proviene de un ambiente productivo.
    if not os.environ.get('LOGS_FLUENT', None) is None:
        return LoggerWrapper(name)
    else:
        import coloredlogs
        import logging

        logger = logging.getLogger(name)

        # solo cuando se indique se mostraran todos los logs
        if logsAll:
            coloredlogs.install()
        else:
            coloredlogs.install(logger=logger)
        return logger

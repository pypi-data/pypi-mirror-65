# -*- coding: utf-8 -*-
"""
Module de pilotage d'un microcontrôleur (PyBoard, ESP32, Micro:bit, ...) fonctionnant sous micropython à partir d'un ordinateur sous Python 3.

@author: David Thérincourt
"""

from .pyboard import Pyboard

def execFichier(nomFichier, portSerie, debit = 115200):
    """
    Fonction qui exécute un programme MicroPython à partir d'un ordinateur sur un microcontrôleur (avec le firmware MicroPython) par le port série en mode REPL RAW.

    Paramètres :
        nomFichier (str) : nom du fichier MicroPython à exécuté.
        portSerie (str) : nom du port série sur lequel se trouve le microcontrôleur (ex. COM6)

    Paramètre optionnel :
        debit (int) :  débit de transfert des données sur le port série (115200 bauds par défaut)

    Retourne (str) :
        Chaîne de caractères contenant le sortie standart du mode REPL (utile pour réccupérer des données avec la fonction print() de MicroPython)
    """
    pyb = Pyboard(portSerie, debit)
    pyb.enter_raw_repl()
    repl_txt = pyb.execfile(nomFichier)
    pyb.close()
    return repl_txt.decode()

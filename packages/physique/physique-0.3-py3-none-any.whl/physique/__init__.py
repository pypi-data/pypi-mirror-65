# -*- coding: utf-8 -*-
"""
librairie Python 3 pour les sciences physiques au lycée.

Modules disponibles de la librairie (package)) physique :
- modelisation :
    Modélisation de courbes (linéaire, affine, parabolique, exponentielle, ...)
    Exemple :
    >>> from physique.modelisation import ajustement_parabolique
- csv :
    Importation et exportation de données au format CSV pour Avimeca3, ...
    Exemple :
    >>> from physique.csv import importAvimeca3
- micropython
    Exécution d'un programme MicroPython sur un microcontrôleur (Micro:bit, Pyboard, ESP32, ...) à partir d'un ordinateur par le port série (mode REPL RAW)
    Exemple :
    >>> from physique.micropython import execFichier

@author: David Thérincourt - 2020
"""

import physique.modelisation
import physique.csv
import physique.micropython

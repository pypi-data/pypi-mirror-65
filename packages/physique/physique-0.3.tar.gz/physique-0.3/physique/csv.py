# -*- coding: utf-8 -*-
"""
Module d'importation et d'exportation de tableaux de données au format CSV.
Logiciels pris en compte : Latis, Regressi, RegAvi, AviMeca3

@author: David Thérincourt
"""

import numpy as np
from io import StringIO

def normaliseFichier(fichier, encodage = 'utf-8') :
    """
    Normalise les séparateurs décimaux dans un fichier CSV en remplaçant les virgules par des points.
    """
    f = open(fichier,'r', encoding = encodage)
    data = f.read()
    f.close()
    return StringIO(data.replace(",","."))

def importAvimeca3(fichier, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3

    Paramètre :
        fichier (str) : nom du fichier CSV

    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)

    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normaliseFichier(fichier, encodage = 'cp1252') # iso-8859-1 ou CP1252
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 3, comments = '#')

def importRegavi(fichier, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel RegAvi

    Paramètre :
        fichier (str) : nom du fichier CSV

    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)

    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normaliseFichier(fichier, encodage = 'ascii')
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 2, comments = '#')

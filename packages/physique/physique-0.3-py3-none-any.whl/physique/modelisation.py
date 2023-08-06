# -*- coding: utf-8 -*-
"""
Module de modélisation de courbes pour les sciences physiques
@author: David Thérincourt
"""

import numpy as np
from scipy.stats import linregress
from scipy.optimize import curve_fit

#--------------------------
# Fonctions mathématiques
#--------------------------

def lineaire(x, a) :
    """
    Fonction lineaire du type y = a*x

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    a (float) :

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return a*x

def parabole(x, a, b, c) :
    """
    Fonction parabolique du type y = a*x**2 + b*x + c

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    a (float) :
    b (float) :
    c (float) :

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return a*x**2+b*x+c

def exp1(x, A, tau, x0=0):
    """
    Fonction exponenetielle croissante du type y = A*(1-exp(-(x-x0)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*(1-np.exp(-(x-x0)/tau))

def exp2(x, A, tau, x0=0):
    """
    Fonction exponenetielle décroissante du type y = A*exp(-(x-x0)/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*np.exp(-(x-x0)/tau)

#---------------------------------------------
# Modélisations
#---------------------------------------------

def ajustement_affine(x, y):
    """
    Modélisation d'une fonction affine de la forme y = a*x + b

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne un tuple (a, b) :
    a (float) : coefficient directeur.
    b (float) : ordonnée à l'origine.
    """
    a, b, _, _, _ = linregress(x,y)
    return a, b


def ajustement_lineaire(x, y, a_p0=1) :
    """
    Modélisation d'une fonction parabolique du type y = a*x

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne :
    a (float)
    """
    (a), pcov = curve_fit(lineaire,x,y, p0=[a_p0])
    return a



def ajustement_parabolique(x, y) :
    """
    Modélisation d'une fonction parabolique du type y = a*x**2 + b*x + c

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne :
    [a, b, c] (tableau) : coefficients
    """
    return np.polyfit(x, y, 2)


def ajustement_exp1(x, y, A_p0=1, tau_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    du type y = A*(1-exp(-x/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    """
    (A,tau), pcov = curve_fit(exp1,x,y, p0=[A_p0, tau_p0])
    return A, tau

def ajustement_exp1_x0(x, y, A_p0=1, tau_p0=1, x0_p0=0) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    décalée suivant l'abscisse du type y = A*(1-exp(-(x-xo)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.
    x0_p0 (0 par défaut) : valeur du retard aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.
    """
    (A,tau,x0), pcov = curve_fit(exp1,x,y, p0=[A_p0, tau_p0, x0_p0])
    return A, tau, x0



def ajustement_exp2(x, y, A_p0=1, tau_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante du type y = A*(1-exp(x-/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.
    """
    (A,tau), pcov = curve_fit(exp2, x, y, p0=[A_p0, tau_p0])
    return A, tau

def ajustement_exp2_x0(x, y, A_p0=1, tau_p0=1, x0_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante du type y = A*(1-exp(x-/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.
    """
    (A,tau, x0), pcov = curve_fit(exp2, x, y, p0=[A_p0, tau_p0, x0_p0])
    return A, tau, x0

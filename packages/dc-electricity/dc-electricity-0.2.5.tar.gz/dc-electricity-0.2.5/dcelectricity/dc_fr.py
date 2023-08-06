# -*- coding: utf8 -*-
# python 3
# (C) Fabrice Sincère

"""Ce module à but pédagogique permet de manipuler les lois de l'Electricité \
dans un circuit électrique linéaire en régime continu.

Python 3

Site web : http://fsincere.free.fr/isn/python/cours_python_dc.php

Exemple d'utilisation :

Schéma électrique
-----------------

          V1
       <------
    --->--R1-------------
 ^     I1         |      |
 |            I2  v      v  I3   ^
 |                |      |       |
E|                R2     R3      | V2
 |                |      |       |
 |                |      |
    ---------------------

Données :
E = 12 V ; R1 = 1 kΩ ; R2 = 2.7 kΩ ; R3 = 1.8 kΩ

Calcul des courants, des tensions et bilan de puissances :

    from dcelectricity import dc_fr as dc
    loi = dc.Loi()

    # définitions
    E = dc.Tension(12)
    E.Info("Propriétés de E :")

    R1 = dc.Resistance(1, 'k')
    R1.Info("Propriétés de R1 :")

    R2 = dc.Resistance(2.7, 'k')
    R2.Info("Propriétés de R2 :")

    R3 = dc.Resistance(1.8, 'k')
    R3.Info("Propriétés de R3 :")

    # résistance équivalente
    Req = loi.Rserie(R1, loi.Rparallele(R2, R3))
    Req.Info("Propriétés de Req :")

    # loi d'Ohm
    I1 = loi.Ohm(v=E, r=Req)
    I1.Info("Propriétés de I1 :")

    # loi d'Ohm
    V1 = loi.Ohm(i=I1, r=R1)
    V1.Info("Propriétés de V1 :")

    # loi des branches
    V2 = loi.Branche("+-", E, V1)
    V2.Info("Propriétés de V2 :")

    # loi d'Ohm
    I2 = loi.Ohm(r=R2, v=V2)
    I2.Info("Propriétés de I2 :")

    # loi des nœuds
    I3 = loi.Noeud("+-", I1, I2)
    I3.Info("Propriétés de I3 :")

    # autre méthode pour trouver V2
    # formule du diviseur de tension
    V2bis = loi.DiviseurTension(vtotal=E, r=loi.Rparallele(R2, R3), r2=R1)
    V2bis.Info("Propriétés de V2bis :")

    # autre méthode pour trouver I2
    # formule du diviseur de courant
    I2bis = loi.DiviseurCourant(itotal=I1, r=R2, r2=R3)
    I2bis.Info("Propriétés de I2bis :")

    # encore une autre méthode pour trouver V2
    # Théorème de Millman
    masse = dc.Tension(0)
    V2ter = loi.Millman(v_r=[(E, R1), (masse, R2), (masse, R3)])
    V2ter.Info("Propriétés de V2ter :")

    # bilan de puissances
    puissanceE = loi.Puissance(v=E, i=I1)
    puissanceE.Info("Générateur E :")

    P1 = loi.Joule(r=R1, i=I1)
    P1.Info("Résistance R1 :")
    P2 = loi.Joule(r=R2, i=I2)
    P2.Info("Résistance R2 :")
    P3 = loi.Joule(r=R3, i=I3)
    P3.Info("Résistance R3 :")
    (P1+P2+P3).Info("Puissance totale consommée par les résistances :")

Résultat :

    Propriétés de E :
    Tension : 12.000000 V
    Propriétés de R1 :
    Résistance : 1000 Ω (1.000000 kΩ)
    Propriétés de R2 :
    Résistance : 2700 Ω (2.700000 kΩ)
    Propriétés de R3 :
    Résistance : 1800 Ω (1.800000 kΩ)
    Propriétés de Req :
    Résistance : 2080 Ω (2.080000 kΩ)
    Propriétés de I1 :
    Intensité du courant : 0.00576923 A (5.769231 mA)
    Propriétés de V1 :
    Tension : 5.769231 V
    Propriétés de V2 :
    Tension : 6.230769 V
    Propriétés de I2 :
    Intensité du courant : 0.00230769 A (2.307692 mA)
    Propriétés de I3 :
    Intensité du courant : 0.00346154 A (3.461538 mA)
    Propriétés de V2bis :
    Tension : 6.230769 V
    Propriétés de I2bis :
    Intensité du courant : 0.00230769 A (2.307692 mA)
    Propriétés de V2ter :
    Tension : 6.230769 V
    Générateur E :
    Puissance : 0.0692308 W (69.230769 mW)
    Résistance R1 :
    Puissance : 0.033284 W (33.284024 mW)
    Résistance R2 :
    Puissance : 0.0143787 W (14.378698 mW)
    Résistance R3 :
    Puissance : 0.021568 W (21.568047 mW)
    Puissance totale consommée par les résistances :
    Puissance : 0.0692308 W (69.230769 mW)
"""

import sys
import math

__version__ = (0, 2, 5)
__author__ = "Fabrice Sincère <fabrice.sincere@ac-grenoble.fr>"

if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    exit(1)


def PrefixeGrandeur(mantisse, prefixe=''):
    """mantisse -> type float
prefixe  -> type str

retourne la valeur décimale correspondante (type float)

Le symbole du préfixe doit être une des valeurs :
'p' pico, 'n', 'u' ou 'µ' micro, 'm', 'k', 'M' méga, 'G', 'T', \'' par défaut

Exemple :
    from dcelectricity import dc_fr as dc
    dc.PrefixeGrandeur(20, 'm')  # retourne 0.02
    dc.PrefixeGrandeur(50, 'k')  # retourne 50000
    dc.PrefixeGrandeur(-10000)   # retourne -10000
"""
    prefixes = {'': 1, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'µ': 1e-6,
                'm': 1e-3, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}

    return mantisse * prefixes[prefixe]


def NotationIngenieur(valeur):
    """valeur -> type float

Retourne un tuple (mantisse, symbole du préfixe)
avec mantisse comprise entre 1 et 1000

mantisse -> type float
prefixe  -> type str

Le symbole du préfixe est une des valeurs :
'p' pico, 'n', 'µ' micro, 'm', 'k', 'M' méga, 'G', 'T', \'' par défaut

Exemple :
    from dcelectricity import dc_fr as dc
    dc.NotationIngenieur(999)    # retourne (999, '')
    dc.NotationIngenieur(1000)   # retourne (1.0, 'k')
    dc.NotationIngenieur(-1e-6)  # retourne (-1.0, 'µ')
    dc.NotationIngenieur(0)      # retourne (0, '')

    mantisse, prefixe = dc.NotationIngenieur(1200000)
    print("Résistance : {} {}Ω".format(mantisse, prefixe))

donne :
    Résistance : 1.2 MΩ
"""
    if valeur == 0.0:
        return (0, '')

    nbdecimal = math.log10(abs(valeur))

    if -15.0 <= nbdecimal < -9.0:
        return (valeur*1e12, 'p')
    elif -9.0 <= nbdecimal < -6.0:
        return (valeur*1e9, 'n')
    elif -6.0 <= nbdecimal < -3.0:
        return (valeur*1e6, 'µ')
    elif -3.0 <= nbdecimal < 0.0:
        return (valeur*1e3, 'm')
    elif 0.0 <= nbdecimal < 3.0:
        return (valeur, '')
    elif 3.0 <= nbdecimal < 6.0:
        return (valeur*1e-3, 'k')
    elif 6.0 <= nbdecimal < 9.0:
        return (valeur*1e-6, 'M')
    elif 9.0 <= nbdecimal < 12.0:
        return (valeur*1e-9, 'G')
    elif 12.0 <= nbdecimal < 15.0:
        return (valeur*1e-12, 'T')
    else:
        return (valeur, '')  # notation scientifique


class Composant:
    """Classe relative aux dipôles passifs linéaires en régime continu : \
les résistances
Cette classe ne s'utilise pas directement.
"""
    def __init__(self):
        pass


class Resistance(Composant):
    """ Classe relative aux résistances."""

    def __init__(self, mantisse, prefixe=''):
        """Instanciation d'un objet Resistance

mantisse -> type float
prefixe  -> type str (parmi : 'p','n','u' ou 'µ','m','k','M','G','T',/
'' par défaut)

Exemple :
    from dcelectricity import dc_fr as dc
    r1 = dc.Resistance(22000)
    r2 = dc.Resistance(4.7, 'k')
"""
        Composant.__init__(self)
        self.__unite = "Ω"    # ohm
        try:
            valeur = PrefixeGrandeur(mantisse, prefixe)
            self.__valeur = float(valeur)
        except:
            raise TypeError("Le paramètre valeur doit être de type float")

        if self.__valeur < 0.0:
            raise ValueError("La résistance doit être positive")

    def Valeur(self):
        """ Retourne la résistance en ohm (type float) """
        return self.__valeur

    def __call__(self):
        """ L’objet est appelé comme une fonction \
et la méthode retourne la résistance en ohm (type float)

    r1 = dc.Resistance(22000)
    print(r1())

affiche :
    22000.0
"""
        return self.__valeur

    def Info(self, message=''):
        """Affiche les propriétés de la résistance

Exemple :

    R1 = dc.Resistance(1,'k')
    R1.Info("Propriétés de R1 :")

affiche :
    Propriétés de R1 :
    Résistance : 1000 Ω (1.000000 kΩ)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Retourne la représentation de l'objet (utilisé par la fonction print)

Exemple :
    R1 = dc.Resistance(1,'k')
    print(R1)

affiche :
    Résistance : 1000 Ω (1.000000 kΩ)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        mantisse, prefixe = NotationIngenieur(self.__valeur)
        if prefixe == '':
            affichage = "Résistance : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Résistance : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, mantisse, prefixe,
                       self.__unite)
        return affichage

    def __add__(self, resistance):
        """self.__add__(resistance) <=> self + resistance
Résistances en série
Retourne un objet Resistance

    r1 = dc.Resistance(22000)
    r2 = dc.Resistance(4.7, 'k')
    r3 = r1+r2  # Résistance : 26700 Ω (26.700000 kΩ)
"""
        return Loi().Rserie(self, resistance)

    def __sub__(self, resistance):
        """self.__sub__(resistance) <=> self - resistance
Retourne un objet Resistance"""

        if isinstance(resistance, Resistance) is False:
                raise TypeError("résistance attendue")
        return Resistance(self.__valeur-resistance.Valeur())

    def __pos__(self):
        """self.__pos__() <=> +self
Retourne un objet Resistance"""
        return Resistance(self.__valeur)  # objet différent

    def __floordiv__(self, resistance):
        """self.__floordiv__(resistance) <=> self // resistance
Résistances en parallèle
Retourne un objet Resistance

    r1 = dc.Resistance(22000)
    r2 = dc.Resistance(4.7, 'k')
    r3 = r1//r2  # Résistance : 3872.66 Ω (3.872659 kΩ)
"""
        return Loi().Rparallele(self, resistance)

    def __mul__(self, parametre):
        """self.__mul__(parametre) <=> self * parametre
Si parametre est un objet Courant :
Loi d'Ohm
Retourne un objet Tension

    r1 = dc.Resistance(22000)
    i1 = dc.Courant(10, 'u')
    v1 = r1*i1  # Tension : 0.22 V (220.000000 mV)

Si parametre est un float (positif) :
Multiplication
Retourne un objet Resistance

    r2 = r1*10  # Résistance : 220000 Ω (220.000000 kΩ)
    r3 = r2*(r1/(r1+r2))  # Résistance : 20000 Ω (20.000000 kΩ)
"""
        if isinstance(parametre, Courant) is True:
            return Loi().Ohm(r=self, i=parametre)
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Resistance(self.__valeur*parametre)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val est un float (positif)
Retourne un objet Resistance

    r1 = dc.Resistance(22000)
    r2 = 10*r1  # Résistance : 220000 Ω (220.000000 kΩ)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Resistance(self.__valeur*val)

    def __rtruediv__(self, val):
        """self.__rmul__(val) <=> val / self
val est un float (positif)
Retourne un objet Conductance

    r1 = dc.Resistance(22000)
    g1 = 1/r1  # Conductance : 4.54545e-05 S (45.454545 µS)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Conductance(val/self.__valeur)

    def __truediv__(self, parametre):
        """self.__truediv__(parametre) <=> self / parametre

Si parametre est un objet Resistance :
Retourne un float

    r1 = dc.Resistance(22000)
    r2 = dc.Resistance(10000)
    x = r1/r2  # 2.2

Si parametre est un float :
Retourne un objet Resistance

    r3 = r1/10  # Résistance : 2200 Ω (2.200000 kΩ)
"""
        if isinstance(parametre, Resistance) is True:
            return self.__valeur/parametre.Valeur()

        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")

        return Resistance(self.__valeur/parametre)


class Conductance(Composant):
    """ Classe relative aux conductances (inverse de la résistance)
Exemple :
    from dcelectricity import dc_fr as dc
    G1 = dc.Conductance(0.1)
    G2 = dc.Conductance(10, 'm')
    V3 = dc.Tension(3)
    G3 = G1+G2  # Conductance : 0.11 S (110.000000 mS)
    R3 = 1/G3   # Résistance : 9.090909 Ω
    # Loi d'Ohm
    I3 = G3*V3  # Intensité du courant : 0.33 A (330.000000 mA)
"""

    def __init__(self, mantisse, prefixe=''):
        """ Instanciation d'un objet Conductance

mantisse (significand) -> type float
prefixe (prefix) -> type str (parmi : 'p','n','u' ou 'µ','m','k', 'M','G','T', \
'' par défaut)

Exemple :

    G1 = dc.Conductance(0.1)
    G2 = dc.Conductance(4.7, 'm')
"""
        Composant.__init__(self)
        self.__unite = "S"    # siemens
        try:
            valeur = PrefixeGrandeur(mantisse, prefixe)
            self.__valeur = float(valeur)
        except:
            raise TypeError("Le paramètre valeur doit être de type float")

        if self.__valeur < 0.0:
            raise ValueError("La conductance doit être positive")

    def Valeur(self):
        """ Retourne la conductance en siemens (type float) """
        return self.__valeur

    def __call__(self):
        """ L’objet est appelé comme une fonction et la méthode retourne \
la conductance en siemens (type float)


    G2 = dc.Conductance(4.7, 'm')
    print(G2())

affiche :
    0.0047
"""
        return self.__valeur

    def Info(self, message=''):
        """ Affiche les propriétés de la conductance

Exemple :

    G1 = dc.Conductance(0.1)
    G1.Info("Propriétés de G1 :")

affiche :
    Propriétés de G1 :
    Conductance : 0.1 S (100.000000 mS)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """ Retourne la représentation de l'objet (utilisé par la fonction print)

Exemple :

    G1 = dc.Conductance(0.1)
    print(G1)

affiche :
    Conductance : 0.1 S (100.000000 mS)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        mantisse, prefixe = NotationIngenieur(self.__valeur)
        if prefixe == '':
            affichage = "Conductance : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Conductance : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, mantisse, prefixe,
                       self.__unite)
        return affichage

    def __add__(self, conductance):
        """self.__add__(conductance) <=> self + conductance
Retourne un objet Conductance"""

        if isinstance(conductance, Conductance) is False:
                raise TypeError("conductance attendue")
        return Conductance(self.__valeur + conductance.__valeur)

    def __sub__(self, conductance):
        """self.__sub__(conductance) <=> self - conductance
Retourne un objet Conductance"""

        if isinstance(conductance, Conductance) is False:
                raise TypeError("conductance attendue")
        return Conductance(self.__valeur - conductance.__valeur)

    def __pos__(self):
        """self.__pos__() <=> +self
Retourne un objet Conductance"""
        return Conductance(self.__valeur)  # objet différent

    def __mul__(self, parametre):
        """self.__mul__(parametre) <=> self * parametre
Si parametre est un objet Tension :
Loi d'Ohm
Retourne un objet Courant

    g1 = dc.Conductance(0.01)
    v1 = dc.Tension(10)
    i1 = g1*v1  # Intensité du courant : 0.1 A (100.000000 mA)

Si parametre est un float (positif) :
Multiplication
Retourne un objet Conductance

    g2 = g1*10  # Conductance : 0.1 S (100.000000 mS)
"""
        if isinstance(parametre, Tension) is True:
            return Courant(self.__valeur*parametre.Valeur())
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Conductance(self.__valeur*parametre)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val est un float (positif)
Retourne un objet Conductance

    g1 = dc.Conductance(0.01)
    g2 = 10*g1  # Conductance : 0.1 S (100.000000 mS)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Conductance(self.__valeur*val)

    def __rtruediv__(self, val):
        """self.__rtruediv__(val) <=> val / self
val est un float (positif)
Retourne un objet Resistance

    g1 = dc.Conductance(0.001)
    r1 = 1/g1  # Résistance : 1000 Ω (1.000000 kΩ)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Resistance(val/self.__valeur)

    def __truediv__(self, parametre):
        """self.__truediv__(parametre) <=> self / parametre

Si parametre est un objet Conductance :
Retourne un float

    g1 = dc.Conductance(0.01)
    g2 = dc.Conductance(0.2)
    x = g1/g2  # 0.05

Si parametre est un float :
Retourne un objet Conductance

    g3 = g1/10  # Conductance : 0.001 S (1.000000 mS)
"""
        if isinstance(parametre, Conductance) is True:
            return self.__valeur/parametre.Valeur()

        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")

        return Conductance(self.__valeur/parametre)

    def __floordiv__(self, conductance):
        """self.__floordiv__(conductance) <=> self // conductance
conductances en parallèle
Retourne un objet Conductance

    g1 = dc.Conductance(0.0002)
    g2 = dc.Conductance(0.0008)
    g3 = g1//g2  # Conductance : 0.001 S (1.000000 mS)
"""
        return self.__add__(conductance)


class Loi:

    """
Classe relative aux lois électriques dans un circuit linéaire \
en régime continu :
- loi des branches
- loi des nœuds
- loi d'Ohm
- association de résistances, en série, en parallèle
- diviseur de tension, de courant
- théorème de Millman
- loi de Joule (P=RI²)
- puissance (P=V*I)

Utilisation :

    from dcelectricity import dc_fr as dc
    loi = dc.Loi()

    v1 = dc.Tension(5)
    i1 = dc.Courant(20, 'µ')
    r1 = loi.Ohm(v=v1, i=i1)
"""

    def Branche(self, signes, *tensions):
        """
Loi des branches dans un circuit électrique en régime continu

signes -> type str
*tensions -> instances de la classe Tension

retourne une instance de la classe Tension

Exemple :

On veut : v4 = v1 + v2 - v3

v1, v2, v3 sont des instances de la classe Tension :


    v1 = dc.Tension(5)
    v2 = dc.Tension(-8)
    v3 = dc.Tension(2.5)

    loi = dc.Loi()
    v4 = loi.Branche('++-', v1, v2, v3)
    v4.Info("Propriétés de v4 :")

affiche :
    Propriétés de v4 :
    Tension : -5.500000 V
"""

        if len(tensions) == 0:
            raise ValueError("il faut au moins un objet Tension")

        for tension in tensions:
            if isinstance(tension, Tension) is False:
                raise TypeError("Il faut des objets Tension")

        if not isinstance(signes, str):
            raise TypeError("Le paramètre 'signes' doit être un string avec \
                un format '++-+'")

        if len(tensions) != len(signes):
            raise ValueError("La taille de 'signes' est incorrecte")
        else:
            for signe in signes:
                if signe not in "+-":
                    raise ValueError("'signes' ne doit contenir que les \
                        caractères '+' ou '-'")

        valeur = 0.0
        for index, tension in enumerate(tensions):
            if signes[index] == "+":
                valeur += tension.Valeur()
            elif signes[index] == "-":
                valeur -= tension.Valeur()
        return Tension(valeur)

    def Noeud(self, signes, *courants):
        """
Loi des nœuds dans un circuit électrique en régime continu

signes -> type str
*courants -> instances de la classe Courant

retourne une instance de la classe Courant

Exemple :

On veut : i4 = -i1 + i2 - i3

i1, i2, i3 sont des instances de la classe Courant


    i1 = dc.Courant(5, 'm')
    i2 = dc.Courant(8, 'm')
    i3 = dc.Courant(2.5, 'm')

    loi = dc.Loi()
    i4 = loi.Noeud('-+-', i1, i2, i3)
    i4.Info("Propriétés de i4 :")

affiche :
    Propriétés de i4 :
    Intensité du courant : 0.0005 A (500.000000 µA)
"""

        if len(courants) == 0:
            raise ValueError("il faut au moins un objet Courant")

        for courant in courants:
            if isinstance(courant, Courant) is False:
                raise TypeError("Il faut des objets Courant")

        if not isinstance(signes, str):
            raise TypeError("Le paramètre 'signes' doit être un string avec un \
                format '++-+'")

        if len(courants) != len(signes):
            raise ValueError("La taille de 'signes' est incorrecte")
        else:
            for signe in signes:
                if signe not in "+-":
                    raise ValueError("'signes' ne doit contenir que les \
                        caractères '+' ou '-'")

        valeur = 0.0
        for index, courant in enumerate(courants):
            if signes[index] == "+":
                valeur += courant.Valeur()
            elif signes[index] == "-":
                valeur -= courant.Valeur()
        return Courant(valeur)

    def Ohm(self, **grandeurs):
        """
Loi d'Ohm dans un circuit électrique en régime continu

Suivant le cas : v = r*i ou i = v/r ou r = v/i

**grandeurs -> 2 paramètres parmi les 3 (v, r et i)
v -> instance de la classe Tension
i -> instance de la classe Courant
r -> instance de la classe Resistance

retourne une instance de la 3ème grandeur

Exemple 1:


    v1 = dc.Tension(5)
    i1 = dc.Courant(20, 'µ')

    loi = dc.Loi()
    r1 = loi.Ohm(v=v1, i=i1)
    r1.Info("Propriétés de r1 :")

affiche :
    Propriétés de r1 :
    Résistance : 250000 Ω (250.000000 kΩ)

Exemple 2:


    v2 = dc.Tension(2)
    r2 = dc.Resistance(100, 'k')

    loi = dc.Loi()
    i2 = loi.Ohm(v=v2, r=r2)
    i2.Info("Propriétés de i2 :")

affiche :
    Propriétés de i2 :
    Intensité du courant : 2e-05 A (20.000000 µA)
"""

        grandeurs_attendus = ['v', 'r', 'i']

        if len(grandeurs) != 2:
            raise TypeError("Il faut 2 paramètres")

        else:
            # liste des paramètres
            cles = list(grandeurs)
            if (cles[0] not in grandeurs_attendus or
                    cles[1] not in grandeurs_attendus):
                raise TypeError("les paramètres attendus sont r, v ou i")

        # v = r*i
        if 'v' not in cles:
            if isinstance(grandeurs['i'], Courant) is False:
                raise TypeError("courant attendu")

            courant = grandeurs['i'].Valeur()

            if isinstance(grandeurs['r'], Resistance) is False:
                raise TypeError("résistance attendue")

            resistance = grandeurs['r'].Valeur()
            tension = resistance * courant
            return Tension(tension)

        # i = v/r
        if 'i' not in cles:
            if isinstance(grandeurs['v'], Tension) is False:
                raise TypeError("tension attendue")

            tension = grandeurs['v'].Valeur()

            if isinstance(grandeurs['r'], Resistance) is False:
                raise TypeError("résistance attendue")

            resistance = grandeurs['r'].Valeur()
            courant = tension / resistance
            return Courant(courant)

        # r =v/i
        if 'r' not in cles:
            if isinstance(grandeurs['v'], Tension) is False:
                raise TypeError("tension attendue")

            tension = grandeurs['v'].Valeur()

            if isinstance(grandeurs['i'], Courant) is False:
                raise TypeError("courant attendu")

            courant = grandeurs['i'].Valeur()
            resistance = tension / courant
            return Resistance(resistance)

    def Rserie(self, *resistances):
        """
Résistance équivalente d'une association de résistances en série

*resistances -> instances de la classe Resistance

retourne une instance de la classe Resistance

Exemple :


    r1 = dc.Resistance(100,'k')
    r2 = dc.Resistance(47,'k')
    r3 = dc.Resistance(22,'k')

    loi = dc.Loi()
    Req = loi.Rserie(r1, r2, r3)
    Req.Info("Propriétés de Req :")

affiche :
    Propriétés de Req :
    Résistance : 169000 Ω (169.000000 kΩ)
"""

        if len(resistances) == 0:
            raise TypeError("Il faut au moins un paramètre")

        Req = 0.0
        for r in resistances:
            if isinstance(r, Resistance) is False:
                raise TypeError("résistance attendue")
            Req += r.Valeur()

        return Resistance(Req)

    def Rparallele(self, *resistances):
        """
Résistance équivalente d'une association de résistances en parallèle

*resistances -> instances de la classe Resistance

retourne une instance de la classe Resistance

Exemple :


    r1 = dc.Resistance(1500)
    r2 = dc.Resistance(1000)

    loi = dc.Loi()
    Req = loi.Rparallele(r1, r2)
    Req.Info("Propriétés de Req :")

affiche :
    Propriétés de Req :
    Résistance : 600.000000 Ω
"""

        if len(resistances) == 0:
            raise TypeError("Il faut au moins un paramètre")

        Geq = 0.0  # conductance
        for r in resistances:
            if isinstance(r, Resistance) is False:
                raise TypeError("résistance attendue")

            if r.Valeur() == 0.0:
                return Resistance(0.0)
            Geq += 1.0/r.Valeur()

        return Resistance(1/Geq)

    def DiviseurTension(self, vtotal, r, r2):
        """ Formule du diviseur de tension

        vtotal
--------------------->

----[r]-----[r2]-----

   ----->
     v

r et r2 sont deux résistances parcourues par le même courant

vtotal   -> instance de la classe Tension
r et r2  -> instances de la classe Resistance

La méthode retourne la valeur de la tension u aux bornes
de r (instance de la classe Tension)

Exemple :


    r1 = dc.Resistance(1, 'k')
    r2 = dc.Resistance(9, 'k')
    v = dc.Tension(5)

    loi = dc.Loi()
    v1 = loi.DiviseurTension(vtotal=v, r=r1, r2=r2)

    v1.Info("Propriétés de v1 :")

affiche :

    Propriétés de v1 :
    Tension : 0.5 V (500.000000 mV)
"""

        if isinstance(r, Resistance) is False:
                raise TypeError("résistance attendue")

        R = r.Valeur()
        if isinstance(r2, Resistance) is False:
                raise TypeError("résistance attendue")

        R2 = r2.Valeur()
        if isinstance(vtotal, Tension) is False:
                raise TypeError("tension attendue")

        V = vtotal.Valeur()
        return Tension(V*R/(R+R2))

    def DiviseurCourant(self, itotal, r, r2):
        """ Formule du diviseur de courant

                i
    ----[r]----<--     itotal
---|              |---<----
    ----[r2]---<--

r et r2 sont deux résistances en parallèle, consommant un courant total itotal

itotal   -> instance de la classe Courant
r et r2  -> instances de la classe Resistance

La méthode retourne la valeur du courant i dans la résistance r \
(instance de la classe Courant)

Exemple :


    r1 = dc.Resistance(100)
    r2 = dc.Resistance(900)
    i = dc.Courant(100, 'm')

    loi = dc.Loi()
    i1 = loi.DiviseurCourant(itotal=i, r=r1, r2=r2)
    i1.Info("Propriétés de i1 :")

affiche :
    Propriétés de i1 :
    Intensité du courant : 0.09 A (90.000000 mA)
"""

        if isinstance(r, Resistance) is False:
            raise TypeError("résistance attendue")

        R = r.Valeur()
        if isinstance(r2, Resistance) is False:
            raise TypeError("résistance attendue")

        R2 = r2.Valeur()
        if isinstance(itotal, Courant) is False:
            raise TypeError("courant attendu")

        I = itotal.Valeur()
        return Courant(I*R2/(R+R2))

    def Millman(self, v_r, i=[]):
        """ Théorème de Millman

Biblio : http://fabrice.sincere.pagesperso-orange.fr/electricite.htm

Millman(self, v_r=[(v1, r1), (v2, r2) ...], i=[i1, i2...])

v_r -> liste de tuples
Le tuple contient deux éléments :
(instance de classe Tension, instance de classe Resistance)

i -> liste d'instances de classe Courant

La méthode retourne une instance de la classe Tension

Exemple :


    masse = dc.Tension(0)
    E = dc.Tension(10)
    R1 = dc.Resistance(1000)
    R2 = dc.Resistance(10000)
    R3 = dc.Resistance(2200)

    loi = dc.Loi()
    v2 = loi.Millman(v_r = [(E, R1), (masse, R2), (masse, R3)])

    v2.Info("Propriétés de v2 :")

affiche :
    Propriétés de v2 :
    Tension : 6.432749 V
"""
        if isinstance(v_r, list) is False:
                raise TypeError("un type list est attendu pour v_r")

        if len(v_r) == 0:
            raise TypeError("v_r doit contenir au moins un élément")

        somme_v_sur_R = 0.0
        somme_1_sur_R = 0.0

        for elt in v_r:
            if isinstance(elt, tuple) is False:
                raise TypeError("un type tuple est attendu")
            if len(elt) != 2:
                raise TypeError("le tuple doit contenir deux éléments")
            if isinstance(elt[0], Tension) is False:
                raise TypeError("un objet Tension est attendu")
            if isinstance(elt[1], Resistance) is False:
                raise TypeError("un objet Resistance est attendu")
            somme_v_sur_R += elt[0].Valeur()/elt[1].Valeur()
            somme_1_sur_R += 1/elt[1].Valeur()

        if isinstance(i, list) is False:
            raise TypeError("un type list est attendu pour i")

        itotal = 0.0
        for courant in i:
            if isinstance(courant, Courant) is False:
                raise TypeError("un objet Courant est attendu")
            itotal += courant.Valeur()

        tension = (somme_v_sur_R + itotal)/somme_1_sur_R
        return Tension(tension)

    def Puissance(self, v, i):
        """
Calcul la puissance électrique (en watts) mise en jeu \
dans un dipôle quelconque

v est un objet Tension
i est un objet Courant

La méthode retourne un objet de la classe Puissance

Remarque : ne pas confondre Loi.Puissance() et Puissance()

Exemple d'utilisation :


    loi = dc.Loi()
    v1 = dc.Tension(5)
    i1 = dc.Courant(100, 'm')
    p1 = loi.Puissance(v=v1, i=i1)
    p1.Info("Propriétés de p1 :")

affiche :
    Propriétés de p1 :
    Puissance : 0.5 W (500.000000 mW)
"""
        if isinstance(v, Tension) is False:
                    raise TypeError("Il faut un objet Tension")

        if isinstance(i, Courant) is False:
                    raise TypeError("Il faut un objet Courant")

        return Puissance(v.Valeur()*i.Valeur())

    def Joule(self, r, **grandeur):
        """
Calcul la puissance électrique (en watts) consommée par une résistance

Suivant le cas : p = r*i² ou p = v²/r (loi de Joule)

**grandeur -> v ou i

v -> instance de la classe Tension
i -> instance de la classe Courant
r -> instance de la classe Resistance

La méthode retourne un objet de la classe Puissance

Exemple d'utilisation :


    loi = dc.Loi()
    r1 = dc.Resistance(50)
    i1 = dc.Courant(100, 'm')
    p1 = loi.Joule(r=r1, i=i1)
    p1.Info("Propriétés de p1 :")

    r2 = dc.Resistance(220)
    v2 = dc.Tension(5)
    p2 = loi.Joule(r=r2, v=v2)
    p2.Info("Propriétés de p2 :")

affiche :
    Propriétés de p1 :
    Puissance : 0.5 W (500.000000 mW)
    Propriétés de p2 :
    Puissance : 0.113636 W (113.636364 mW)
"""
        grandeurs_attendus = ['v', 'i']

        if len(grandeur) != 1:
            raise TypeError("Il faut un paramètre v ou i")
        else:
            cle = list(grandeur)
            if cle[0] not in grandeurs_attendus:
                raise TypeError("les paramètres attendus sont v ou i")
        if isinstance(r, Resistance) is False:
            raise TypeError("résistance attendue")

        # p = r*i²
        if 'i' in cle:
            if isinstance(grandeur['i'], Courant) is False:
                raise TypeError("courant attendu")

            puissance = r.Valeur()*(grandeur['i'].Valeur())**2
            return Puissance(puissance)

        # p = v²/r
        elif 'v' in cle:
            if isinstance(grandeur['v'], Tension) is False:
                raise TypeError("tension attendue")
            if r.Valeur() != 0.:
                puissance = (grandeur['v'].Valeur())**2/r.Valeur()
                return Puissance(puissance)
            elif grandeur['v'].Valeur() == 0.:
                return Puissance(0.)
            else:
                raise ValueError("La tension doit être nulle")


class Grandeur:
    """Classe relative aux grandeurs électrique en régime continu : \
tensions et courants.

Cette classe ne s'utilise pas directement.
"""
    def __init__(self):
        pass


class Tension(Grandeur):
    """ Cette classe est relative aux tensions électriques en regime continu.

Utilisation :

    from dcelectricity import dc_fr as dc
    v1 = dc.Tension(5)
"""

    def __init__(self, mantisse, prefixe=''):
        """Instanciation d'un objet Tension

mantisse -> type float
prefixe  -> type str (parmi : 'p','n','u' ou 'µ','m','k','M','G','T',\
'' par défaut)

Exemple :


    v1 = dc.Tension(0.032)
    v2 = dc.Tension(100, 'm')
"""
        Grandeur.__init__(self)
        self.__unite = "V"    # volt
        try:
            valeur = PrefixeGrandeur(mantisse, prefixe)
            self.__valeur = float(valeur)
        except:
            raise TypeError("La tension en volts doit être de type float")

    def Valeur(self):
        """ Retourne la tension en volts (type float) """
        return self.__valeur

    def __call__(self):
        """ L’objet est appelé comme une fonction \
et la méthode retourne la tension en volts (type float)

    v1 = dc.Tension(10)
    print(v1())

affiche :
    10.0
"""
        return self.__valeur

    def Info(self, message=''):
        """Affiche les propriétés de la tension.

Exemple :
    v1 = dc.Tension(0.032)
    v1.Info("Propriétés de v1 :")

affiche :
    Propriétés de v1 :
    Tension : 0.032 V (32.000000 mV)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Retourne la représentation de l'objet (utilisé par la fonction print)

Exemple :
    v1 = dc.Tension(0.032)
    print(v1)

affiche :
    Tension : 0.032 V (32.000000 mV)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        mantisse, prefixe = NotationIngenieur(self.__valeur)
        if prefixe == '':
            affichage = "Tension : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Tension : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, mantisse,
                       prefixe, self.__unite)
        return affichage

    def __add__(self, tension):
        """self.__add__(tension) <=> self + tension
Loi des branches
Retourne un objet Tension

    v1 = dc.Tension(5)
    v2 = dc.Tension(3)
    v3 = v1+v2  # Tension : 8.000000 V
"""
        return Loi().Branche('++', self, tension)

    def __sub__(self, tension):
        """self.__sub__(tension) <=> self - tension
Loi des branches
Retourne un objet Tension

    v1 = dc.Tension(5)
    v2 = dc.Tension(3)
    v3 = v1-v2  # Tension : 2.000000 V
"""
        return Loi().Branche('+-', self, tension)

    def __pos__(self):
        """self.__pos__() <=> +self
Retourne un objet Tension """
        return Tension(self.__valeur)  # objet différent

    def __neg__(self):
        """self.__neg__() <=> -self
Retourne un objet Tension"""
        return Tension(-self.__valeur)

    def __truediv__(self, parametre):
        """self.__truediv__(parametre) <=> self / parametre
Si parametre est un objet Resistance :
Loi d'Ohm
Retourne un objet Courant

    v1 = dc.Tension(5)
    r1 = dc.Resistance(1000)
    i1 = v1/r1  #  Intensité du courant : 0.005 A (5.000000 mA)

Si parametre est un objet Courant :
Loi d'Ohm
Retourne un objet Resistance

    v1 = dc.Tension(5)
    i1 = dc.Courant(5, 'm')
    r1 = v1/i1  #  Résistance : 1000 Ω (1.000000 kΩ)

Si parametre est un float :
Retourne un objet Tension

    v2 = v1/10  #  Tension : 0.5 V (500.000000 mV)

Si parametre est un objet Tension :
Retourne un float

    x = v1/v2  # x = 10.0
"""
        if isinstance(parametre, Resistance) is True:
            return Loi().Ohm(v=self, r=parametre)
        if isinstance(parametre, Tension) is True:
            return self.__valeur/parametre.Valeur()
        if isinstance(parametre, Courant) is True:
            return Loi().Ohm(v=self, i=parametre)
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Tension(self.__valeur/parametre)

    def __mul__(self, parametre):
        """self.__mul__(parametre) <=> self * parametre
Si parametre est un objet Conductance :
Loi d'Ohm
Retourne un objet Courant

    v1 = dc.Tension(5)
    g1 = dc.Conductance(0.001)
    i1 = v1*g1  #  Intensité du courant : 0.005 A (5.000000 mA)

Si parametre est un objet Courant :
Retourne un objet Puissance

    p1 = v1*i1  #  Puissance : 0.025 W (25.000000 mW)

Si parametre est un float :
Retourne un objet Tension

    v2 = v1*0.1  #  Tension : 0.5 V (500.000000 mV)
"""

        if isinstance(parametre, Conductance) is True:
            return Courant(self.__valeur*parametre.Valeur())
        if isinstance(parametre, Courant) is True:
            return Puissance(self.__valeur*parametre.Valeur())
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Tension(self.__valeur*parametre)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val est un float
Retourne un objet Tension

    v1 = dc.Tension(5)
    v2 = 0.1*v1  #  Tension : 0.5 V (500.000000 mV)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Tension(self.__valeur*val)


class Courant(Grandeur):
    """ Cette classe est relative aux courants électriques en régime continu.

Utilisation :
    from dcelectricity import dc_fr as dc
    i1 = dc.Courant(5, 'm')
"""

    def __init__(self, mantisse, prefixe=''):
        """Instanciation d'un objet Courant

mantisse -> type float
prefixe  -> type str (parmi : 'p','n','u' ou 'µ','m','k','M','G','T',\
'' par défaut)

Exemple :

    i1 = dc.Courant(32, 'm')
"""
        Grandeur.__init__(self)
        self.__unite = "A"    # ampère
        try:
            valeur = PrefixeGrandeur(mantisse, prefixe)
            self.__valeur = float(valeur)
        except:
            raise TypeError("Le paramètre valeur doit être de type float")

    def Valeur(self):
        """ Retourne l'intensité du courant en A (type float) """
        return self.__valeur

    def __call__(self):
        """ L’objet est appelé comme une fonction \
et la méthode retourne l'intensité du courant en A (type float)

    i1 = dc.Courant(32, 'm')
    print(i1())

affiche :
    0.032
"""
        return self.__valeur

    def Info(self, message=''):
        """Affiche les propriétés du courant

Exemple :
    i1 = dc.Courant(0.032)
    i1.Info("Propriétés de i1 :")

affiche :
    Propriétés de i1 :
    Intensité du courant : 0.032 A (32.000000 mA)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Retourne la représentation de l'objet (utilisé par la fonction print)

Exemple :
    i1 = dc.Courant(0.032)
    print(i1)

affiche :
    Intensité du courant : 0.032 A (32.000000 mA)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        mantisse, prefixe = NotationIngenieur(self.__valeur)
        if prefixe == '':
            affichage = "Intensité du courant : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Intensité du courant : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, mantisse,
                       prefixe, self.__unite)
        return affichage

    def __add__(self, courant):
        """self.__add__(courant) <=> self + courant
Loi des nœuds
Retourne un objet Courant

    i1 = dc.Courant(0.032)
    i2 = dc.Courant(0.050)
    i3 = i1+i2  #  Intensité du courant : 0.082 A (82.000000 mA)
"""
        return Loi().Noeud('++', self, courant)

    def __sub__(self, courant):
        """self.__sub__(courant) <=> self - courant
Loi des nœuds
Retourne un objet Courant

    i1 = dc.Courant(0.032)
    i2 = dc.Courant(0.050)
    i3 = i1-i2  #  Intensité du courant : -0.018 A (-18.000000 mA)
"""
        return Loi().Noeud('+-', self, courant)

    def __pos__(self):
        """self.__pos__() <=> +self
Retourne un objet Courant"""
        return Courant(self.__valeur)  # objet différent

    def __neg__(self):
        """self.__neg__() <=> -self
Retourne un objet Courant"""
        return Courant(-self.__valeur)

    def __truediv__(self, parametre):
        """self.__truediv__(parametre) <=> self / parametre
Si parametre est un objet Conductance :
Loi d'Ohm
Retourne un objet Tension

    i1 = dc.Courant(0.032)
    g1 = dc.Conductance(0.001)
    v1 = i1/g1  # Tension : 32.000000 V

Si parametre est un objet Tension :
Loi d'Ohm
Retourne un objet Conductance

    v1 = dc.Tension(10)
    i1 = dc.Courant(0.01)
    g1 = i1/v1  # Conductance : 0.001 S (1.000000 mS)

Si parametre est un float :
Retourne un objet Courant

    i2 = i1/10  # Intensité du courant : 0.0032 A (3.200000 mA)

Si parametre est un objet Courant :
Retourne un float

    x = i1/i2  # x = 10.0
"""
        if isinstance(parametre, Conductance) is True:
            return Tension(self.__valeur/parametre.Valeur())
        if isinstance(parametre, Courant) is True:
            return self.__valeur/parametre.Valeur()
        if isinstance(parametre, Tension) is True:
            return Conductance(self.__valeur/parametre.Valeur())
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Courant(self.__valeur/parametre)

    def __mul__(self, parametre):
        """self.__mul__(parametre) <=> self * parametre

Si parametre est un objet Resistance :
Loi d'Ohm
Retourne un objet Tension

    i1 = dc.Courant(0.032)
    r1 = dc.Resistance(1000)
    v1 = i1*r1  # Tension : 32.000000 V

Si parametre est un objet Tension :
Retourne un objet Puissance

    p1 = i1*v1  # Puissance : 1.024000 W

Si parametre est un float :
Retourne un objet Courant

    i2 = i1*10  # Intensité du courant : 0.32 A (320.000000 mA)
"""
        if isinstance(parametre, Resistance) is True:
            return Tension(self.__valeur*parametre.Valeur())
        if isinstance(parametre, Tension) is True:
            return Puissance(self.__valeur*parametre.Valeur())
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Courant(self.__valeur*parametre)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val est un float
Retourne un objet Courant

    i1 = dc.Courant(0.032)
    i2 = 10*i1  # Intensité du courant : 0.32 A (320.000000 mA)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Courant(self.__valeur*val)


class Puissance(Grandeur):
    """ Cette classe est relative aux puissances électriques en regime continu.

Utilisation :
    from dcelectricity import dc_fr as dc
    p1 = dc.Puissance(10)
"""

    def __init__(self, mantisse, prefixe=''):
        """
Instanciation d'un objet Puissance

mantisse -> type float
prefixe  -> type str (parmi : 'p','n','u' ou 'µ','m','k', 'M','G','T',\
'' par défaut)

Exemple :

    p1 = dc.Puissance(10)
    p2 = dc.Puissance(200, 'm')
"""
        Grandeur.__init__(self)
        self.__unite = "W"    # watt
        try:
            valeur = PrefixeGrandeur(mantisse, prefixe)
            self.__valeur = float(valeur)
        except:
            raise TypeError("Le paramètre valeur doit être de type float")

    def Valeur(self):
        """ Retourne la valeur de la puissance en watts (type float) """
        return self.__valeur

    def __call__(self):
        """ L’objet est appelé comme une fonction et la méthode retourne \
la puissance en watts (type float)

    p1 = dc.Puissance(0.05)
    print(p1())

affiche :
    0.05
"""
        return self.__valeur

    def Info(self, message=''):
        """
Affiche les propriétés de la puissance.

Exemple :
    p1 = dc.Puissance(0.05)
    p1.Info("Propriétés de p1 :")

affiche :
    Propriétés de p1 :
    Puissance : 0.05 W (50.000000 mW)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
Retourne la représentation de l'objet (utilisé par la fonction print)

Exemple :
    p1 = dc.Puissance(0.05)
    print(p1)

affiche :
    Puissance : 0.05 W (50.000000 mW)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        mantisse, prefixe = NotationIngenieur(self.__valeur)
        if prefixe == '':
            affichage = "Puissance : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Puissance : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, mantisse,
                       prefixe, self.__unite)
        return affichage

    def __add__(self, puissance):
        """self.__add__(puissance) <=> self + puissance
Retourne un objet Puissance"""
        return Puissance(self.__valeur + puissance.Valeur())

    def __sub__(self, puissance):
        """self.__sub__(puissance) <=> self - puissance
Retourne un objet Puissance"""
        return Puissance(self.__valeur - puissance.Valeur())

    def __pos__(self):
        """self.__pos__() <=> +self
Retourne un objet Puissance"""
        return Puissance(self.__valeur)  # objet différent

    def __neg__(self):
        """self.__neg__() <=> -self
Retourne un objet Puissance"""
        return Puissance(-self.__valeur)

    def __truediv__(self, parametre):
        """self.__truediv__(parametre) <=> self / parametre
Si parametre est un objet Tension :
Retourne un objet Courant

    p1 = dc.Puissance(0.05)
    v1 = dc.Tension(10)
    i1 = p1/v1  # Intensité du courant : 0.005 A (5.000000 mA)

Si parametre est un float :
Retourne un objet Puissance

    p2 = p1/5  # Puissance : 0.01 W (10.000000 mW)

Si parametre est un objet Courant :
Retourne un objet Tension

    v2 = p2/i1  # Tension : 2.000000 V

Si parametre est un objet Puissance :
Retourne un float

    x = p1/p2  # x = 5.0
"""
        if isinstance(parametre, Tension) is True:
            return Courant(self.__valeur/parametre.Valeur())
        if isinstance(parametre, Courant) is True:
            return Tension(self.__valeur/parametre.Valeur())
        if isinstance(parametre, Puissance) is True:
            return self.__valeur/parametre.Valeur()
        try:
            parametre = float(parametre)
        except:
            raise TypeError("nombre attendu")
        return Puissance(self.__valeur/parametre)

    def __mul__(self, val):
        """self.__mul__(val) <=> self * val
val est un float
Retourne un objet Puissance

    p1 = dc.Puissance(0.05)
    p2 = p1*10  # Puissance : 0.5 W (500.000000 mW)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Puissance(self.__valeur*val)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val est un float
Retourne un objet Puissance

    p1 = dc.Puissance(0.05)
    p2 = 10*p1  # Puissance : 0.5 W (500.000000 mW)
"""
        try:
            val = float(val)
        except:
            raise TypeError("nombre attendu")
        return Puissance(self.__valeur*val)

if __name__ == '__main__':
    import dc_fr as dc
    # aide sur le module
    help(dc)

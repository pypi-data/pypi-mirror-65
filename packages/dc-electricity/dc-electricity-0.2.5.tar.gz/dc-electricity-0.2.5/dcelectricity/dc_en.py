# -*- coding: utf8 -*-
# python 3
# (C) Fabrice Sincère

"""An educational package about linear DC electrical circuits"""

import sys
import math

__version__ = (0, 2, 5)
__author__ = "Fabrice Sincère <fabrice.sincere@ac-grenoble.fr>"

if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    exit(1)


def PrefixNotation(significand, prefix=''):
    """significand -> float
prefix  -> str
return the corresponding decimal number -> float

prefix is one of :
'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default

>>> from dcelectricity import dc_en as dc
>>> dc.PrefixNotation(20, 'm')  # 0.02
>>> dc.PrefixNotation(50, 'k')  # 50000
>>> dc.PrefixNotation(-10000)   # -10000
"""
    prefixes = {'': 1, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'µ': 1e-6,
                'm': 1e-3, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}

    return significand * prefixes[prefix]


def EngineeringNotation(val):
    """val -> float

Return a tuple (significand, prefix)
with significand between 1 and 1000

significand -> float
prefix  -> str

prefix is one of :
'p' pico, 'n', 'u' or 'µ' micro, 'm', 'k', 'M' mega, 'G', 'T', '' default

>>> from dcelectricity import dc_en as dc
>>> dc.EngineeringNotation(999)    #  (999, '')
>>> dc.EngineeringNotation(1000)   #  (1.0, 'k')
>>> dc.EngineeringNotation(-1e-6)  #  (-1.0, 'µ')
>>> dc.EngineeringNotation(0)      #  (0, '')
>>> significand, prefix = dc.EngineeringNotation(1200000)
>>> print("Resistance : {} {}Ω".format(significand, prefix))
Resistance : 1.2 MΩ
"""
    if val == 0.0:
        return (0, '')

    nbdecimal = math.log10(abs(val))

    if -15.0 <= nbdecimal < -9.0:
        return (val*1e12, 'p')
    elif -9.0 <= nbdecimal < -6.0:
        return (val*1e9, 'n')
    elif -6.0 <= nbdecimal < -3.0:
        return (val*1e6, 'µ')
    elif -3.0 <= nbdecimal < 0.0:
        return (val*1e3, 'm')
    elif 0.0 <= nbdecimal < 3.0:
        return (val, '')
    elif 3.0 <= nbdecimal < 6.0:
        return (val*1e-3, 'k')
    elif 6.0 <= nbdecimal < 9.0:
        return (val*1e-6, 'M')
    elif 9.0 <= nbdecimal < 12.0:
        return (val*1e-9, 'G')
    elif 12.0 <= nbdecimal < 15.0:
        return (val*1e-12, 'T')
    else:
        return (val, '')  # notation scientifique


class Component:
    "Component class"
    def __init__(self):
        pass


class Resistor(Component):
    "The Resistor class."

    def __init__(self, significand, prefix=''):
        """Creates Resistor object

significand -> float
prefix  -> str
prefix is one of : 'p','n','u' or 'µ','m','k','M','G','T','' default

>>> from dcelectricity import dc_en as dc
>>> r1 = dc.Resistor(22000)
>>> r2 = dc.Resistor(4.7, 'k')
"""
        Component.__init__(self)
        self.__unite = "Ω"    # ohm
        try:
            valeur = PrefixNotation(significand, prefix)
            self.__valeur = float(valeur)
        except:
            raise TypeError("value must be a float")

        if self.__valeur < 0.0:
            raise ValueError("resistance must be positive")

    def Value(self):
        "Return the resistance (measured in ohms) -> float"
        return self.__valeur

    def __call__(self):
        """Return the resistance (measured in ohms) -> float

>>> r1 = dc.Resistor(22000)
>>> r1()
22000.0
"""
        return self.__valeur

    def Info(self, message=''):
        """Return and displays the Resistor properties

>>> R1 = dc.Resistor(1,'k')
>>> R1.Info("R1 properties :")
R1 properties :
Resistance : 1000 Ω (1.000000 kΩ)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
>>> R1 = dc.Resistor(1,'k')
>>> print(R1)
Resistance : 1000 Ω (1.000000 kΩ)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        significand, prefix = EngineeringNotation(self.__valeur)
        if prefix == '':
            affichage = "Resistance : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Resistance : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, significand, prefix,
                       self.__unite)
        return affichage

    def __add__(self, resistor):
        """self.__add__(resistor) <=> self + resistor
Resistors in series
resistor -> Resistor object
Return a Resistor object

>>> r1 = dc.Resistor(22000)
>>> r2 = dc.Resistor(4.7, 'k')
>>> r3 = r1+r2
>>> r3
Resistance : 26700 Ω (26.700000 kΩ)
"""
        return Law().Rserie(self, resistor)

    def __sub__(self, resistor):
        "self.__sub__(resistor) <=> self - resistor"

        if isinstance(resistor, Resistor) is False:
                raise TypeError("Resistor expected")
        return Resistor(self.__valeur-resistor.Value())

    def __pos__(self):
        "self.__pos__() <=> +self"
        return Resistor(self.__valeur)  # objet différent

    def __floordiv__(self, resistor):
        """self.__floordiv__(resistor) <=> self // resistor
Resistors in parallel
resistor -> Resistor object
Return a Resistor object

>>> r1 = dc.Resistor(22000)
>>> r2 = dc.Resistor(4.7, 'k')
>>> r3 = r1//r2
>>> r3
Resistance : 3872.66 Ω (3.872659 kΩ)
"""
        return Law().Rparallel(self, resistor)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg
arg is a Current object or a positive float

arg -> Current object :
Ohm's law
Return a Voltage object

>>> r1 = dc.Resistor(22000)
>>> i1 = dc.Current(10, 'u')
>>> v1 = r1*i1
>>> v1
Voltage : 0.22 V (220.000000 mV)

arg -> float (positive) :
Multiplication
Return a Resistor object

>>> r2 = r1*10  # Resistance : 220000 Ω (220.000000 kΩ)
>>> r3 = r2*(r1/(r1+r2))  # Resistance : 20000 Ω (20.000000 kΩ)
"""
        if isinstance(arg, Current) is True:
            return Law().Ohm(r=self, i=arg)
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Resistor(self.__valeur*arg)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val -> float (positive)
Return a Resistor object

>>> r1 = dc.Resistor(22000)
>>> r2 = 10*r1  # Resistance : 220000 Ω (220.000000 kΩ)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Resistor(self.__valeur*val)

    def __rtruediv__(self, val):
        """self.__rmul__(val) <=> val / self
val -> float (positive)
Return a Conductance object

>>> r1 = dc.Resistor(22000)
>>> g1 = 1/r1  # Conductance : 4.54545e-05 S (45.454545 µS)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Conductance(val/self.__valeur)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is a Resistor object or a float.

arg -> Resistor object
Return a float :

>>> r1 = dc.Resistor(22000)
>>> r2 = dc.Resistor(10000)
>>> x = r1/r2  # 2.2

arg -> float
Return a Resistor object :

>>> r3 = r1/10  # Resistance : 2200 Ω (2.200000 kΩ)
"""
        if isinstance(arg, Resistor) is True:
            return self.__valeur/arg.Value()

        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")

        return Resistor(self.__valeur/arg)


class Conductance(Component):
    """The Conductance class.

>>> from dcelectricity import dc_en as dc
>>> G1 = dc.Conductance(0.1)
>>> G2 = dc.Conductance(10, 'm')
>>> V3 = dc.Voltage(3)
>>> G3 = G1+G2  # Conductance : 0.11 S (110.000000 mS)
>>> R3 = 1/G3   # Resistance : 9.090909 Ω
>>> # Ohm's law
>>> I3 = G3*V3
>>> I3
Current : 0.33 A (330.000000 mA)
"""

    def __init__(self, significand, prefix=''):
        """Creates Conductance object

significand -> float
prefix -> str (one of : 'p','n','u' ou 'µ','m','k', 'M','G','T','' default)

>>> G1 = dc.Conductance(0.1)
>>> G2 = dc.Conductance(4.7, 'm')
"""
        Component.__init__(self)
        self.__unite = "S"    # siemens
        try:
            valeur = PrefixNotation(significand, prefix)
            self.__valeur = float(valeur)
        except:
            raise TypeError("number expected")

        if self.__valeur < 0.0:
            raise ValueError("conductance must be positive")

    def Value(self):
        "Return the conductance (measured in siemens) -> float"
        return self.__valeur

    def __call__(self):
        """Return the conductance (measured in siemens) -> float

>>> G2 = dc.Conductance(4.7, 'm')
>>> G2()
0.0047
"""
        return self.__valeur

    def Info(self, message=''):
        """Return and displays the Conductance properties

>>> G1 = dc.Conductance(0.1)
>>> G1.Info("G1 properties :")
G1 properties :
Conductance : 0.1 S (100.000000 mS)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
>>> G1 = dc.Conductance(0.1)
>>> G1
Conductance : 0.1 S (100.000000 mS)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        significand, prefix = EngineeringNotation(self.__valeur)
        if prefix == '':
            affichage = "Conductance : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Conductance : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, significand, prefix,
                       self.__unite)
        return affichage

    def __add__(self, conductance):
        "self.__add__(conductance) <=> self + conductance"

        if isinstance(conductance, Conductance) is False:
                raise TypeError("Conductance expected")
        return Conductance(self.__valeur + conductance.__valeur)

    def __sub__(self, conductance):
        "self.__sub__(conductance) <=> self - conductance"

        if isinstance(conductance, Conductance) is False:
                raise TypeError("Conductance expected")
        return Conductance(self.__valeur - conductance.__valeur)

    def __pos__(self):
        "self.__pos__() <=> +self"
        return Conductance(self.__valeur)  # new object

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is a Voltage object or a float (positive)

arg -> Voltage object :
Ohm's law
Return a Current object

>>> g1 = dc.Conductance(0.01)
>>> v1 = dc.Voltage(10)
>>> i1 = g1*v1  # Current : 0.1 A (100.000000 mA)

arg -> float (positive) :
Multiplication
Return a Conductance object

>>> g2 = g1*10  # Conductance : 0.1 S (100.000000 mS)
"""
        if isinstance(arg, Voltage) is True:
            return Current(self.__valeur*arg.Value())
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Conductance(self.__valeur*arg)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val -> float (positive)
Return a Conductance object

>>> g1 = dc.Conductance(0.01)
>>> g2 = 10*g1  # Conductance : 0.1 S (100.000000 mS)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Conductance(self.__valeur*val)

    def __rtruediv__(self, val):
        """self.__rtruediv__(val) <=> val / self
val -> float (positive)
Return a Resistor object

>>> g1 = dc.Conductance(0.001)
>>> r1 = 1/g1  # Resistance : 1000 Ω (1.000000 kΩ)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Resistor(val/self.__valeur)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is a Conductance object or a float.

arg -> Conductance object :
Return a float

>>> g1 = dc.Conductance(0.01)
>>> g2 = dc.Conductance(0.2)
>>> x = g1/g2  # 0.05

arg -> float :
Return a Conductance object

>>> g3 = g1/10  # Conductance : 0.001 S (1.000000 mS)
"""
        if isinstance(arg, Conductance) is True:
            return self.__valeur/arg.Value()

        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")

        return Conductance(self.__valeur/arg)

    def __floordiv__(self, conductance):
        """self.__floordiv__(conductance) <=> self // conductance
conductances in parallel
Return a Conductance object

    g1 = dc.Conductance(0.0002)
    g2 = dc.Conductance(0.0008)
    g3 = g1//g2  # Conductance : 0.001 S (1.000000 mS)
"""
        return self.__add__(conductance)


class Law:
    """
- Kirchhoff’s current law (KCL)
- Kirchhoff’s voltage law (KVL)
- Ohm's law
- Resistors in series and parallel
- Voltage divider and current divider
- Millman's theorem
- Joule's first law (P=I²R)
- Electrical power (P=V*I)

>>> from dcelectricity import dc_en as dc
>>> law = dc.Law()
>>> v1 = dc.Voltage(5)
>>> i1 = dc.Current(20, 'µ')
>>> r1 = law.Ohm(v=v1, i=i1)
"""

    def KVL(self, signs, *voltages):
        """Kirchhoff’s voltage law

signs -> str
*voltages -> Voltage
return Voltage

Example : v4 = v1 + v2 - v3

>>> v1 = dc.Voltage(5)
>>> v2 = dc.Voltage(-8)
>>> v3 = dc.Voltage(2.5)
>>> law = dc.Law()
>>> v4 = law.KVL('++-', v1, v2, v3)
>>> v4.Info("v4 properties :")
v4 properties :
Voltage : -5.500000 V
"""

        if len(voltages) == 0:
            raise ValueError("at least one Voltage")

        for voltage in voltages:
            if isinstance(voltage, Voltage) is False:
                raise TypeError("Voltage expected")

        if not isinstance(signs, str):
            raise TypeError("string expected")

        if len(voltages) != len(signs):
            raise ValueError("signs length is wrong")
        else:
            for sign in signs:
                if sign not in "+-":
                    raise ValueError("signs string wrong format")

        valeur = 0.0
        for index, voltage in enumerate(voltages):
            if signs[index] == "+":
                valeur += voltage.Value()
            elif signs[index] == "-":
                valeur -= voltage.Value()
        return Voltage(valeur)

    def KCL(self, signs, *currents):
        """Kirchhoff’s current law

signs -> str
*currents -> Current
return Current

Example : i4 = -i1 + i2 - i3

>>> i1 = dc.Current(5, 'm')
>>> i2 = dc.Current(8, 'm')
>>> i3 = dc.Current(2.5, 'm')
>>> law = dc.Law()
>>> i4 = law.KCL('-+-', i1, i2, i3)
>>> i4.Info("i4 properties :")
i4 properties :
Current : 0.0005 A (500.000000 µA)
"""

        if len(currents) == 0:
            raise ValueError("Current expected")

        for current in currents:
            if isinstance(current, Current) is False:
                raise TypeError("Current expected")

        if not isinstance(signs, str):
            raise TypeError("string expected")

        if len(currents) != len(signs):
            raise ValueError("signs length is wrong")
        else:
            for sign in signs:
                if sign not in "+-":
                    raise ValueError("signs string wrong format")

        valeur = 0.0
        for index, current in enumerate(currents):
            if signs[index] == "+":
                valeur += current.Value()
            elif signs[index] == "-":
                valeur -= current.Value()
        return Current(valeur)

    def Ohm(self, **kwargs):
        """Ohm's law

As the case may be : v = r*i, i = v/r or r = v/i

**kwargs -> two of v, r, i
v -> Voltage
i -> Current
r -> Resistor

Example 1:

>>> v1 = dc.Voltage(5)
>>> i1 = dc.Current(20, 'µ')
>>> law = dc.Law()
>>> r1 = law.Ohm(v=v1, i=i1)
>>> r1.Info("r1 properties :")
r1 properties :
Resistance : 250000 Ω (250.000000 kΩ)

Example 2:

>>> v2 = dc.Voltage(2)
>>> r2 = dc.Resistor(100, 'k')
>>> law = dc.Law()
>>> i2 = law.Ohm(v=v2, r=r2)
>>> i2.Info("i2 properties :")
i2 properties :
Current : 2e-05 A (20.000000 µA)
"""

        grandeurs_attendus = ['v', 'r', 'i']

        if len(kwargs) != 2:
            raise ValueError("two arguments are expected")

        else:
            # liste des paramètres
            cles = list(kwargs)
            if (cles[0] not in grandeurs_attendus or
                    cles[1] not in grandeurs_attendus):
                raise ValueError("expected arguments are r, v or i")

        # v = r*i
        if 'v' not in cles:
            if isinstance(kwargs['i'], Current) is False:
                raise TypeError("Current expected")

            current = kwargs['i'].Value()

            if isinstance(kwargs['r'], Resistor) is False:
                raise TypeError("Resistor expected")

            resistance = kwargs['r'].Value()
            voltage = resistance * current
            return Voltage(voltage)

        # i = v/r
        if 'i' not in cles:
            if isinstance(kwargs['v'], Voltage) is False:
                raise TypeError("Voltage expected")

            voltage = kwargs['v'].Value()

            if isinstance(kwargs['r'], Resistor) is False:
                raise TypeError("Resistor expected")

            resistance = kwargs['r'].Value()
            current = voltage / resistance
            return Current(current)

        # r =v/i
        if 'r' not in cles:
            if isinstance(kwargs['v'], Voltage) is False:
                raise TypeError("Voltage expected")

            voltage = kwargs['v'].Value()

            if isinstance(kwargs['i'], Current) is False:
                raise TypeError("Current expected")

            current = kwargs['i'].Value()
            resistance = voltage / current
            return Resistor(resistance)

    def Rserie(self, *resistors):
        """Resistors in series

*resistors -> Resistor
return Resistor

>>> r1 = dc.Resistor(100,'k')
>>> r2 = dc.Resistor(47,'k')
>>> r3 = dc.Resistor(22,'k')
>>> law = dc.Law()
>>> Req = law.Rserie(r1, r2, r3)
>>> Req.Info("Req properties :")
Req properties :
Resistance : 169000 Ω (169.000000 kΩ)
"""

        if len(resistors) == 0:
            raise TypeError("at least one argument")

        Req = 0.0
        for r in resistors:
            if isinstance(r, Resistor) is False:
                raise TypeError("Resistor expected")
            Req += r.Value()

        return Resistor(Req)

    def Rparallel(self, *resistors):
        """Resistors in parallel

*resistors -> Resistor
return Resistor

>>> r1 = dc.Resistor(1500)
>>> r2 = dc.Resistor(1000)
>>> law = dc.Law()
>>> Req = law.Rparallel(r1, r2)
>>> Req.Info("Req properties :")
Req properties :
Resistance : 600.000000 Ω
"""

        if len(resistors) == 0:
            raise TypeError("at least one argument")

        Geq = 0.0  # conductance
        for r in resistors:
            if isinstance(r, Resistor) is False:
                raise TypeError("Resistor expected")

            if r.Value() == 0.0:
                return Resistor(0.0)
            Geq += 1.0/r.Value()

        return Resistor(1/Geq)

    def VoltageDivider(self, vtotal, r, r2):
        """Voltage divider

        vtotal
--------------------->

----[r]-----[r2]-----

   ----->
     v

vtotal -> Voltage
r, r2  -> Resistor
return v Voltage

>>> r1 = dc.Resistor(1, 'k')
>>> r2 = dc.Resistor(9, 'k')
>>> v = dc.Voltage(5)
>>> law = dc.Law()
>>> v1 = law.VoltageDivider(vtotal=v, r=r1, r2=r2)
>>> v1.Info("v1 properties :")
v1 properties :
Voltage : 0.5 V (500.000000 mV)
"""

        if isinstance(r, Resistor) is False:
                raise TypeError("Resistor expected")

        R = r.Value()
        if isinstance(r2, Resistor) is False:
                raise TypeError("Resistor expected")

        R2 = r2.Value()
        if isinstance(vtotal, Voltage) is False:
                raise TypeError("Voltage expected")

        V = vtotal.Value()
        return Voltage(V*R/(R+R2))

    def CurrentDivider(self, itotal, r, r2):
        """Current divider

                i
    ----[r]----<--     itotal
---|              |---<----
    ----[r2]---<--

itotal -> Current
r, r2  -> Resistor
return i Current

>>> r1 = dc.Resistor(100)
>>> r2 = dc.Resistor(900)
>>> i = dc.Current(100, 'm')
>>> law = dc.Law()
>>> i1 = law.CurrentDivider(itotal=i, r=r1, r2=r2)
>>> i1.Info("i1 properties :")
i1 properties :
Current : 0.09 A (90.000000 mA)
"""

        if isinstance(r, Resistor) is False:
            raise TypeError("Resistor expected")

        R = r.Value()
        if isinstance(r2, Resistor) is False:
            raise TypeError("Resistor expected")

        R2 = r2.Value()
        if isinstance(itotal, Current) is False:
            raise TypeError("Current expected")

        I = itotal.Value()
        return Current(I*R2/(R+R2))

    def Millman(self, v_r, i=[]):
        """Millman's theorem

Millman(self, v_r=[(v1, r1), (v2, r2) ...], i=[i1, i2...])

v_r -> list of tuples
i -> list of Current
return Voltage

>>> gnd = dc.Voltage(0)
>>> E = dc.Voltage(10)
>>> R1 = dc.Resistor(1000)
>>> R2 = dc.Resistor(10000)
>>> R3 = dc.Resistor(2200)
>>> law = dc.Law()
>>> v2 = law.Millman(v_r = [(E, R1), (gnd, R2), (gnd, R3)])
>>> v2.Info("v2 properties :")
v2 properties :
Voltage : 6.432749 V
"""
        if isinstance(v_r, list) is False:
                raise TypeError("list expected for v_r argument")

        if len(v_r) == 0:
            raise TypeError("v_r must contain at least one item")

        somme_v_sur_R = 0.0
        somme_1_sur_R = 0.0

        for elt in v_r:
            if isinstance(elt, tuple) is False:
                raise TypeError("tuple expected")
            if len(elt) != 2:
                raise TypeError("tuple must contain two items")
            if isinstance(elt[0], Voltage) is False:
                raise TypeError("Voltage expected")
            if isinstance(elt[1], Resistor) is False:
                raise TypeError("Resistor expected")
            somme_v_sur_R += elt[0].Value()/elt[1].Value()
            somme_1_sur_R += 1/elt[1].Value()

        if isinstance(i, list) is False:
            raise TypeError("list expected")

        itotal = 0.0
        for current in i:
            if isinstance(current, Current) is False:
                raise TypeError("Current expected")
            itotal += current.Value()

        voltage = (somme_v_sur_R + itotal)/somme_1_sur_R
        return Voltage(voltage)

    def Power(self, v, i):
        """Electrical power (P=V*I)

v -> Voltage
i -> Current
return Power object

Note : don't confuse Law.Power() and Power()

>>> law = dc.Law()
>>> v1 = dc.Voltage(5)
>>> i1 = dc.Current(100, 'm')
>>> p1 = law.Power(v=v1, i=i1)
>>> p1.Info("p1 properties :")
p1 properties :
Power : 0.5 W (500.000000 mW)
"""
        if isinstance(v, Voltage) is False:
                    raise TypeError("Voltage expected")

        if isinstance(i, Current) is False:
                    raise TypeError("Current expected")

        return Power(v.Value()*i.Value())

    def Joule(self, r, **kwarg):
        """Joule's first law

p = r*i² or p = v²/r

**kwarg -> v or i

v -> Voltage
i -> Current
r -> Resistor
return Power

>>> law = dc.Law()
>>> r1 = dc.Resistor(50)
>>> i1 = dc.Current(100, 'm')
>>> p1 = law.Joule(r=r1, i=i1)
>>> p1.Info("p1 properties :")
p1 properties :
Power : 0.5 W (500.000000 mW)

>>> r2 = dc.Resistor(220)
>>> v2 = dc.Voltage(5)
>>> p2 = law.Joule(r=r2, v=v2)
>>> p2.Info("p2 : properties ")
p2 properties :
Power : 0.113636 W (113.636364 mW)
"""
        grandeurs_attendus = ['v', 'i']

        if len(kwarg) != 1:
            raise TypeError("one argument expected")
        else:
            cle = list(kwarg)
            if cle[0] not in grandeurs_attendus:
                raise TypeError("argument v or i expected")
        if isinstance(r, Resistor) is False:
            raise TypeError("Resistor expected")

        # p = r*i²
        if 'i' in cle:
            if isinstance(kwarg['i'], Current) is False:
                raise TypeError("Current expected")

            power = r.Value()*(kwarg['i'].Value())**2
            return Power(power)

        # p = v²/r
        elif 'v' in cle:
            if isinstance(kwarg['v'], Voltage) is False:
                raise TypeError("Voltage expected")
            if r.Value() != 0.:
                power = (kwarg['v'].Value())**2/r.Value()
                return Power(power)
            elif kwarg['v'].Value() == 0.:
                return Power(0.)
            else:
                raise ValueError("voltage must be 0")


class ElectricalQuantity:
    "ElectricalQuantity class"
    def __init__(self):
        pass


class Voltage(ElectricalQuantity):
    """The Voltage class.

>>> from dcelectricity import dc_en as dc
>>> v1 = dc.Voltage(5)
"""

    def __init__(self, significand, prefix=''):
        """Creates Voltage object

significand -> float
prefix -> str (one of : 'p','n','u' ou 'µ','m','k','M','G','T','' default)

>>> v1 = dc.Voltage(0.032)
>>> v2 = dc.Voltage(100, 'm')
"""
        ElectricalQuantity.__init__(self)
        self.__unite = "V"    # volt
        try:
            valeur = PrefixNotation(significand, prefix)
            self.__valeur = float(valeur)
        except:
            raise TypeError("number expected")

    def Value(self):
        "Return the voltage (measured in volts) -> float"
        return self.__valeur

    def __call__(self):
        """ Return the voltage (measured in volts) -> float

>>> v1 = dc.Voltage(10)
>>> v1()
10.0
"""
        return self.__valeur

    def Info(self, message=''):
        """Return and displays the Voltage properties

>>> v1 = dc.Voltage(0.032)
>>> v1.Info("v1 properties :")
v1 properties :
Voltage : 0.032 V (32.000000 mV)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
>>> v1 = dc.Voltage(0.032)
>>> v1
Voltage : 0.032 V (32.000000 mV)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        significand, prefix = EngineeringNotation(self.__valeur)
        if prefix == '':
            affichage = "Voltage : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Voltage : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, significand,
                       prefix, self.__unite)
        return affichage

    def __add__(self, voltage):
        """self.__add__(voltage) <=> self + voltage
Kirchhoff’s voltage law
Return Voltage

>>> v1 = dc.Voltage(5)
>>> v2 = dc.Voltage(3)
>>> v3 = v1+v2  # Voltage : 8.000000 V
"""
        return Law().KVL('++', self, voltage)

    def __sub__(self, voltage):
        """self.__sub__(voltage) <=> self - voltage
Kirchhoff’s voltage law
Return Voltage

>>> v1 = dc.Voltage(5)
>>> v2 = dc.Voltage(3)
>>> v3 = v1-v2  # Voltage : 2.000000 V
"""
        return Law().KVL('+-', self, voltage)

    def __pos__(self):
        """self.__pos__() <=> +self
Return Voltage """
        return Voltage(self.__valeur)  # new object

    def __neg__(self):
        """self.__neg__() <=> -self
Return Voltage"""
        return Voltage(-self.__valeur)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Resistor, Current, Voltage or float.

arg -> Resistor :
Ohm's law
Return Current

>>> v1 = dc.Voltage(5)
>>> r1 = dc.Resistor(1000)
>>> i1 = v1/r1  #  Current : 0.005 A (5.000000 mA)

arg -> Current :
Ohm's law
Return Resistor

>>> v1 = dc.Voltage(5)
>>> i1 = dc.Current(5, 'm')
>>> r1 = v1/i1  #  Resistance : 1000 Ω (1.000000 kΩ)

arg -> float :
Return Voltage

>>> v2 = v1/10  #  Voltage : 0.5 V (500.000000 mV)

arg -> Voltage :
Return float

>>> x = v1/v2  # x = 10.0
"""
        if isinstance(arg, Resistor) is True:
            return Law().Ohm(v=self, r=arg)
        if isinstance(arg, Voltage) is True:
            return self.__valeur/arg.Value()
        if isinstance(arg, Current) is True:
            return Law().Ohm(v=self, i=arg)
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Voltage(self.__valeur/arg)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is Conductance, Current or float.

arg ->  Conductance :
Ohm's law
Return Current

>>> v1 = dc.Voltage(5)
>>> g1 = dc.Conductance(0.001)
>>> i1 = v1*g1  #  Current : 0.005 A (5.000000 mA)

arg -> Current :
Return Power

>>> p1 = v1*i1  #  Power : 0.025 W (25.000000 mW)

arg -> float :
Return Voltage

>>> v2 = v1*0.1  #  Voltage : 0.5 V (500.000000 mV)
"""

        if isinstance(arg, Conductance) is True:
            return Current(self.__valeur*arg.Value())
        if isinstance(arg, Current) is True:
            return Power(self.__valeur*arg.Value())
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Voltage(self.__valeur*arg)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val -> float
Return Voltage

>>> v1 = dc.Voltage(5)
>>> v2 = 0.1*v1  #  Voltage : 0.5 V (500.000000 mV)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Voltage(self.__valeur*val)


class Current(ElectricalQuantity):
    """The Current class

>>> from dcelectricity import dc_en as dc
>>> i1 = dc.Current(5, 'm')
"""

    def __init__(self, significand, prefix=''):
        """Creates Current object

significand -> float
prefix -> str (one of : 'p','n','u' ou 'µ','m','k','M','G','T','' default)

>>> i1 = dc.Current(32, 'm')
"""
        ElectricalQuantity.__init__(self)
        self.__unite = "A"    # ampère
        try:
            valeur = PrefixNotation(significand, prefix)
            self.__valeur = float(valeur)
        except:
            raise TypeError("number expected")

    def Value(self):
        "Return the current (measured in ampères) -> float"
        return self.__valeur

    def __call__(self):
        """Return the current (measured in ampères) -> float

>>> i1 = dc.Current(32, 'm')
>>> i1()
0.032
"""
        return self.__valeur

    def Info(self, message=''):
        """Return and displays the Current properties

>>> i1 = dc.Current(0.032)
>>> i1.Info("i1 properties :")
i1 properties :
Current : 0.032 A (32.000000 mA)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
>>> i1 = dc.Current(0.032)
>>> i1
Current : 0.032 A (32.000000 mA)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        significand, prefix = EngineeringNotation(self.__valeur)
        if prefix == '':
            affichage = "Current : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Current : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, significand,
                       prefix, self.__unite)
        return affichage

    def __add__(self, current):
        """self.__add__(current) <=> self + current
Kirchhoff’s current law
Return Current

>>> i1 = dc.Current(0.032)
>>> i2 = dc.Current(0.050)
>>> i3 = i1+i2  #  Current : 0.082 A (82.000000 mA)
"""
        return Law().KCL('++', self, current)

    def __sub__(self, current):
        """self.__sub__(current) <=> self - current
Kirchhoff’s current law
Return Current

>>> i1 = dc.Current(0.032)
>>> i2 = dc.Current(0.050)
>>> i3 = i1-i2  #  Current : -0.018 A (-18.000000 mA)
"""
        return Law().KCL('+-', self, current)

    def __pos__(self):
        """self.__pos__() <=> +self
Return Current"""
        return Current(self.__valeur)  # objet différent

    def __neg__(self):
        """self.__neg__() <=> -self
Return Current"""
        return Current(-self.__valeur)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is Current, Conductance, Voltage or float.

arg -> Conductance :
Ohm's law
Return Voltage

>>> i1 = dc.Current(0.032)
>>> g1 = dc.Conductance(0.001)
>>> v1 = i1/g1  # Voltage : 32.000000 V

arg -> Voltage :
Ohm's law
Return Conductance

    v1 = dc.Voltage(10)
    i1 = dc.Current(0.01)
    g1 = i1/v1  # Conductance : 0.001 S (1.000000 mS)

arg -> float :
Return Current

>>> i2 = i1/10  # Current : 0.0032 A (3.200000 mA)

arg -> Current :
Return float

>>> x = i1/i2  # x = 10.0
"""
        if isinstance(arg, Conductance) is True:
            return Voltage(self.__valeur/arg.Value())
        if isinstance(arg, Current) is True:
            return self.__valeur/arg.Value()
        if isinstance(arg, Voltage) is True:
            return Conductance(self.__valeur/arg.Value())
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Current(self.__valeur/arg)

    def __mul__(self, arg):
        """self.__mul__(arg) <=> self * arg

arg is Resistor, Voltage or float.

arg -> Resistor :
Ohm's law
Return Voltage

>>> i1 = dc.Current(0.032)
>>> r1 = dc.Resistor(1000)
>>> v1 = i1*r1  # Voltage : 32.000000 V

arg -> Voltage :
Return Power

>>> p1 = i1*v1  # Power : 1.024000 W

arg -> float :
Return Current

>>> i2 = i1*10  # Current : 0.32 A (320.000000 mA)
"""
        if isinstance(arg, Resistor) is True:
            return Voltage(self.__valeur*arg.Value())
        if isinstance(arg, Voltage) is True:
            return Power(self.__valeur*arg.Value())
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Current(self.__valeur*arg)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val -> float
Return Current

>>> i1 = dc.Current(0.032)
>>> i2 = 10*i1  # Current : 0.32 A (320.000000 mA)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Current(self.__valeur*val)


class Power(ElectricalQuantity):
    """ The Power class

>>> from dcelectricity import dc_en as dc
>>> p1 = dc.Power(10)
"""

    def __init__(self, significand, prefix=''):
        """Creates Power object

significand -> float
prefix -> str (one of : 'p','n','u' ou 'µ','m','k', 'M','G','T','' default)

>>> p1 = dc.Power(10)
>>> p2 = dc.Power(200, 'm')
"""
        ElectricalQuantity.__init__(self)
        self.__unite = "W"    # watt
        try:
            valeur = PrefixNotation(significand, prefix)
            self.__valeur = float(valeur)
        except:
            raise TypeError("number expected")

    def Value(self):
        "Return the electrical power (measured in watts) -> float"
        return self.__valeur

    def __call__(self):
        """ Return the electrical power (measured in watts) -> float

>>> p1 = dc.Power(0.05)
>>> p1()
0.05
"""
        return self.__valeur

    def Info(self, message=''):
        """Return and displays the Power properties

>>> p1 = dc.Power(0.05)
>>> p1.Info("p1 properties :")
p1 properties :
Power : 0.05 W (50.000000 mW)
"""
        affichage = '' if message is '' else message + '\n'
        affichage += self.__str__()
        print(affichage)
        return affichage

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
>>> p1 = dc.Power(0.05)
>>> p1
Power : 0.05 W (50.000000 mW)
"""
        # Rmq : ce mécanisme est utilisé par la méthode Info()

        significand, prefix = EngineeringNotation(self.__valeur)
        if prefix == '':
            affichage = "Power : {:f} {}".\
                format(self.__valeur, self.__unite)
        else:
            affichage = "Power : {:g} {} ({:f} {}{})".\
                format(self.__valeur, self.__unite, significand,
                       prefix, self.__unite)
        return affichage

    def __add__(self, power):
        """self.__add__(power) <=> self + power
Return Power"""
        return Power(self.__valeur + power.Value())

    def __sub__(self, power):
        """self.__sub__(power) <=> self - power
Return Power"""
        return Power(self.__valeur - power.Value())

    def __pos__(self):
        """self.__pos__() <=> +self
Return Power"""
        return Power(self.__valeur)  # new object

    def __neg__(self):
        """self.__neg__() <=> -self
Return Power"""
        return Power(-self.__valeur)

    def __truediv__(self, arg):
        """self.__truediv__(arg) <=> self / arg

arg is a Voltage, Current, Power or float

arg -> Voltage :
Return Current

>>> p1 = dc.Power(0.05)
>>> v1 = dc.Voltage(10)
>>> i1 = p1/v1  # Current : 0.005 A (5.000000 mA)

arg -> float :
Return Power

>>> p2 = p1/5  # Power : 0.01 W (10.000000 mW)

arg -> Current :
Return Voltage

>>> v2 = p2/i1  # Voltage : 2.000000 V

arg -> Power :
Return float

>>> x = p1/p2  # x = 5.0
"""
        if isinstance(arg, Voltage) is True:
            return Current(self.__valeur/arg.Value())
        if isinstance(arg, Current) is True:
            return Voltage(self.__valeur/arg.Value())
        if isinstance(arg, Power) is True:
            return self.__valeur/arg.Value()
        try:
            arg = float(arg)
        except:
            raise TypeError("number expected")
        return Power(self.__valeur/arg)

    def __mul__(self, val):
        """self.__mul__(val) <=> self * val
val -> float
Return a Power object

>>> p1 = dc.Power(0.05)
>>> p2 = p1*10  # Power : 0.5 W (500.000000 mW)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Power(self.__valeur*val)

    def __rmul__(self, val):
        """self.__rmul__(val) <=> val * self
val -> float
Return a Power object

>>> p1 = dc.Power(0.05)
>>> p2 = 10*p1  # Power : 0.5 W (500.000000 mW)
"""
        try:
            val = float(val)
        except:
            raise TypeError("number expected")
        return Power(self.__valeur*val)

if __name__ == '__main__':
    import dc_en as dc
    help(dc)

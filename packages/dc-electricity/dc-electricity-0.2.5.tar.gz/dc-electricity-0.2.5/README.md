## dcelectricity package

The aim of this project is to understand the rudiments of DC electrical circuits and their functioning (primary and secondary school curricula).

### Basic electrical quantities

- Voltage (volt)
- Current (ampère)
- Resistance (ohm)
- Conductance (siemens)
- Power (watt)

### Electrical laws

- Kirchhoff’s current law
- Kirchhoff’s voltage law
- Ohm's law
- Resistors in series and parallel
- Voltage divider and current divider
- Millman's theorem
- Joule's first law (P=I²R)
- Power law (P=V*I)


### A complete example

#### DC Circuit diagram

```
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

```

Datas :
E = 12 V ; R1 = 1 kΩ ; R2 = 2.7 kΩ ; R3 = 1.8 kΩ    
What are the I1, I2, I3 currents ?   
What are the V1, V2 voltages ?  


```python  
>>> from dcelectricity.dc_en import *  # english version
>>> # from dcelectricity.dc_fr import *  # french version
>>> E = Voltage(12)
>>> E
Voltage : 12.000000 V
>>> R1 = Resistor(1, 'k')
>>> R1
Resistance : 1000 Ω (1.000000 kΩ)
>>> R2 = Resistor(2.7, 'k')
>>> R3 = Resistor(1.8, 'k')
>>> R23 = R2//R3  # resistances in parallel
>>> R23
Resistance : 1080 Ω (1.080000 kΩ)
>>> Req = R1 +R23  # resistances in series
>>> Req
Resistance : 2080 Ω (2.080000 kΩ)
>>> I1 = E/Req  # Ohm's law
>>> I1
Current : 0.00576923 A (5.769231 mA)
>>> V1 = R1*I1  # Ohm's law
>>> V1
Voltage : 5.769231 V
>>> V2 = E -V1  # Kirchhoff’s voltage law
>>> V2
Voltage : 6.230769 V
>>> I2 = V2/R2  # Ohm's law
>>> I2
Current : 0.00230769 A (2.307692 mA)
>>> I3 = I1 -I2  # Kirchhoff’s current law
>>> I3
Current : 0.00346154 A (3.461538 mA)
```

#### Resistances and conductances

```python
>>> G2 = 1/R2
>>> G2
Conductance : 0.00037037 S (370.370370 µS)
>>> G3 = 1/R3
>>> 1/(G2 +G3)
Resistance : 1080 Ω (1.080000 kΩ)
>>> R2*(R3/(R2 +R3))
Resistance : 1080 Ω (1.080000 kΩ)
>>> 1/(1/R2 +1/R3)
Resistance : 1080 Ω (1.080000 kΩ)
```

#### Law class

```python
>>> law = Law()
>>> # voltage divider
>>> V2 = law.VoltageDivider(vtotal=E, r=R2//R3, r2=R1)
>>> V2
Voltage : 6.230769 V
>>> # Millman's theorem
>>> gnd = dc.Voltage(0)
>>> V2 = law.Millman(v_r=[(E, R1), (gnd, R2), (gnd, R3)])
>>> V2
Voltage : 6.230769 V
>>> (E/R1)/(1/R1 +1/R2 +1/R3)
Voltage : 6.230769 V
>>> V2/E
0.5192307692307693
>>> # current divider
>>> I3 = law.CurrentDivider(itotal=I1, r=R3, r2=R2)
>>> I3
Current : 0.00346154 A (3.461538 mA)
>>> I1*R2/(R2 +R3)
Current : 0.00346154 A (3.461538 mA)
```

#### Electrical power, Joule's first law

```python
>>> P = E*I1  # source power
>>> P
Power : 0.0692308 W (69.230769 mW)
>>> P1 = law.Joule(r=R1, i=I1)
>>> P1
Power : 0.033284 W (33.284024 mW)
>>> R1*I1*I1
Power : 0.033284 W (33.284024 mW)
>>> law.Joule(r=R1, v=V1)
Power : 0.033284 W (33.284024 mW)
>>> V1*(V1/R1)
Power : 0.033284 W (33.284024 mW)
>>> P2 = law.Joule(r=R2, i=I2)
>>> P2
Power : 0.0143787 W (14.378698 mW)
>>> P3 = law.Joule(r=R3, i=I3)
Power : 0.021568 W (21.568047 mW)
>>> P1 +P2 +P3
Power : 0.0692308 W (69.230769 mW)
```

### Advantages and limitations

This module manages basic arithmetic operations (+, -, *, /) as well as // which designates two resistors in parallel.  

The consistency of the units is checked :  

```python
>>> V3 = V1 -V2 +I3
TypeError
>>> I = I1 +0.5
TypeError
>>> I2 = Current(0.5)
>>> I = I1 +I2
>>> I = 5*I2 -V1/R1 +I3
```

The result of an operation must give a quantity whose unit is one of : V, A, Ω, S, W, no unit.  
Otherwise, you will get an error :   

```python
>>> R1/V1           # Ω/V -> Error
TypeError
>>> R2*(R3/(R2 +R3))  # Ω*(Ω/Ω) -> Ω*() -> Ω
>>> R2*R3/(R2 +R3)  # Ω*Ω -> Error
TypeError
>>> P = V1*(V1/R1)  # V*(V/Ω) -> V*A -> W
>>> P = V1*V1/R1    # V*V -> Error
TypeError
>>> V1()**2/R1()
```





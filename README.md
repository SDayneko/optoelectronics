<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

# Optoelectronics
It is software used to test optoelectronic devices.
The NI-VISA is used to control a Keithley  source measure unit (SMU) .  Additional information about NI-VISA can be found on the following website: https://pyvisa.readthedocs.io/en/1.8/getting_nivisa.html

Keithley2612B library was written on Python to control [Keithley 2612B](https://www.tek.com/keithley-source-measure-units/smu-2600b-series-sourcemeter).
Please, contact the writer of the program to add other Kiethly SMU models.

## Before to start:
Use the next command to install necessary libraries::
```bash
python -m pip install -r requirements.txt
```

## Script to check connection of the keithley SMU to the PC:

J-V_curve.py program was written on Python to check correct connection of the Keithley 2612B SMU and measures voltage dependent current on Channel A and current on Channel B. The data from the collected J-V curve will be saved in a csv-file.

First, use your own adress of connection Keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```

![Keithley connection](https://github.com/SDayneko/optoelectronics/blob/main/img/connection_keithley.png)

Then, use the next command to start script:
```bash
python J-V_curve.py
```

Before starting the J-V curve program, the IP address needs to be changed depending on which SMU you are using. Use the following code to check your connection of the Keithley SMU to the PC (check_connection.py, script):
```python
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
```
or use the next command to start script:
```bash
python check_connection.py
```
![Keithley connection](https://github.com/SDayneko/optoelectronics/blob/main/img/connection_keithley.png)

## Script to measure light emitting diodes (OLEDs, PLEDs, QLEDs, QD-OLEDs and PeLEDs)
<ul class="list-group">
  <li class="list-group-item">OLEDs - organic light-emitting diodes</li>
  <li class="list-group-item">PLEDs - polymer light-emitting diodes</li>
  <li class="list-group-item">QLEDs - quantum dots light-emitting diodes</li>
  <li class="list-group-item">QD-OLEDs - quantum dots-organic light-emitting diodes</li>
  <li class="list-group-item">PeLEDs - perovskite light-emitting diodes</li>
</ul>

Use the performance_LED.py script to measure and calculate the performance of LEDs. 
All data will be saved in a csv-file.

First, use your own adress of connection Keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```
![Keithley connection](https://github.com/SDayneko/optoelectronics/blob/main/img/connection_keithley.png)

## Script to measure photovoltaic devices (OPVs, OSCs, PSCs and QDSCs)
<ul class="list-group">
  <li class="list-group-item">OPVs - organic photovoltaics</li>
  <li class="list-group-item">OSCs - organic solar cells</li>
  <li class="list-group-item">PSCs - perovskite solar cells</li>
  <li class="list-group-item">QDSCs - quantum dots solar cells</li>
</ul>

1. Geometrical of the setup and characteristics of the indoor light source.

In this example, the geometrical of the setup where the photodetector is placed on-axis in front of the indoor light source (white warm LED) to detect emitted light in the forward perpendicular direction is present in Figure 1. The distance (D) between the photodetector and white warm LED is chosen between 0.2 and 2 m (it depends on the emissivity of the white light source) to provide sufficient surface illumination.

![The setup system to measure light intensity of white LED.](https://github.com/SDayneko/optoelectronics/blob/main/img/Figure_1.png)

To measure the electroluminescent spectrum of light source the spectrometer coupled to an optical fibre has used. The calibrated lamp of known spectral emissivity has used to obtain a spectral correction for the spectrometer and optical fibre combined system.

The light intensity (Eλ), in W/m^2, is defined as:

![Equation 1](https://github.com/SDayneko/optoelectronics/blob/main/img/Equation_1.png)

where Ipd - the current density in the Si-photodiode (A/m^2); S(λ) - normalized spectrum of source (LED) is measured as a function of wavelength has units of “count”, R(λ) is a function of the wavelength of the calibrated Si photodiode has units of A/W (Figure 2).

![Responsivity of the photodetector](https://github.com/SDayneko/optoelectronics/blob/main/img/Figure_2.png)

The same result can be obtained by integrate the electroluminescent spectrum S'(λ) of the white warm LED by measuring calibrated spectrometer, optical fibre and integrating sphere. The electroluminescent spectrum S'(λ) of the white warm LED is shown in Supplementary Figure 3. Integrated this spectrum we obtained the light power (Pin) on the surface.

![Electroluminescence spectrum of the white warm LED](https://github.com/SDayneko/optoelectronics/blob/main/img/Figure_3.png)

Next, calculate the illuminance of a light source Ev in lm/m^2 = lux:

![Equation 2](https://github.com/SDayneko/optoelectronics/blob/main/img/Equation_2.png)

where the coefficient Km is equal to 683 lm/W, V(λ) is the spectral luminosity factor for human photopic vision (Figure S4). Note that this function is usually given normalized at a wavelength of ~555 nm; in which case the function must be multiplied by a factor Km of ~683 lm/W before being employed in the calculations.

![The standard sensitivity curve of human eye.](https://github.com/SDayneko/optoelectronics/blob/main/img/Figure_3.png)

2. The next parameters must calculate for the PV script (performance_PV.py) and changed:

The "int_si_spec" is equal:

![int_si_spec](https://github.com/SDayneko/optoelectronics/blob/main/img/int_si_spec.png)

The "int_spec" is equal:

![int_spec](https://github.com/SDayneko/optoelectronics/blob/main/img/int_si_spec.png)

The "eye_el" is equal:

![eye_el](https://github.com/SDayneko/optoelectronics/blob/main/img/eye_el.png)

Also, change the size of the Si-photodiode ("si_p_area") and size of active area of device ("dev_area")

3. Use the performance_PV.py script to measure and calculate the performance of LEDs. 
All data will be saved in a csv-file.

First, use your own adress of connection Keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```
![Keithley connection](https://github.com/SDayneko/optoelectronics/blob/main/img/connection_keithley.png)

## License
[MIT](https://github.com/SDayneko/optoelectronics/blob/main/LICENSE)
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

# optoelectronics
It is software used to test optoelectronic devices.
The NI-VISA is used to control a Keithley  source measure unit (SMU) .  Additional information about NI-VISA can be found on the following website: https://pyvisa.readthedocs.io/en/1.8/getting_nivisa.html

Keithley2612B library was written on Python to control Keithley 2612B.
Please, contact the writer of the program to add other Kiethly SMU models.

## Before to start.

## Script to check connection of the keithley SMU to the PC:

J-V_curve.py program was written on Python to check correct connection of the Keithley2612B and measures voltage dependent current on Channel A and current on Channel B. The data from the collected J-V curve will be saved in a csv-file.

First, use your own adress of connection keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```
Then, use the next command to start script:
```bash
python J-V_curve.py
```

Before starting the J-V curve program, the IP address needs to be changed depending on which SMU you are using. Use the following code to check your connection of the keithley SMU to the PC (check_connection.py, script):
```python
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
```
or use the next command to start script:
```bash
python check_connection.py
```

## Script to measure light emitting diodes (OLEDs, PLEDs, QLEDs, QD-OLEDs and PeLEDs)
OLEDs - organic light-emitting diodes
PLEDs - polymer light-emitting diodes
QLEDs - quantum dots light-emitting diodes
QD-OLEDs - quantum dots-organic light-emitting diodes
PeLEDs - perovskite light-emitting diodes

Use the performance_LED.py script to measure and calculate the performance of LEDs. 
All data will be saved in a csv-file.

First, use your own adress of connection keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```

## Script to measure photovoltaic devices (OPVs, OSCs, PSCs and QDSCs)
OPVs - organic photovoltaics
OSCs - organic solar cells
PSCs - perovskite solar cells
QDSCs - quantum dots solar cells

Use the performance_PV.py script to measure and calculate the performance of LEDs. 
All data will be saved in a csv-file.

First, use your own adress of connection keythley SMU to PC, here is an example of my conncetion in the script:
```python
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')
```

## License
[MIT](https://github.com/SDayneko/optoelectronics/blob/main/LICENSE)
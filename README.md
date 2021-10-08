# optoelectronics
It is software used to test optoelectronic devices.
The NI-VISA is used to control a Keithley  source measure unit (SMU) .  Additional information about NI-VISA can be found on the following website: https://pyvisa.readthedocs.io/en/1.8/getting_nivisa.html

Keithley2612B library was written on Python to control Keithley 2612B.
Please, contact the writer of the program to add other models of Keithley.

J-V_curve.py program was written on Python to check correct connection of the Keithley2612B and measures voltage dependent current on Channel A and current on Channel B. The data from the collected J-V curve will be saved in a csv-file.

Before starting the J-V curve program, the IP address needs to be changed depending on which SMU you are using. Use the following code to check your connection of the keithley SMU to the PC (check_connection.py, script):
```
$ import pyvisa
$ rm = pyvisa.ResourceManager()
$ print(rm.list_resources())
```

Finally, use the performance_LED.py script to measure and calculate  the performance of OLEDs/QLEDs. 
All data will be saved in a csv-file.


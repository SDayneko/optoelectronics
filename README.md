# optoelectronics
It is software to test optoelectronic devices.

The NI-VISA is used to control Keithley. The additional information about NI-VISA can be found on the website: https://pyvisa.readthedocs.io/en/1.8/getting_nivisa.html

Keithley2612B library was written on Python to control Keithley 2612B.

J-V_curve.py program was written on Python to chack correct connection of the Keithley2612B and measure current depends on the voltage on Channel A and current on Channel B. The data of J-V curve will save in csv-file. 

Before starting the program J-V curve needs to change the IP address depending on which source meter you are using.
Use the next code to chack your connection the keithley to the PC (chack_connection.py):
```
$ import pyvisa
$ rm = pyvisa.ResourceManager()
$ print(rm.list_resources())
```

Use the performance_LED.py to measure and calculate of the performance OLEDs/QLEDs.
All data will save in csv-file. 

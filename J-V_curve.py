"""
J-V curve program was written to measure current depends on the voltage on Channel A and measure current on Channel B.
The data will save in the CSV-file and the graphic of the data will save in the PDF-file.
written by: Sergey Dayneko
website: www.dayneko.org
last modified: 2021-10-04
"""

from Keithley2612B import SMU2612B
import matplotlib.pyplot as plt
import datetime
import csv
import time

""" ******* Connect to the Sourcemeter ******** """
# initialize the Sourcemeter and connect to it
# you may need to change the IP address depending on which sourcemeter you are using
sm = SMU2612B('USB0::0x05E6::0x2612::4439973::INSTR')

# get one channel of the Sourcemeter (we only need one for this measurement)
smu_A = sm.get_channel(sm.CHANNEL_A)
smu_B = sm.get_channel(sm.CHANNEL_B)

""" ******* Configure the SMU Channel A ******** """
# reset to default settings
smu_A.reset()
# setup the operation mode
smu_A.set_mode_voltage_source()
# set the voltage and current parameters
smu_A.set_voltage_range(10)
smu_A.set_voltage_limit(10)
smu_A.set_voltage(0)
smu_A.set_current(0)
smu_A.enable_current_autorange
smu_A.display_current()
smu_A.set_sense_2wire()
smu_A.set_measurement_speed_normal()
""" ******* Configure the SMU Channel B ******** """

# reset to default settings
smu_B.reset()
# set the voltage and current parameters
smu_B.display_current()
smu_B.set_voltage_range(0.2)
smu_B.set_voltage_limit(0.2)
smu_B.enable_current_autorange
smu_B.set_sense_2wire()
smu_B.set_measurement_speed_normal()

# Create unique filenames for saving the data
time_for_name = datetime.datetime.now().strftime("%Y_%m_%d")

filename_csv = 'test-' + time_for_name +'-scan_1.csv'
filename_pdf = 'test-' + time_for_name +'-scan_1.pdf'
# Header for
with open(filename_csv, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',  lineterminator='\n')
        writer.writerow(["Voltage (V)", "Current (mA)", "Current_pd (mA)"])
""" ******* Make a voltage-sweep and do some measurements ******** """
# define sweep parameters
sweep_start = -2
sweep_end = 5
sweep_step = 0.1
delay_time = 10e-3 # 10 ms
steps = int((sweep_end - sweep_start) / sweep_step) + 1

# define variables we store the measurement in
data_current = []
data_voltage = []
data_current_pd = []

# enable the output
smu_A.enable_output()
smu_B.enable_output()

time_start = time.time()
# step through the voltages and get the values from the device
for nr in range(steps):
        time.sleep(delay_time)
        # calculate the new voltage we want to set
        voltage_to_set = sweep_start + (sweep_step * nr)
        # set the new voltage to the SMU
        smu_A.set_voltage(voltage_to_set)
        # get current and voltage from the SMU and append it to the list so we can plot it later
        [current, voltage] = smu_A.measure_current_and_voltage()
        if abs(current) >= 0.09 and abs(current) <= 0.19:
                smu_A.set_current_range(0.2)
                smu_A.set_current_limit(0.2)
        if abs(current) > 0.19 and abs(current) <= 0.29:
                smu_A.set_current_range(0.3)  #300mA
                smu_A.set_current_limit(0.3) #300mA
        if abs(current) > 0.29 and abs(current) <= 0.3:
                smu_A.set_current_range(0.4)  #400mA
                smu_A.set_current_limit(0.4) #400mA
        if abs(current) > 0.39 and abs(current) <= 0.4:
                smu_A.set_current_range(0.7)  #700mA
                smu_A.set_current_limit(0.7) #700mA
        current_pd_a = smu_B.measure_current()
        #time.sleep(delay_time)
        #smu_A.set_voltage(0)
        data_voltage.append(voltage)
        data_current.append(current * 1000)
        data_current_pd.append(current_pd_a * 1000)
        print('Voltage: '+str(voltage)+'V; Current:'+str(current * 1000)+'mA; Current_PD: '+str(current_pd_a*1000)+'mA')

time_finish = time.time()
#time = time_start-time_finish
print('time: '+str(time_finish-time_start)+' sec.')
# Write the data in a csv
f = open(filename_csv, 'a')
for i in range(steps):
        f.write(str(data_voltage[i])) #Voltage (V)
        f.write(',')
        f.write(str(data_current[i])) #Current (mA)
        f.write(',')
        f.write(str(data_current_pd[i])) #Current PD (mA)
        f.write('\n')
f.close()

# disable the output
smu_A.disable_output()
smu_B.disable_output()

# properly disconnect from the device
sm.disconnect()

""" ******* Plot the Data we obtained ******** """
fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Voltage (V)')
ax1.set_ylabel('Current (mA)', color = color)
ax1.plot(data_voltage, data_current, color = color)
ax1.tick_params(axis='y', labelcolor = color)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Current_PD (mA)', color = color)
ax2.plot(data_voltage, data_current_pd, color = color)
ax2.tick_params(axis = 'y', labelcolor = color)
plt.savefig(filename_pdf)
plt.show()

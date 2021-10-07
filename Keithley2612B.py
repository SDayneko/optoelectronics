"""
Library to access the basic functionality of the Keithley SourceMeter 2612B by using pyvisa for communication.
last modified: 2021-10-04
"""
import pyvisa
class _SMUChannel:
    # variables to store the ranges that have been selected
    # we need this information to check if the limit value is valid
    __current_range = 0
    __voltage_range = 0
    def __init__(self, smu_object, smu_channel):
        """
        Implements the functionality for one individual channel of the SMU.
        Args:
            smu_object (SMU2612B): the SMU the channel belongs to
            smu_channel: the channel you want to connect to
        Returns:
            an "channel" object that has methods to control the channel
        """
        # store the parameters in variables that can be accessed from other methods
        self.__smu = smu_object
        self.__channel = smu_channel
    """
    #####################################################################################
    commands for setting the mode / ranges / limits / levels
    #####################################################################################
    """
    def identify(self):
        """
        returns a string with model and channel identification
        """
        model = self.__smu.identify_model()
        if self.__channel is SMU2612B.CHANNEL_A:
            channel = "Channel A"
        else:
            channel = "Channel B"
        identification_string = str(model) + " " + str(channel)
        return identification_string
    def reset(self):
        """
        Resets the channel to the default setting of the SMU.
        """
        self.__smu._reset(self.__channel)
    def set_mode_voltage_source(self):
        """
        Sets the channel into voltage source mode.
        In this mode you set the voltage and can measure current.
        """
        self.__smu._set_mode(self.__channel, SMU2612B.VOLTAGE_MODE)
    def set_mode_current_source(self):
        """
        Sets the channel into current source mode.
        In this mode you set the current and can measure voltage.
        """
        self.__smu._set_mode(self.__channel, SMU2612B.CURRENT_MODE)
    def enable_voltage_autorange(self):
        """
        Enables the autorange feature for the voltage source and measurement
        """
        self.__smu._set_autorange(self.__channel, SMU2612B.UNIT_VOLTAGE, SMU2612B.STATE_ON)
    def disable_voltage_autorange(self):
        """
        Disables the autorange feature for the voltage source and measurement
        """
        self.__smu._set_autorange(self.__channel, SMU2612B.UNIT_VOLTAGE, SMU2612B.STATE_OFF)
    def enable_current_autorange(self):
        """
        Enables the autorange feature for the current source and measurement
        """
        self.__smu._set_autorange(self.__channel, SMU2612B.UNIT_CURRENT, SMU2612B.STATE_ON)
    def disable_current_autorange(self):
        """
        Disables the autorange feature for the current source and measurement
        """
        self.__smu._set_autorange(self.__channel, SMU2612B.UNIT_CURRENT, SMU2612B.STATE_OFF)
    def set_voltage_range(self, value):
        """
        Sets the range for the voltage.
        Args:
            value: set to the maximum expected voltage be sourced or measured
        Examples:
            to set the voltage range to 1 V use:
            >>> self.set_voltage_range(1)
        Note:
            The range is applied to the source function as well as the measurement function.
        """
        # store the requested voltage range; we check it when the limit is set
        self.__voltage_range = value
        self.__smu._set_range(self.__channel, SMU2612B.UNIT_VOLTAGE, value)
    def set_current_range(self, value):
        """
        Sets the range for the current.
        Args:
            value: set to the maximum expected current be sourced or measured
        Examples:
            to set the current range to 10 mA use:
            >>> self.set_voltage_range(0.01)
            also to set the current range to 1 µA use:
            >>> self.set_voltage_range(1e-6)
        Note:
            The range is applied to the source function as well as the measurement function.
        """
        # store the requested current range; we check it when the limit is set
        self.__current_range = value
        self.__smu._set_range(self.__channel, SMU2612B.UNIT_CURRENT, value)
    def set_voltage_limit(self, value):
        """
        Limits the voltage output of the current source.
        Args:
            value: set to the maximum allowed voltage.
        Examples:
            to set the limit to 10 V
            >>> self.set_voltage_limit(10)
        Note:
            If you are in voltage source mode the voltage limit has no effect.
        Raises:
            ValueError: If `value` is bigger then the selected voltage range.
        """
        # check if the limit is within the range
        if value <= self.__voltage_range:
            self.__smu._set_limit(self.__channel, SMU2612B.UNIT_VOLTAGE, value)
        else:
            raise ValueError("The limit is not within the range. Please set the range first")
    def set_current_limit(self, value):
        """
        Limits the current output of the voltage source.
        Args:
            value: set to the maximum allowed current.
        Examples:
            to set the limit to 10 mA (both of the lines below do the same)
            >>> self.set_current_limit(0.01)
            >>> self.set_current_limit(1e-2)
        Note:
            If you are in current source mode the current limit has no effect.
        Raises:
            ValueError: If `value` is bigger then the selected current range.
        """
        # check if the limit is within the range
        if value <= self.__current_range:
            self.__smu._set_limit(self.__channel, SMU2612B.UNIT_CURRENT, value)
        else:
            raise ValueError("The limit is not within the range. Please set the range first")
    def set_voltage(self, value):
        """
        Sets the output level of the voltage source.
        Args:
            value: source voltage level.
        Examples:
            to set the output level to 100 mV
            >>> self.set_voltage(0.1)
        Note:
           If the source is configured as a voltage source and the output is on,
           the new setting is sourced immediately.
           The sign of `level` dictates the polarity of the source.
           Positive values generate positive voltage from the high terminal of the source relative to the low terminal.
           Negative values generate negative voltage from the high terminal of the source relative to the low terminal.
        """
        self.__smu._set_level(self.__channel, SMU2612B.UNIT_VOLTAGE, value)
    def set_current(self, value):
        """
        Sets the output level of the current source.
        Args:
            value: source current level.
        Examples:
            to set the output level to 100 µA
            >>> self.set_current(1e-4)
        Note:
           If the source is configured as a current source and the output is on, the new setting is sourced immediately.
           The sign of `level` dictates the polarity of the source.
           Positive values generate positive current from the high terminal of the source relative to the low terminal.
           Negative values generate negative current from the high terminal of the source relative to the low terminal.
        """
        self.__smu._set_level(self.__channel, SMU2612B.UNIT_CURRENT, value)
    def enable_output(self):
        """
        Sets the source output state to on.
        Examples:
            to enable the output
            >>> self.enable_output()
        Note:
           When the output is switched on, the SMU sources either voltage or current, as set by
           set_mode_voltage_source() or set_mode_current_source()
        """
        self.__smu._set_output_state(self.__channel, SMU2612B.STATE_ON)
    def disable_output(self):
        """
        Sets the source output state to off.
        Examples:
            to disable the output
            >>> self.disable_output()
        Note:
           When the output is switched off, the SMU goes in to low Z mode (meaning: the output is shorted).
           Be careful when using the SMU for measurement of high power devices. The disabling of the output could lead
           high current flow.
        """
        self.__smu._set_output_state(self.__channel, SMU2612B.STATE_OFF)
    """
    #####################################################################################
    commands for setting what measurement will be shown at the display of the SMU channel
    #####################################################################################
    """
    def display_voltage(self):
        """
        The voltage measurement will be displayed on the SMU.
        """
        self.__smu._set_display(self.__channel, SMU2612B.DISPLAY_VOLTAGE)
    def display_current(self):
        """
        The current measurement will be displayed on the SMU.
        """
        self.__smu._set_display(self.__channel, SMU2612B.DISPLAY_CURRENT)
    def display_resistance(self):
        """
        The calculated resistance will be displayed on the SMU.
        """
        self.__smu._set_display(self.__channel, SMU2612B.DISPLAY_RESISTANCE)
    def display_power(self):
        """
        The calculated power will be displayed on the SMU.
        """
        self.__smu._set_display(self.__channel, SMU2612B.DISPLAY_POWER)
    """
    #####################################################################################
    commands for setting the sense mode (2-wire or 4-wire)
    #####################################################################################
    """
    def set_sense_2wire(self):
        """
        Setting the the sense mode to local (2-wire)
        Notes:
            Corresponding LUA command (SMU 2600B reference manual page 2-77)
            smuX.sense = smuX.SENSE_LOCAL
        """
        self.__smu._set_sense_mode(self.__channel, SMU2612B.SENSE_MODE_2_WIRE)
    def set_sense_4wire(self):
        """
        Setting the the sense mode to local (4-wire)
        Notes:
            Corresponding LUA command (SMU 2600B reference manual page 2-77)
            smuX.sense = smuX.SENSE_REMOTE
        """
        self.__smu._set_sense_mode(self.__channel, SMU2612B.SENSE_MODE_4_WIRE)
    """
    #####################################################################################
    commands for setting the measurement speed / accuracy
    #####################################################################################
    """
    def set_measurement_speed_fast(self):
        """
        This attribute controls the integration aperture for the analog-to-digital converter (ADC).
        fast corresponds to 0.01 PLC (Power Line Cycles) -> approx. 5000 measurements per second
        Results in: fast performance, but accuracy is reduced
        """
        self.__smu._set_measurement_speed(self.__channel, SMU2612B.SPEED_FAST)
    def set_measurement_speed_med(self):
        """
        This attribute controls the integration aperture for the analog-to-digital converter (ADC).
        fast corresponds to 0.1 PLC (Power Line Cycles) -> approx. 500 measurements per second
        Results in: speed and accuracy are balanced
        """
        self.__smu._set_measurement_speed(self.__channel, SMU2612B.SPEED_MED)
    def set_measurement_speed_normal(self):
        """
        This attribute controls the integration aperture for the analog-to-digital converter (ADC).
        fast corresponds to 1 PLC (Power Line Cycles) -> approx. 50 measurements per second
        Results in: speed and accuracy are balanced
        """
        self.__smu._set_measurement_speed(self.__channel, SMU2612B.SPEED_NORMAL)
    def set_measurement_speed_hi_accuracy(self):
        """
        This attribute controls the integration aperture for the analog-to-digital converter (ADC).
        fast corresponds to 10 PLC (Power Line Cycles) -> approx. 5 measurements per second
        Results in: high accuracy, but speed is reduced
        """
        self.__smu._set_measurement_speed(self.__channel, SMU2612B.SPEED_HI_ACCURACY)
    """
    #####################################################################################
    commands for reading values
    #####################################################################################
    """
    def measure_voltage(self):
        """
        Causes the SMU to trigger a voltage measurement and return a single reading.
        Returns:
            float: the value of the reading in volt
        """
        return self.__smu._measure(self.__channel, SMU2612B.UNIT_VOLTAGE)
    def measure_current(self):
        """
        Causes the SMU to trigger a current measurement and return a single reading.
        Returns:
            float: the value of the reading in ampere
        """
        return self.__smu._measure(self.__channel, SMU2612B.UNIT_CURRENT)
    def measure_resistance(self):
        """
        Causes the SMU to trigger a resistance measurement and return a single reading.
        Retu of the reading in ohm
        """
        return self.__smu._measure(self.__channel, SMU2612B.UNIT_RESISTANCE)
    def measure_power(self):
        """
        Causes the SMU to trigger a power measurement and return a single reading.
        Returns:
            float: the value of the reading in watt
        """
        return self.__smu._measure(self.__channel, SMU2612B.UNIT_POWER)
    def measure_current_and_voltage(self):
        """
        Causes the SMU to trigger a voltage and current measurement simultaneously.
        Use this function if you need exact time correlation between voltage and current.
        Examples:
            measure current and voltage simultaneously
            >>> [current, voltage] = self.measure_current_and_voltage()
        Returns:
            list: a list of the two measured values.
                current as the first list element
                voltage as the second list element
        """
        return self.__smu._measure(self.__channel, SMU2612B.UNIT_CURRENT_VOLTAGE)
    def measure_voltage_sweep(self, start_value, stop_value, settling_time, points):
        """
        Causes the SMU to make a voltage sweep based on a staircase profile.
        Args:
            start_value: the voltage level from which the sweep will start.
            stop_value: the voltage level at which the sweep will stop.
            settling_time: the time the unit will wait after a voltage step is reached before a measurement
                is triggered. If set to 0 the measurement will be done as fast as possible.
            points: the number of steps.
        Note:
           If you want to measure really fast be sure that you have set the measurement speed accordingly
        Examples:
            perform a voltage sweep from 0 V to 5 V with 500 steps (so 10 mV step size) as fast as possible
            >>> self.set_measurement_speed_fast()
            >>> [current_list, voltage_list] = self.measure_voltage_sweep(0, 5, 0, 500)
        Returns:
            list: the returning list contains itself two lists
                first element is a list of the measured current values
                second element is a list of the voltage source values (not the actual measured voltage)
        """
        return self.__smu._measure_linear_sweep(self.__channel, SMU2612B.UNIT_VOLTAGE,
                                                start_value, stop_value, settling_time, points)
    def measure_current_sweep(self, start_value, stop_value, settling_time, points):
        """
        Causes the SMU to make a current sweep based on a staircase profile.
        Args:
            start_value: the current level from which the sweep will start.
            stop_value: the current level at which the sweep will stop.
            settling_time: the time the unit will wait after a current step is reached before a measurement
                is triggered. If set to 0 the measurement will be done as fast as possible.
            points: the number of steps.
        Note:
           If you want to measure really fast be sure that you have set the measurement speed accordingly
        Examples:
            perform a current sweep from 1 mA to 100 mA with 1000 steps (so 0.1 mA step size)
            and let the device under test 1 second time to settle before taking a measurement
            >>> self.set_measurement_speed_normal()
            >>> [current_list, voltage_list] = self.measure_voltage_sweep(1e-3, 0.1, 1, 1000)
        Returns:
            list: the returning list contains itself two lists
                first element is a list of the current source values (not the actual measured current)
                second element is a list of the measured voltage
        """
        return self.__smu._measure_linear_sweep(self.__channel, SMU2612B.UNIT_CURRENT,
                                                start_value, stop_value, settling_time, points)
class SMU2612B:
    # define strings that are used in the LUA commands
    CHANNEL_A = "a"
    CHANNEL_B = "b"
    # defines an arbitrary word; when used the program tries to access all available channels
    CHANNEL_ALL = "all"
    CURRENT_MODE = "DCAMPS"
    VOLTAGE_MODE = "DCVOLTS"
    DISPLAY_VOLTAGE = 'DCVOLTS'
    DISPLAY_CURRENT = 'DCAMPS'
    DISPLAY_RESISTANCE = 'OHMS'
    DISPLAY_POWER = 'WATTS'
    SENSE_MODE_2_WIRE = 'SENSE_LOCAL'
    SENSE_MODE_4_WIRE = 'SENSE_REMOTE'
    UNIT_VOLTAGE = "v"
    UNIT_CURRENT = "i"
    UNIT_CURRENT_VOLTAGE = "iv"
    UNIT_POWER = "p"
    UNIT_RESISTANCE = "r"
    STATE_ON = "ON"
    STATE_OFF = "OFF"
    SPEED_FAST = 0.01
    SPEED_MED = 0.1
    SPEED_NORMAL = 1
    SPEED_HI_ACCURACY = 10
    # maximum amount of values that can be read from the Keithley buffer without an error from the
    # pyvisa interface. We set it to 1000 values.
    __PYVISA_MAX_BUFFER_REQUEST = 1000
    def __init__(self, visa_resource_name, timeout=1000):
        """
        Implements the global (channel independent) functionality for the Keithley SMU 2600 series.
        The communication is made through NI-VISA (you need to have this installed)
        Args:
            visa_resource_name: use exactly the VISA-resource-name you see in your NI-MAX
        Returns:
            pyvisa.ResourceManager.open_resource: Object to control the SMU
        """
        # Variables to store the capabilities of the instrument
        self.__voltage_ranges = None
        self.__current_ranges = None
        self.__channel_b_present = None
        # variable to store if the debug output was enabled
        self.__debug = False
        # open the resource manager
        __rm = pyvisa.ResourceManager()
        # Connect to the device
        self.__instrument = __rm.open_resource(visa_resource_name)
        self.__connected = True
        # set the timeout
        self.__instrument.timeout = timeout
        # clear the error queue
        self.__clear_error_queue()
        # clear everything that may is in the buffer
        self.__instrument.clear()
        # find out the ranges of the device and set the limits
        model = self.identify_model()
        self.set_model_limits(model)
    def disconnect(self):
        """
        Disconnect the instrument. After this no further communication is possible.
        """
        if self.__connected:
            self.__instrument.close()
            self.__connected = False
    def get_channel(self, channel):
        """
        Gives you an object with which you can control the individual parameters of a channel.
        Args:
            channel: the channel you want to connect to.
                Use the keywords SMU2612B.CHANNEL_A or SMU2612B.CHANNEL_B
        Returns:
            _SMUChannel: an "channel" object that has methods to control the channel
        Raises:
            ValueError: If the channel is not available.
        """
        # check if the channel b is available. We don't have to check channel a because every smu has one
        if channel is SMU2612B.CHANNEL_B and not self.__channel_b_present:
            raise ValueError("No channel B on this model")
        return _SMUChannel(self, channel)
    def enable_debug_output(self):
        """
        Enables the debug output of all communication to the SMU.
        The messages will be printed on the console.
        """
        self.__debug = True
    def disable_debug_output(self):
        """
        Disables the debug output. Nothing will be printed to the console that you haven't specified yourself.
        """
        self.__debug = False
    """
    #####################################################################################
    commands for communicating with the instrument via the pyvisa interface
    #####################################################################################
    """
    def __clear_error_queue(self):
        """
        internal function to clear the error queue of the SMU
        """
        self.write_lua("errorqueue.clear()")
    def __check_error_queue(self):
        """
        requests the error queue from the SMU. If there is an error this function will raise an
        value error containing the message from the SMU.

        Raises:
            ValueError: If there is an error stored at the SMU
        """
        # check if there was an error
        cmd = "errorcode, message = errorqueue.next()\nprint(errorcode, message)"
        response = self.__instrument.query(str(cmd))
        if self.__debug:
            print('Error msg: ' + str(response))
        try:
            [code, message] = response.split('\t', 1)
            if float(code) != 0:
                # if we have an error code something happened and we should raise an error
                raise ValueError('The SMU said: "' + str(message) + '"  /  Keithley-Error-Code: ' + str(code))
        except:
            raise ValueError('The SMU said: "' + str(response))
    def write_lua(self, cmd, check_for_errors=True):
        """
        Writes a command to the pyvisa connection. It expects no return message from the SMU
        Args:
            cmd: the TSP command for the SMU
            check_for_errors: by default the error queue of the SMU is checked after every command that is send to the
                SMU. In some cases the SMU will not respond to this check and a pyvisa timeout would occur. In such
                a case you can disable this check.
        """
        if self.__debug:
            print('Write cmd: ' + str(cmd))
        self.__instrument.write(str(cmd))
        # check if the command executed without any errors
        if check_for_errors:
            self.__check_error_queue()
    def query_lua(self, cmd, check_for_errors=True):
        """
        Queries something from the SMU with TSP syntax.
        basically we just write a TSP command and expect some kind of response from the SMU
        Args:
            cmd: the TSP command for the SMU
            check_for_errors: by default the error queue of the SMU is checked after every command that is send to the
                SMU. In some cases the SMU will not respond to this check and a pyvisa timeout would occur. In such
                a case you can disable this check.
        """
        if self.__debug:
            print('Query cmd: ' + str(cmd))
        # send the request to the device
        reading = self.__instrument.query(str(cmd)).rstrip('\r\n')
        if self.__debug:
            print('Query answer: ' + str(reading))
        # check if the command executed without any errors
        if check_for_errors:
            self.__check_error_queue()
        return reading
    """
    #####################################################################################
    commands that gather information of the device and set parameter
    #####################################################################################
    """
    def identify_model(self):
        """
        Returns the model number of the SMU. Based on this string the model limits are set.
        Returns:
            str: the model number of the SMU
        """
        return self.query_lua('print(localnode.model)')
    def set_model_limits(self, model_number):
        """
        This function is used to set the model specific differences. This method is called at the initialisation
        process. There is usually no need for you to call this method.
        Args:
            model_number (str): the model number of the SMU.
        """
        if self.__debug:
            print("Model " + str(model_number) + " detected. Setting ranges ...")
        if "2612B" in model_number:
            self.__voltage_ranges = [0.2, 2, 20, 200]
            self.__current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
            self.__channel_b_present = True
        else:
            raise ValueError("unknown model number")
    def get_available_voltage_ranges(self):
        """
        Returns a list containing the available voltage ranges based on the model limits.
        Returns:
            list: containing the available voltage ranges
        """
        return self.__voltage_ranges
    def get_available_current_ranges(self):
        """
        Returns a list containing the available current ranges based on the model limits.
        Returns:
            list: containing the available current ranges
        """
        return self.__current_ranges
    """
    #####################################################################################
    commands for measuring values from the two channels simultaneously
    #####################################################################################
    """
    def measure_voltage(self):
        """
        Causes the SMU to trigger a voltage measurement and return a single reading for both channels (if available).
        Use this function if you need exact time correlation between the voltage of the two channels.
        Examples:
            measure voltage simultaneously on both channels
            >>> [v_chan_a, v_chan_b] = self.measure_voltage()
        Returns:
            list: a list of floats containing the two measured values.
                voltage measurement of channel a as the first list element
                voltage measurement of channel b as the second list element
        Raises:
            ValueError: If the SMU has just one channel
        """
        return self._measure(SMU2612B.CHANNEL_ALL, SMU2612B.UNIT_VOLTAGE)
    def measure_current(self):
        """
        Causes the SMU to trigger a current measurement and return a single reading for both channels (if available).
        Use this function if you need exact time correlation between the current of the two channels.
        Examples:
            measure current simultaneously on both channels
            >>> [i_chan_a, i_chan_b] = self.measure_current()
        Returns:
            list: a list of floats containing the two measured values.
                current measurement of channel a as the first list element
                current measurement of channel b as the second list element
        Raises:
            ValueError: If the SMU has just one channel
        """
        return self._measure(SMU2612B.CHANNEL_ALL, SMU2612B.UNIT_CURRENT)
    def measure_resistance(self):
        """
        Causes the SMU to trigger a resistance measurement and return a single reading for both channels (if available).
        Use this function if you need exact time correlation between the resistance of the two channels.
        Examples:
            measure resistance simultaneously on both channels
            >>> [r_chan_a, r_chan_b] = self.measure_resistance()
        Returns:
            list: a list of floats containing the two measured values.
                resistance measurement of channel a as the first list element
                resistance measurement of channel b as the second list element
        Raises:
            ValueError: If the SMU has just one channel
        """
        return self._measure(SMU2612B.CHANNEL_ALL, SMU2612B.UNIT_RESISTANCE)
    def measure_power(self):
        """
        Causes the SMU to trigger a power measurement and return a single reading for both channels (if available).
        Use this function if you need exact time correlation between the power of the two channels.
        Examples:
            measure power simultaneously on both channels
            >>> [p_chan_a, p_chan_b] = self.measure_power()
        Returns:
            list: a list of floats containing the two measured values.
                power of channel a as the first list element
                power of channel b as the second list element
        Raises:
            ValueError: If the SMU has just one channel
        """
        return self._measure(SMU2612B.CHANNEL_ALL, SMU2612B.UNIT_POWER)
    def measure_current_and_voltage(self):
        """
        Causes the SMU to trigger a voltage and current measurement simultaneously for both channels (if available).
        Use this function if you need exact time correlation between voltage and current of the two channels.
        Examples:
            measure current and voltage simultaneously on both channels
            >>> [i_chan_a, v_chan_a, i_chan_b, v_chan_b] = self.measure_current_and_voltage()
        Returns:
            list: a list of floats containing the four measured values.
                current of channel a as the first list element
                voltage of channel a as the second list element
                current of channel b as the third list element
                voltage of channel b as the fourth list element
        Raises:
            ValueError: If the SMU has just one channel
        """
        return self._measure(SMU2612B.CHANNEL_ALL, SMU2612B.UNIT_CURRENT_VOLTAGE)
    """
    #####################################################################################
    commands for setting the parameters of channels
    those should not be accessed directly but through the channel class
    #####################################################################################
    """
    def _reset(self, channel):
        """restore the default settings"""
        cmd = 'smu' + str(channel) + '.reset()'
        self.write_lua(cmd)
    def _set_display(self, channel, function):
        """defines what measurement will be shown on the display"""
        cmd = 'display.smu' + str(channel) + '.measure.func = display.MEASURE_' + str(function)
        self.write_lua(cmd)
    def _set_measurement_speed(self, channel, speed):
        """defines how many PLC (Power Line Cycles) a measurement takes"""
        cmd = 'smu' + str(channel) + '.measure.nplc = ' + str(speed)
        self.write_lua(cmd)
    def _set_mode(self, channel, mode):
        cmd = 'smu' + str(channel) + '.source.func = ' + 'smu' + str(channel) + '.OUTPUT_' + str(mode)
        self.write_lua(cmd)
    def _set_sense_mode(self, channel, mode):
        """
        set 2-wire or 4-wire sense mode
        Manual page 2-77
        Notes:
            LUA commands look like this
            smua.sense = smua.SENSE_REMOTE
            smua.sense = smua.SENSE_LOCAL
        """
        cmd = 'smu' + str(channel) + '.sense = ' + 'smu' + str(channel) + '.' + str(mode)
        self.write_lua(cmd)
    def _set_autorange(self, channel, unit, state):
        """enables or disables the autorange feature"""
        # set the source range
        cmd = 'smu' + str(channel) + '.source.autorange' + str(unit) \
              + ' = smu' + str(channel) + '.AUTORANGE_' + str(state)
        self.write_lua(cmd)
        # set the measurement range
        cmd = 'smu' + str(channel) + '.measure.autorange' + str(unit) \
              + ' = smu' + str(channel) + '.AUTORANGE_' + str(state)
        self.write_lua(cmd)
    def _set_range(self, channel, unit, range_value):
        """Set the range to the given value (or to the next suitable range)"""
        range_found = 0
        # select the range you want to compare to based on the given type
        if unit is self.UNIT_CURRENT:
            range_to_check = self.__current_ranges
        elif unit is self.UNIT_VOLTAGE:
            range_to_check = self.__voltage_ranges
        else:
            raise ValueError('Type "' + str(unit) + '" is valid in range setting')
        # find the range that fits the desired value best
        if range_value in range_to_check:
            range_found = range_value
        else:
            # if there is no exact match use the range that is best suitable
            for v in sorted(range_to_check):
                if v > range_value:
                    range_found = v
                    break
            # if none of the ranges above work ... raise an error
            if not range_found:
                raise ValueError("no suitable range found")
        # set the source range
        cmd = 'smu' + str(channel) + '.source.range' + str(unit) + ' = ' + str(range_found)
        self.write_lua(cmd)
        # set the measurement range
        cmd = 'smu' + str(channel) + '.measure.range' + str(unit) + ' = ' + str(range_found)
        self.write_lua(cmd)
    def _set_limit(self, channel, unit, value):
        """command used to set the limits for voltage, current or power"""
        # send the command to the SourceMeter
        cmd = 'smu' + str(channel) + '.source.limit' + str(unit) + ' = ' + str(value)
        self.write_lua(cmd)
    def _set_level(self, channel, unit, value):
        # send the command to the SourceMeter
        cmd = 'smu' + str(channel) + '.source.level' + str(unit) + ' = ' + str(value)
        self.write_lua(cmd)
    def _set_output_state(self, channel, state):
        cmd = 'smu' + str(channel) + '.source.output = smu' + str(channel) + '.OUTPUT_' + str(state)
        self.write_lua(cmd)
    """
    #####################################################################################
    commands for reading values from the channels
    those should not be accessed directly but through the channel class
    #####################################################################################
    """
    def _measure(self, channel, unit):
        """function for getting a single reading of the specified value"""
        # if CHANNEL_ALL is specified this has only an effect on two channel units
        if channel == SMU2612B.CHANNEL_ALL:
            # if channel b is present then modify the LUA command
            if self.__channel_b_present:
                # In case we want to measure voltage and current we get four return parameters
                # so the LUA command has to be different.
                if unit == SMU2612B.UNIT_CURRENT_VOLTAGE:
                    cmd = 'iChA, vChA = smua.measure.' + str(unit) + '()\n' \
                          + 'iChB, vChB = smub.measure.' + str(unit) + '()\n' \
                          + 'print(iChA, vChA, iChB, vChB)'
                else:
                    cmd = 'ChA = smua.measure.' + str(unit) + '()\n' \
                          + 'ChB = smub.measure.' + str(unit) + '()\n' \
                          + 'print(ChA, ChB)'
            else:
                raise ValueError("This device has only ONE channel. "
                                 "Use the measurement function of the channel instead.")
        else:
            cmd = 'print(smu' + str(channel) + '.measure.' + str(unit) + '())'
        reading = self.query_lua(cmd)
        reading = reading.replace("'", "")
        # if we get more than one value out then put it in a list
        out = []
        parts = reading.split("\t")
        if len(parts) > 1:
            for value in parts:
                out.append(float(value))
            return out
        else:
            return float(reading)
    def _measure_linear_sweep(self, channel, unit, start_value, stop_value, settling_time, points):
        """function to sweep voltage or current and measure current resp. voltage"""
        sweep_unit = measure_unit = ''
        if unit is self.UNIT_VOLTAGE:
            sweep_unit = 'V'
            measure_unit = 'I'
        elif unit is self.UNIT_CURRENT:
            sweep_unit = 'I'
            measure_unit = 'V'
        else:
            ValueError('Only possible to sweep Voltage or Current')
        # prepare the buffer
        cmd = 'smu' + str(channel) + '.nvbuffer1.clear()\n' \
              'smu' + str(channel) + '.nvbuffer1.appendmode = 1\n' \
              'smu' + str(channel) + '.nvbuffer1.collectsourcevalues = 1\n' \
              'smu' + str(channel) + '.measure.count = 1'
        self.write_lua(cmd)
        # construct the sweep command based on the given parameters
        # SweepILinMeasureV(smua, 1e-3, 10e-3, 0.1, 10)
        cmd = 'Sweep' + sweep_unit + 'LinMeasure' + measure_unit + '(smu' + str(channel) + ', ' \
              + str(start_value) + ', ' + str(stop_value) + ', ' + str(settling_time) + ', ' + str(points) + ')'
        self.write_lua(cmd, check_for_errors=False)
        # wait till the measurement is finished
        # we just try to read some values of the buffer. If we receive an answer we
        # know that the measurement is finished
        answer = None
        cmd = 'print("Are you alive?")'
        while answer is None:
            try:
                # query the values that are stored in the nvbuffer1
                answer = self.query_lua(cmd, check_for_errors=False)
            except pyvisa.VisaIOError:
                # no answer yet ... we just try again
                pass
        # clear any old readings that are in the buffer
        self.__instrument.clear()
        # determine in how many chunks we need to read the buffer and what the start and end values are
        quotient = points // self.__PYVISA_MAX_BUFFER_REQUEST
        remainder = points % self.__PYVISA_MAX_BUFFER_REQUEST
        # define the starting values for the buffer read
        buffer_start_values = []
        buffer_end_values = []
        for i in range(quotient):
            buffer_start_values.append(i * self.__PYVISA_MAX_BUFFER_REQUEST + 1)
            buffer_end_values.append((i+1) * self.__PYVISA_MAX_BUFFER_REQUEST)
        # the last value needs to be set to the amount of data points we have
        if remainder != 0:
            buffer_start_values.append(quotient * self.__PYVISA_MAX_BUFFER_REQUEST + 1)
            buffer_end_values.append(quotient * self.__PYVISA_MAX_BUFFER_REQUEST + remainder)
        # put the readings of the measured data in a list
        measure_values = []
        # read in the buffer and combine the output
        for count in range(len(buffer_start_values)):
            cmd = 'printbuffer(' + str(buffer_start_values[count]) + ', ' + str(buffer_end_values[count]) \
                  + ', smu' + str(channel) + '.nvbuffer1.readings)'
            answer = self.query_lua(cmd, check_for_errors=False)
            parts = answer.split(",")
            for value in parts:
                measure_values.append(float(value))
                # clear the visa input buffer
            self.__instrument.clear()
        # put the readings of the source values in a list
        source_values = []
        # read in the buffer and combine the output
        for count in range(len(buffer_start_values)):
            cmd = 'printbuffer(' + str(buffer_start_values[count]) + ', ' + str(buffer_end_values[count]) \
                  + ', smu' + str(channel) + '.nvbuffer1.sourcevalues)'
            answer = self.query_lua(cmd, check_for_errors=False)
            parts = answer.split(",")
            for value in parts:
                source_values.append(float(value))
                # clear the visa input buffer
            self.__instrument.clear()
        # always return the current as first parameter
        if unit is self.UNIT_VOLTAGE:
            return [measure_values, source_values]
        else:
            return [source_values, measure_values]


from .thermometer import Thermometer


class DS18B20(Thermometer):
    """
    DS18B20 1 wire abstraction class

    This class extends Thermometer.

    Parameters
    ----------
    owserver : pyownet.protocol._Proxy :
        The proxy object used to access the owserver

    path : str :
        The owfs path for the Thermometer

    uncached : bool:
        (Default value = False)
        If True forces owserver to query the 1wire bus on each property access.

    lower_precision : int, optional:
        The lower precision allowed for temperature readings.

    upper_precision : int, optional:
        The upper precision allowed for temperature readings.
    """
    def __init__(self, owserver, path, uncached=True):
        super().__init__(owserver, path, uncached=uncached)
        self.lower_precision = 9
        self.upper_precision = 12

    def __repr__(self):
        super_repr = super().__repr__().replace(')>', ', ')
        return (f'{super_repr}'
                f'power={self.power}, '
                f'temperature9={self.temperature9}, '
                f'temperature10={self.temperature10}, '
                f'temperature11={self.temperature11}, '
                f'temperature12={self.temperature12}, '
                f'fasttemp={self.fasttemp}, '
                f'temphigh={self.temphigh}, '
                f'templow={self.templow}'
                f')>')

    def _temperature_with_precision(self, precision: int) -> float:
        """
        Reads the device temperature with the specified precision.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.

        Parameters
        ----------
        precision : int :
            An integer between self.lower_precision and self.upper_precision.

        Returns
        -------
        float :
            The temperature reading at the specified precision.

        Raises
        ------
        PrecisionNotSetError
            Reaise when one of the self.lower_precision or the
            self.upper_precision properties is set to None.

        IncorrectPrecisionError
            Raises if the precision is lower than self.lower_precision or
            higher than self.upper_precision.
        """
        return float(self._read(f'temperature{precision}'))

    @property
    def power(self) -> bool:
        """
        bool: Read-only. Is the chip powered externally?

        True if it is powered externally. False if it is powered parasitically
        from the data bus.
        """
        self.logger.info(
            f'Trying to read power status for device: {self.query_path}')
        return bool(self._read('power'))

    @property
    def temperature9(self) -> float:
        """
        float. Read-only. Measured temperature. 9 bit resolution.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.
        """
        return self._temperature_with_precision(9)

    @property
    def temperature10(self) -> float:
        """
        float: Read-only. Measured temperature. 10 bit resolution.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.
        """
        return self._temperature_with_precision(10)

    @property
    def temperature11(self) -> float:
        """
        float: Read-only. Measured temperature. 11 bit resolution.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.
        """
        return self._temperature_with_precision(11)

    @property
    def temperature12(self) -> float:
        """
        float: Read-only. Measured temperature. 12 bit resolution.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.
        """
        return self._temperature_with_precision(12)

    @property
    def fasttemp(self) -> float:
        """
        float: Read-only. Measured temperature. Equivalent to temperature9.

        There is a tradeoff of time versus accuracy in the temperature
        measurement.
        """
        return float(self._read('fasttemp'))

    @property
    def temphigh(self) -> int:
        """
        int: Get or set the lower limit for the high temperature alarm state.
        """
        return int(float(self._read('temphigh')))

    @temphigh.setter
    def temphigh(self, value: int) -> None:
        self._write('temphigh', str(value).encode('ascii'))

    @property
    def templow(self) -> int:
        """
        int: Get or set the higher limit for the low temperature alarm state.
        """
        return int(float(self._read('templow')))

    @templow.setter
    def templow(self, value: int) -> None:
        self._write('templow', str(value).encode('ascii'))

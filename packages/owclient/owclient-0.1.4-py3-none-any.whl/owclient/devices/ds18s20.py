from .thermometer import Thermometer


class DS18S20(Thermometer):
    """
    High-Precision 1-Wire Digital Thermometer

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
    """
    def __repr__(self):
        super_repr = super().__repr__().replace(')>', ',')
        return (f'{super_repr} temphigh={self.temphigh}, '
                f'templow={self.templow})>')

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


class DS1920(DS18S20):
    """
    iButton version of the DS18S20 thermometer
    """
    pass

import logging

import pyownet

from owclient.exc import CouldNotReadError
from owclient.exc import CouldNotWriteError


class Device:
    """
    1wire device base class

    This class publishes the basic 1 wire device read only files as properties.

    Parameters
    ----------
    owserver : pyownet.protocol._Proxy:
        The pyownet Proxy used to send commands to owserver.

    path : str:
        The path to acces the device.

    uncached : bool, optional:
        (Default value = False)
        If True forces owserver to query the 1wire bus on each property access.
    """
    def __init__(self,
                 owserver: pyownet.protocol._Proxy,
                 path: str,
                 uncached: bool = True) -> None:
        self._owserver = owserver
        self.uncached = uncached
        self.path = path
        self.logger = logging.getLogger(f'{__name__}.{type(self).__name__}')

    def __repr__(self) -> str:
        return (f'<{type(self).__name__}('
                f'path={self.path}, '
                f'query_path={self.query_path}, '
                f'uncached={self.uncached}, '
                f'address={self.address}, '
                f'r_address={self.r_address}, '
                f'crc8={self.crc8}, '
                f'family={self.family}, '
                f'id={self.id}, '
                f'r_id={self.r_id}, '
                f'locator={self.locator}, '
                f'r_locator={self.r_locator}'
                f')>')

    def _read(self, property: str) -> bytes:
        """
        Read a property value from a 1 wire bus device.

        Parameters
        ----------
        property : str :
            The property you want to read.

        Return
        ------
        bytes :
            The reading value.
        """
        self.logger.debug(
            f'Trying to read {property} from device: {self.query_path}')
        try:
            return self._owserver.read(f'{self.query_path}{property}')
        except pyownet.protocol.Error as ex:
            msg = f'Could not read {property} from device {self.query_path}'
            self.logger.exception(msg)
            raise CouldNotReadError(msg) from ex

    def _write(self, property: str, value: bytes) -> None:
        """
        Write a property value to a 1 wire bus device.

        Parameters
        ----------
        property : str :
            The property you want to write.

        value : bytes :
            The bytes representation for the value you want to write.
        """
        self.logger.debug(
            f'Trying to write {property} to device: {self.query_path}')
        try:
            self._owserver.write(f'{self.query_path}{property}', value)
        except pyownet.protocol.Error as ex:
            msg = f'Could not write {property} to device {self.query_path}'
            self.logger.exception(msg)
            raise CouldNotWriteError(msg) from ex

    @property
    def query_path(self) -> str:
        """
        Read-only. The path the instance will use to access the device.
        """
        if self.uncached:
            return 'uncached' + self.path
        else:
            return self.path

    @property
    def address(self) -> str:
        """
        Read-only. The entire 64-bit unique ID.

        Given as upper case hexidecimal digits (0-9A-F).
        Address starts with the family code
        """

        return self._read('address').decode('ascii')

    @property
    def r_address(self) -> str:
        """
        Read-only. The entire 64-bit unique ID. (reversed).

        Given as upper case hexidecimal digits (0-9A-F).
        Address starts withthe family code
        """
        return self._read('r_address').decode('ascii')

    @property
    def crc8(self) -> str:
        """
        Read-only. The 8-bit error correction portion.

        Uses cyclic redundancy check. Computed from the preceding 56 bits of
        the unique ID number. Given as upper case hexidecimal digits (0-9A-F).
        """
        return self._read('crc8').decode('ascii')

    @property
    def family(self) -> str:
        """
        Read-only. The 8-bit family code.

        Unique to each type of device. Given as upper case hexidecimal digits
        (0-9A-F).
        """
        return self._read('family').decode('ascii')

    @property
    def id(self) -> str:
        """
        Read-only. The 48-bit middle portion of the unique ID number.

        Does not include the family code or CRC.
        Given as upper case hexidecimal digits (0-9A-F).
        """
        return self._read('id').decode('ascii')

    @property
    def r_id(self) -> str:
        """
        Read-only. The 48-bit middle portion of the ID number (reversed).

        Does not include the family code or CRC.
        Given as upper case hexidecimal digits (0-9A-F).
        """
        return self._read('r_id').decode('ascii')

    @property
    def locator(self) -> str:
        """
        Read-only. Associated connections with a unique 1-wire code.

        Uses an extension of the 1-wire design from iButtonLink company that
        associated 1-wire physical connections with a unique 1-wire code.
        If the connection is behind a Link Locator the locator will show a
        unique 8-byte number (16 character hexidecimal) starting with family
        code FE.

        If no Link Locator is between the device and the master, the locator
        field will be all FF.
        """
        return self._read('locator').decode('ascii')

    @property
    def r_locator(self) -> str:
        """
        Read-only. Associated connections with a unique 1-wire code (reversed).

        Uses an extension of the 1-wire design from iButtonLink company that
        associated 1-wire physical connections with a unique 1-wire code.
        If the connection is behind a Link Locator the locator will show a
        unique 8-byte number (16 character hexidecimal) starting with family
        code FE.

        If no Link Locator is between the device and the master, the locator
        field will be all FF.
        """
        return self._read('r_locator').decode('ascii')

# coding: utf-8
# ##############################################################################
#  (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
This module contains the implementation for the Korad KD3005P PSU remote control.
Uses PySerial to control the PSU.
"""
from typing import ContextManager, List, Any
from contextlib import contextmanager

import serial
import time

from .types import PowerSupply, PowerSupplyCapability, PowerSupplyChannelCapability, \
    PowerSupplyProtectionMode
from ..types import InstrumentType
from ..instrument import Instrument

KORAD_DELAY_TIME = .08
KORAD_BAUD_RATE = 9600


def read_korad_string(ser, length=None):
    """KORAD sends 0-terminated strings, this looks for them."""
    result = []
    c = ser.read(1).decode('ascii')
    while len(c) > 0 and ord(c) != 0:
        result.append(c)
        if length is not None and len(result) == length:
            break
        c = ser.read(1).decode('ascii')

    return ''.join(result)


def float_or_none(value):
    try:
        return float(value)
    except (TypeError, ValueError) as e:
        return None


class _KoradKD3005PContext(PowerSupply):
    def __init__(self, ser: serial.Serial):
        self.ser = ser

        self.ser.write(f'VSET1:0.0'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        self.ser.write(f'ISET1:0.0'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        self.ser.write(f'OUT0'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)

    def set_output_ocp(self, channel: int, is_on: bool):
        """
        Sets the overcurrent protection on or off.

        :param channel: Ignored
        :param is_on: If OCP should be on or not.
        """
        self.ser.write(f'OCP{"1" if is_on else "0"}'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)

    def set_output_ovp(self, channel: int, value: float):
        """Not implemented"""
        raise NotImplementedError('No OCV on Korad KD3005P')

    def set_output_voltage(self, channel: int, voltage: float):
        """
        Sets the output voltage of the KORAD.

        :param channel: Ignored
        :param voltage: The voltage to set the KORAD to.
        """
        self.ser.write(f'VSET1:{voltage:.2f}'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)

    def set_output_current(self, channel: int, current: float):
        """
        Sets the output current limit of the KORAD.

        :param channel: Ignored
        :param current: The current to set the korad to.
        """
        self.ser.write(f'ISET1:{current:.2f}'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)

    def get_output_voltage(self, channel: int) -> float:
        """
        Gets the output voltage of the KORAD.

        :param channel: Ignored
        :return: The output voltage.
        """
        self.ser.write(f'VOUT1?'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        result = read_korad_string(self.ser, 5)
        return float_or_none(result)

    def get_output_current(self, channel: int) -> float:
        """
        Gets the output current of the KORAD.

        :param channel: Ignored
        :return: The actual output current.
        """
        self.ser.write(f'IOUT1?'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        result = read_korad_string(self.ser, 5)
        return float_or_none(result)

    def clear_errors(self):
        """No `clear_errors` on KORAD SCPI commads. raises `NotImplementedError`"""
        raise NotImplementedError('No clear_errors on Korad KD3005P')

    def clear_faults(self):
        """No `clear_faults` on KORAD SCPI commads. raises `NotImplementedError`"""
        raise NotImplementedError('No clear_faults on Korad KD3005P')

    @property
    def error_count(self) -> int:
        """No `error_count` on KORAD SCPI commads. raises `NotImplementedError`"""
        raise NotImplementedError('No error_count on Korad KD3005P')

    @property
    def fault_count(self) -> int:
        """No `fault_count` on KORAD SCPI commads. raises `NotImplementedError`"""
        raise NotImplementedError('No fault_count on Korad KD3005P')

    def set_output_on(self, channel: int, is_on: bool):
        """
        Sets the output on or off on the korad.

        :param channel: Ignored
        :param is_on: If the output should be on or off
        """
        self.ser.write(f'OUT{"1" if is_on else "0"}'.encode('ascii'))

    def close(self):
        """Closes the resources for the KORAD KD3005P PSU."""
        self.ser.write(f'VSET1:0'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        self.ser.write(f'ISET1:0'.encode('ascii'))
        time.sleep(KORAD_DELAY_TIME)
        self.ser.write(f'OUT0'.encode('ascii'))


class KoradKD3005P(Instrument):
    """Instrument implementation for the Korad"""
    def __init__(self, path: str):
        """
        Initializes the Korad PSU.

        :param path: The path to the serial device for the Korad.
        """
        self.path = path

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        """Returns `InstrumentType.PowerSupply`"""
        return InstrumentType.PowerSupply

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return PowerSupplyCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        """Channel capabilities of KORAD KD3005P"""
        return [PowerSupplyChannelCapability(0, 30, 5, None, PowerSupplyProtectionMode.OCP)]

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """Yields the context object of the korad PSU."""
        ser = serial.Serial(port=self.path, baudrate=KORAD_BAUD_RATE, timeout=1)

        # Initialize PSU to 0 for voltage, current
        psu = _KoradKD3005PContext(ser)
        yield psu
        psu.close()

        ser.close()

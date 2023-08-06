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

from contextlib import contextmanager
from typing import ContextManager, List, Any
from datetime import timedelta

from array_devices import Load as TekPowerLoad
from serial import Serial

from .types import Load, LoadMode, LoadCapability, LoadChannelCapability
from ..types import InstrumentType
from ..instrument import Instrument

TEKPOWER_3410A_BAUD = 9600


class _TekPower3410AContext(Load):
    """Underlying context object to use for the TekPower3410A Load."""

    def __init__(self, device: TekPowerLoad):
        self.device = device
        self.device.remote_control = True

    def _validate_channel(self, channel):
        """Raises a value error if the channel is greater than 0, since the TekPower only has one channel."""
        if channel > 0:
            raise ValueError('TekPower 3410A does not have more than 1 channel.')

    def set_output_on(self, channel: int, is_on: bool):
        """Sets the TekPower 3710A load ON or OFF. `channel` is not used, as there is only one."""
        self._validate_channel(channel)
        self.device.load_on = is_on

    def set_output_state(self, channel: int, mode: LoadMode, value: float):
        """Sets the output state of the TekPower 3410A Load."""
        self._validate_channel(channel)
        if mode == LoadMode.Current:
            self.device.set_load_current(value)
        elif mode == LoadMode.Power:
            self.device.set_load_power(value)
        elif mode == LoadMode.Resistance:
            self.device.set_load_resistance(value)
        else:
            raise ValueError(f'Load mode {mode} is not supported on the TekPower 3710A.')

    def get_load_voltage(self, channel: int) -> float:
        """Gets the input voltage on the input of the TekPower load"""
        self._validate_channel(channel)
        self.device.update_status()
        return self.device.voltage

    def get_load_current(self, channel: int) -> float:
        """Gets the input current on the input of the TekPower load"""
        self._validate_channel(channel)
        self.device.update_status()
        return self.device.current

    def get_load_power(self, channel: int) -> float:
        """Gets the input power on the input of the TekPower load"""
        self._validate_channel(channel)
        self.device.update_status()
        return self.device.power

    def get_load_resistance(self, channel: int) -> float:
        """Gets the input resistance on the input of the TekPower load"""
        self._validate_channel(channel)
        self.device.update_status()
        return self.device.resistance

    def get_load_discharge_time(self, channel: int) -> timedelta:
        """Queries the load for the total discharge time."""
        raise NotImplementedError()

    def get_load_watthours(self, channel: int) -> float:
        """Queries the load for the total watthour discharge time."""
        raise NotImplementedError()

    def get_load_capacity(self, channel: int) -> float:
        """Queries the load for the mA capacity of the battery."""
        raise NotImplementedError()

    def close(self):
        """Turns off the inputs and turns off remote control."""
        self.set_output_on(0, False)


class TekPower3410A(Instrument):
    @classmethod
    def instrument_capabilities(cls) -> Any:
        return LoadCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        """
        TekPower 3710A is a single-channel load with CC/CR/CP modes.
        """
        return [LoadChannelCapability(max_voltage=360.0,
                                      min_voltage=0.0,
                                      max_power=150.0,
                                      modes=[
                                          LoadMode.Resistance,
                                          LoadMode.Power,
                                          LoadMode.Current
                                      ])]

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        return InstrumentType.Load

    def __init__(self, port: str, address: int, baudrate: int = TEKPOWER_3410A_BAUD):
        """
        Initializes the TekPower 3410A digital load.

        :param port: The serial port to initialize the load on.
        :param address: The address to use to communicate with the load.
        :param baudrate: The baudrate to communicate at.
        """
        if baudrate < 0:
            raise ValueError(f"{baudrate} is an invalid baudrate.")
        if address < 0 or address > 32:
            raise ValueError(f"{address} is out of the range of [0, 32]")
        self.ser = Serial()
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.timeout = 1.0

        self.address = address

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """
        Opens the serial port to the TekPower load, allowing usage of the digital load.

        :return: A context to the load.
        """
        self.ser.open()
        load = TekPowerLoad(self.address, self.ser)
        context = _TekPower3410AContext(load)
        yield context
        context.close()
        self.ser.close()

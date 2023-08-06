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

from abc import abstractmethod
from enum import Enum
from typing import NamedTuple, Iterable, Protocol
from datetime import timedelta


class LoadMode(Enum):
    """
    Different modes that a digital load could be in:
        Current    -> Constant Current
        Power      -> Constant Power
        Resistance -> Constant Resistance
        Voltage    -> Constant Voltage
    """
    Current = 1,
    Power = 2,
    Resistance = 3,
    Voltage = 4


LoadCapability = NamedTuple('LoadCapability', [])
LoadChannelCapability = NamedTuple('LoadChannelCapability', [('max_voltage', float),
                                                             ('min_voltage', float),
                                                             ('max_power', float),
                                                             ('modes', Iterable[LoadMode])])


class Load(Protocol):
    """
    A protocol representing the different behaviors of a digital load.
    """
    @abstractmethod
    def set_output_on(self, channel: int, is_on: bool):
        """Sets if `channel` on load `is_on` or not."""
        raise NotImplementedError()

    @abstractmethod
    def set_output_state(self, channel: int, mode: LoadMode, value: float):
        """
        Sets the output of the load to CC/CV/CP/CR with the value in mA/mV/mW/mOhms

        :param channel: Which channel to select.
        :param mode: The type of mode the power supply is in.
        :param value: The value of the mode
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_voltage(self, channel: int) -> float:
        """
        Gets the load voltage for `channel` on the load input.

        :param channel: The channel to get the load voltage for.
        :return: The voltage on `channel` for the load, in volts.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_current(self, channel: int) -> float:
        """
        Gets the load current for `channel` on the load input.

        :param channel: The channel to get the load current for.
        :return: The current on `channel` for the load, in amps.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_power(self, channel: int) -> float:
        """
        Gets the load power for `channel` on the load input.

        :param channel: The channel to get the load power usage for.
        :return: The power on `channel` for the load, in watts.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_resistance(self, channel: int) -> float:
        """
        Gets the resistance for `channel` on the load input.

        :param channel: The channel to get the load resistance for.
        :return:  The resistance on `channel` for the load, in ohms.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_discharge_time(self, channel: int) -> timedelta:
        """
        Gets the total time the load has been discharging.

        :param channel: The channel to get the discharging time for.
        :return: The total time the load has been running.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_watthours(self, channel: int) -> float:
        """
        Gets the total watthours the load has discharged.

        :param channel: the channel to get the information for.
        :return: The total watt hours discharge for `channel`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_load_capacity(self, channel: int) -> float:
        """
        Gets the total load capacity.

        :param channel: The channel to get the information for.
        :return: The total load capacity discharged. 
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """Closes the load, turning off the inputs and resending control to the local front panel."""

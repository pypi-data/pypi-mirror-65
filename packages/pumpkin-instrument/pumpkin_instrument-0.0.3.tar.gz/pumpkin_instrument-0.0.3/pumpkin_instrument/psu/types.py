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
from typing import NamedTuple, Optional, Protocol


class PowerSupplyProtectionMode(Enum):
    """
    The different power supply protection modes that are supported on the power supply channels.
    """
    OCP = 0
    OCV = 1


PowerSupplyProtectionModeAll = [PowerSupplyProtectionMode.OCP, PowerSupplyProtectionMode.OCV]
PowerSupplyCapability = NamedTuple('PowerSupplyCapability', [])
PowerSupplyChannelCapability = NamedTuple('PowerSupplyChannelCapability', [('min_voltage', float),
                                                                           ('max_voltage', float),
                                                                           ('max_current', float),
                                                                           ('max_ocv', Optional[float]),
                                                                           ('protection_modes',
                                                                            PowerSupplyProtectionMode)])


class PowerSupply(Protocol):
    """
    A protocol representing the different behaviors of a power supply
    """

    @abstractmethod
    def set_output_on(self, channel: int, is_on: bool):
        """Sets if the `channel` `is_on` on the power supply."""
        raise NotImplementedError()

    @abstractmethod
    def set_output_ocp(self, channel: int, is_on: bool):
        """
        Sets the Overcurrent protection for `channel` ON or OFF.

        :param channel: The channel to set the Overcurrent protection on.
        :param is_on: If the overcurrent protection is ON or OFF.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_output_ovp(self, channel: int, value: float):
        """
        Sets the overvoltage protection to the specified voltage value.

        :param channel: The channel to set the overvoltage protection on.
        :param value: The voltage to set the overvoltage proection to.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_output_voltage(self, channel: int, voltage: float):
        """
        Sets the `voltage` on `channel`.

        :param channel: The `channel` to set the voltage on.
        :param voltage: Voltage (in volts) to use for `channel`.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_output_current(self, channel: int, current: float):
        """
        Sets the `current` limit on `channel`.

        :param channel: The `channel` number to use.
        :param current: The current limit in amps.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_output_voltage(self, channel: int) -> float:
        """
        Gets the output voltage read by the power supply on the given `channel`.

        :param channel: The channel to get the voltage for.
        :return: The current voltage read in `volts`
        """
        raise NotImplementedError()

    @abstractmethod
    def get_output_current(self, channel: int) -> float:
        """
        Gets the output current read by the power supply on the given `channel`.

        :param channel: The channel to get the output current for.
        :return: The output current on `channel`.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_errors(self):
        """
        Clears any reported error count on the power supply. Use `clear_faults` to clear any overvoltage/overcurrent
        limit trips. Note an `error` is a command error, NOT a power supply fault.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_faults(self):
        """
        Clears any faults on the power supply such as an overcurrent protection trip. Use `clear_errors` to clear any
        command errors.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def error_count(self) -> int:
        """
        Gets the error count on the power supply. Can be reset via `clear_errors` method.

        :return: The amount of command errors on the power supply
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def fault_count(self) -> int:
        """
        Gets the amount of faults on the power supply. Can be reset via 'clear_faults` method.

        :return: The amount of faults on the power supply
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """Resets the PSU to a safe state."""
        raise NotImplementedError()


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
This module contains the implementation for the Rigol DL3021A Digital Load remote
control.
Uses PyVISA to command the unit.
"""
from contextlib import contextmanager
from typing import ContextManager, List, Any
from datetime import timedelta
import time

import visa
from pyvisa import resources

from .types import Load, LoadMode, LoadCapability, LoadChannelCapability
from ..types import InstrumentType
from ..instrument import Instrument

MODE_TO_OUTPUT_CMD = {
    LoadMode.Resistance: ':SOUR:RES:LEV:IMM',
    LoadMode.Power: ':SOUR:POW:LEV:IMM',
    LoadMode.Current: ':SOUR:CURR:LEV:IMM',
    LoadMode.Voltage: ':SOUR:VOLT:LEV:IMM'
}
MODE_TO_OUTPUT_MODE_CMD = {
    LoadMode.Resistance: ':SOUR:FUNC RES',
    LoadMode.Current: ':SOUR:FUNC CURR',
    LoadMode.Power: ':SOUR:FUNC POW',
    LoadMode.Voltage: ':SOUR:FUNC VOLT'
}
MODE_TO_MEASURE_QUERY = {
    LoadMode.Resistance: ':MEAS:RES:DC?',
    LoadMode.Current: ':MEAS:CURR:DC?',
    LoadMode.Power: ':MEAS:POW:DC?',
    LoadMode.Voltage: ':MEAS:VOLT:DC?'
}


class _RigolDL3021AContext(Load):
    def __init__(self, visa_instr: resources.MessageBasedResource):
        """
        Initializes the Rigol DL3021A digital load from the VISA resource.

        :param visa_instr: The VISA resource object for the digital load.
        """
        self.instr = visa_instr
        self.instr.write('*CLS; *RST')
        time.sleep(0.25)

        # Start off in CC mode
        self.instr.write(':SOUR:FUNC CURR')
        self.instr.write(':SOUR:CURR:LEV:IMM 0')
        self.instr.write(':SOUR:INP:STAT 0')

        # Set to battery discharge mode
        self.instr.write('SOUR:FUNC:MODE BATT')
        
        # Allow time for reset
        # time.sleep(1)

    def set_output_on(self, channel: int, is_on: bool):
        """Sets the Rigol's output on or off"""
        self.instr.write(f':SOUR:INP:STAT {"1" if is_on else "0"}')

    def set_output_state(self, channel: int, mode: LoadMode, value: float):
        """Sets the output state of the Rigol to CC/CP/CR/CV."""
        mode_cmd = MODE_TO_OUTPUT_MODE_CMD[mode]
        set_cmd = MODE_TO_OUTPUT_CMD[mode]
        self.instr.write(mode_cmd)
        self.instr.write(f'{set_cmd} {value:.3f}')

    def get_load_voltage(self, channel: int) -> float:
        """Queries the loads voltage on the input."""
        query_cmd = MODE_TO_MEASURE_QUERY[LoadMode.Voltage]
        return float(self.instr.query(query_cmd))

    def get_load_current(self, channel: int) -> float:
        """Queries the loads current on the input"""
        query_cmd = MODE_TO_MEASURE_QUERY[LoadMode.Current]
        return float(self.instr.query(query_cmd))

    def get_load_power(self, channel: int) -> float:
        """Queries the loads power on the input."""
        query_cmd = MODE_TO_MEASURE_QUERY[LoadMode.Power]
        return float(self.instr.query(query_cmd))

    def get_load_resistance(self, channel: int) -> float:
        """Queries the loads resistance on the input."""
        query_cmd = MODE_TO_MEASURE_QUERY[LoadMode.Resistance]
        return float(self.instr.query(query_cmd))

    def get_load_discharge_time(self, channel: int) -> timedelta:
        """Queries the load for the total discharge time."""
        query_cmd = ":MEAS:DISCT?"
        rtn = self.instr.query(query_cmd)
        hours, mins, secs = [float(x) for x in rtn.split(':')]
        return timedelta(hours=hours, minutes=mins, seconds=secs)

    def get_load_watthours(self, channel: int) -> float:
        """Queries the load for the total watthour discharge time."""
        query_cmd = ":MEAS:WATT?"
        return float(self.instr.query(query_cmd))

    def get_load_capacity(self, channel: int) -> float:
        """Queries the load for the mA capacity of the battery."""
        query_cmd = ":MEAS:CAP?"
        return float(self.instr.query(query_cmd))

    def close(self):
        """Sets the loads state to off in CC."""
        # End in CC mode
        self.instr.write(':SOUR:FUNC CURR')
        self.instr.write(':SOUR:CURR:LEV:IMM 0')
        self.instr.write(':SOUR:INP:STAT 0')


class Rigol3021A(Instrument):
    def __init__(self, visa_str: str, *args, **kwargs):
        """Initializes the instrument context manager for the Rigol DL3021A"""
        self.rm = visa.ResourceManager(*args, **kwargs)
        self.inst_str = visa_str

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        return InstrumentType.Load

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return LoadCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return [LoadChannelCapability(150, 0, 200,
                                      [LoadMode.Resistance, LoadMode.Voltage, LoadMode.Current, LoadMode.Power])]

    @contextmanager
    def use(self) -> ContextManager[Any]:
        inst = self.rm.open_resource(self.inst_str)
        rigol = _RigolDL3021AContext(inst)
        yield rigol
        rigol.close()
        inst.close()

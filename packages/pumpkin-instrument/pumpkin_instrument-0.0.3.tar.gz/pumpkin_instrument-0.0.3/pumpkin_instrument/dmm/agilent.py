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
from typing import ContextManager, List, Any

import visa
from pyvisa import resources

from .types import Multimeter, MultimeterMode, MultimeterCapability, MultimeterChannelCapability
from ..types import InstrumentType
from ..instrument import Instrument

SCPI_COMMAND_MAP = {
    MultimeterMode.CurrentAC: 'MEAS:CURR:AC?',
    MultimeterMode.CurrentDC: 'MEAS:CURR:DC?',
    MultimeterMode.Resistance: 'MEAS:RES?',
    MultimeterMode.ResistanceFourWire: 'MEAS:FRES?',
    MultimeterMode.Temperature: 'MEAS:TEMP? THER,5000',
    MultimeterMode.TemperatureFourWire: 'MEAS:TEMP? FTH,5000',
    MultimeterMode.VoltageDC: 'MEAS:DC?',
    MultimeterMode.VoltageAC: 'MEAS:AC?'
}


class _Agilent33410AContext(Multimeter):
    def __init__(self, visa_instr: resources.MessageBasedResource):
        """
        Initializes the Agilent 33410A context with the given VISA resource.

        :param visa_instr: The visa resource for the Agilent DMM.
        """
        self.instr = visa_instr
        self.instr.write('*CLS; *RST')

    def measure(self, channel: int, mode: MultimeterMode) -> float:
        return float(self.instr.query(SCPI_COMMAND_MAP[mode]))

    def close(self):
        """Sends the CLS and RST SCPI commands."""
        self.instr.write('*CLS;*RST\n'.encode('ascii'))


class Agilent33410A(Instrument):
    def __init__(self, visa_str: str, *args, **kwargs):
        """Initializes the instrument context manager for the Agilent 33410A."""
        self.rm = visa.ResourceManager(*args, **kwargs)
        self.inst_str = visa_str

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        return InstrumentType.Multimeter

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return MultimeterCapability()

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return MultimeterChannelCapability(6.5, 2.0, 1000, -1000,
                                           [MultimeterMode.TemperatureFourWire, MultimeterMode.Temperature,
                                            MultimeterMode.ResistanceFourWire, MultimeterMode.Resistance,
                                            MultimeterMode.CurrentDC, MultimeterMode.CurrentAC,
                                            MultimeterMode.VoltageAC, MultimeterMode.VoltageDC])

    def use(self) -> ContextManager[Any]:
        inst = self.rm.open_resource(self.inst_str)
        agilent = _Agilent33410AContext(inst)
        yield agilent
        agilent.close()
        inst.close()

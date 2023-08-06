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
Contains all of the protocols and types used throughout the pumpkin_instrument implementations.
"""
from enum import Enum

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class InstrumentType(Enum):
    """
    Represents the various types of lab instruments usable.
    """
    PowerSupply = 1,
    Load = 2,
    Multimeter = 3

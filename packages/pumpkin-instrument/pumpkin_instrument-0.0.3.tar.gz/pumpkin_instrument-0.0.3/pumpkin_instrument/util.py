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
"""Holds utility functions such as `get_tcpip_visa_str` or `get_usb_visa_str`"""


def get_tcpip_visa_str(hostname: str) -> str:
    """
    Returns VISA string for TCP/IP resource.

    :param hostname: The hostname/ip address to use.
    :return: The VISA resource string.
    """
    return f'TCPIP0::{hostname}::inst0::INSTR'

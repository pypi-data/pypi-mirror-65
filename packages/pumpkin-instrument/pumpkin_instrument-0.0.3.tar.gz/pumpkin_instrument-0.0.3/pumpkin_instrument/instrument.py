from abc import abstractmethod
from typing import Union, Protocol, List, ContextManager, Any

from .types import InstrumentType


class Instrument(Protocol):
    @classmethod
    @abstractmethod
    def instrument_type(cls) -> InstrumentType:
        """
        What type of pumpkin_instrument is implemented. Currently there is:
            - PowerSupply
            - Load
            - Multimeter
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def instrument_capabilities(cls) -> Any:
        """
        Describes the capabilities of the pumpkin_instrument that apply to all channels. Currently this is only a placeholder
        for future API expansion.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def channel_capabilities(cls) -> List[Any]:
        """

        """
        raise NotImplementedError()

    @abstractmethod
    def use(self) -> ContextManager[Any]:
        """
        Uses the pumpkin_instrument, taking control of it.
        """
        raise NotImplementedError()
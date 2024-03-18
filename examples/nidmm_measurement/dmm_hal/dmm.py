from abc import ABC, abstractmethod


class Dmm(ABC):
    """Multimeter abstraction"""

    @abstractmethod
    def configure_measurement_digits():
        pass


    @abstractmethod
    def read():
        pass
from abc import ABC, abstractmethod
from enum import Enum

class StrategyEnum(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    CAREFUL_BANDING = "careful_banding"


class Strategy():
    @abstractmethod
    def defineAction(self, player):
        pass

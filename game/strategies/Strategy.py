from abc import ABC, abstractmethod
from enum import Enum

class StrategyEnum(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    CAREFUL_BANDING = "careful_banding"


class Strategy():
    @abstractmethod
    def defineAction(self, player, list_of_players):
        pass

class HelperFunctions():
    @staticmethod
    def knowledge_compare_AgtB(player, A, B):
        # player.
        print("I am a static method")
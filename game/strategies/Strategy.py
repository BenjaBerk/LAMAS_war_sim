from abc import abstractmethod
from enum import Enum
import re

class StrategyEnum(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    CAREFUL_BANDING = "careful_banding"


class Strategy():
    @abstractmethod
    def defineAction(self, player, list_of_players):
        pass

    @abstractmethod
    def __str__(self):
        pass

class HelperFunctions():
    @staticmethod
    def knowledge_compare_AltB(player, A, B):
        for formula in player.knowledge:
            str1 = HelperFunctions.findStrength(player, A)
            str2 = HelperFunctions.findStrength(player, B)
            if not (str1 and str2):
                raise Exception()
            return (
                (str1 == "w" and (str2 == "m" or str2 == "s")) or
                (str1 == "m" and str2 == "s")
            )

    @staticmethod
    def findStrength(player, A):
        for formula in player.knowledge:
            result = re.findall('[wms]', str(formula))[0] # that only works because of the specific subset of formulas we are using
            print(f"{type(result)}, {result}, {result.group}")

    @staticmethod
    def findWeakest(player):
        pass

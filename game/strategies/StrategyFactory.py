from strategies.Aggressive import Aggressive
from strategies.CarefulBanding import CarefulBanding
from strategies.Strategy import StrategyEnum
from strategies.Defensive import Defensive

class StrategyFactory():
    def __init__(self):
        pass
            
    def create(self, strategy=StrategyEnum.DEFENSIVE):
        if (strategy == StrategyEnum.DEFENSIVE or strategy == StrategyEnum.DEFENSIVE.value):
            return Defensive()
        elif (strategy == StrategyEnum.AGGRESSIVE or strategy == StrategyEnum.AGGRESSIVE.value):
            return Aggressive()
        elif (strategy == StrategyEnum.CAREFUL_BANDING or strategy == StrategyEnum.CAREFUL_BANDING.value):
            return CarefulBanding()

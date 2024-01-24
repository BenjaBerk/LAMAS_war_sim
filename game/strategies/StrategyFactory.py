from strategies.Aggressive import Aggressive
from strategies.CarefulBanding import CarefulBanding
from strategies.Strategy import StrategyEnum
from strategies.Defensive import Defensive

class StrategyFactory():
    def __init__(self):
        pass
            
    def create(self, strategy=StrategyEnum.DEFENSIVE):
        if (strategy == StrategyEnum.DEFENSIVE):
            return Defensive()
        elif (strategy == StrategyEnum.AGGRESSIVE):
            return Aggressive()
        elif (strategy == StrategyEnum.CAREFUL_BANDING):
            return CarefulBanding()

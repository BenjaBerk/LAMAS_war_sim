from strategies.Strategy import StrategyEnum
from strategies.Defensive import Defensive

class StrategyFactory():
    def __init__(self):
        pass
            
    def get(self, strategy=StrategyEnum.DEFENSIVE):
        if (strategy == StrategyEnum.DEFENSIVE):
            return Defensive()
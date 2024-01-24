from strategies.Strategy import Strategy

class CarefulBanding(Strategy):
    def __init__(self):
        pass
        
    def defineAction(self, player, list_of_players) -> str:
        return 2
        pass

    def __str__(self):
        return "careful_banding"
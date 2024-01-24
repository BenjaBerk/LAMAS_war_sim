from strategies.Strategy import Strategy

class Aggressive(Strategy):
    def __init__(self):
        pass

    def defineAction(self, player, list_of_players) -> str:
        return 2
        pass

    def __str__(self):
        return "aggressive"
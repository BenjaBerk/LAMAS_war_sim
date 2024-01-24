from strategies.Strategy import Strategy, HelperFunctions

class Defensive(Strategy):
    def __init__(self):
        pass
        
    def defineAction(self, player, list_of_players) -> str:
        me = player.name[0]
        opponents = [x for x in list_of_players if me != x]
        HelperFunctions.knowledge_compare_AgtB(player)
        # for op in opponents:
            # if ()
        print(f"me - {me}, opponents - {opponents}")
        return 2
        pass
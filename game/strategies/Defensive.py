from strategies.Strategy import Strategy, HelperFunctions

class Defensive(Strategy):
    def __init__(self):
        pass
        
    def defineAction(self, player, list_of_players) -> str:
        me = player.name[0]
        target = ""
        opponents = [x for x in list_of_players if me != x]
        for op in opponents:
            if (HelperFunctions.knowledge_compare_AltB(player, me, op)):
                target = me
        if not target:
            target = HelperFunctions.findWeakest(player)
        print(f"me - {me}, opponents - {opponents}")
        return 2
        pass

    def __str__(self):
        return "defensive"
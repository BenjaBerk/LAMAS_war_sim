import Player
from random import shuffle
import WorldModel

class WarSimulation:
    # initializes the simulation
    def __init__(self, n_players=6):
        # construct n players
        self.n_players = n_players
        self.names = [
            'Alexander', 
            'Boudica', 
            'Cleopatra', 
            'De Gaulle', 
            'Elizabeth',
            'Frederick',
            'Gandhi', 
            'Harald Bluetooth',
            'Isabella', 
            'Julius Caesar', 
            'Khan'
            ]
        shuffle(self.names)
        self.names = self.names[:n_players]
        self.players = []
        for name in self.names:
            player = Player.Player(name=name)
            self.players.append(player)
            print(player)

        model = WorldModel.WorldModel(n_players=self.n_players, players=self.names)
        print(f"All possible worlds at start of game: {len(model.worlds)}")
    # each player gets to scout

    def scout_round(self):
        #TODO
        print("Performing scout round:")
    
    # based on knowledge, declare wars
    def resolve_round(self):
        #TODO
        print("Performing resolve round:")


if __name__ == "__main__":
    game = WarSimulation()
    # we have 2 scout rounds, then we resolve
    game.scout_round()
    game.scout_round()
    game.resolve_round()

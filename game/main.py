from Player import Player
from Atom import Atom
from Formula import Formula
import random
import WorldModel
import argparse

class WarSimulation:
    # initializes the simulation
    def __init__(self, n_players=6, visualize=False):
        # construct n players
        self.visualize = visualize
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
        random.shuffle(self.names)
        self.names = self.names[:n_players]
        self.players = []
        self.players_bn = {}
        for name in self.names:
            player = Player(name=name)
            self.players.append(player)
            self.players_bn[name] = player
        
        self.show_players()

        model = WorldModel.WorldModel(n_players=self.n_players, players=self.players)
        print(f"All possible worlds at start of game: {len(model.worlds)}")
        if self.visualize:
            model.visualize_worlds()

    # each player gets to scout
    def scout_round(self):
        print("\nPerforming scout round:")
        # step 1: place scouts
        scout_placement = {}
        for name in self.names: scout_placement[name] = []
        for name in self.names: scout_placement[random.choice(self.names)].append(name)
        print("scout placement:", scout_placement)

        # step 2: infer knowledge
        print("adding gained knowledge")
        for location in scout_placement:
            # determine strength
            strength = self.players_bn[location].strength
            strength_atom = Atom(strength, self.players_bn[location])
            for leader in scout_placement[location]:
                # player should know strength
                self.players_bn[leader].add_knowledge(strength_atom)
                # other players at the same location know the leader knows the strength
                formula = Formula(form_left=strength_atom, op_type='unary', op=f'K_{leader[0]}')
                for other in scout_placement[location]:
                    if (leader != other): self.players_bn[other].add_knowledge(formula)

        print("\nstate after round:")
        self.show_players()

    # based on knowledge, declare wars
    def resolve_round(self):
        #TODO
        print("Performing resolve round:")
    
    def show_players(self):
        for player in self.players:
            print(player)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", type=int, choices=range(2, 7), default=6, help="number of players")
    parser.add_argument("-v", "--visualize", action="store_true", help="Create and plot model", default=False)
    args = parser.parse_args()
    game = WarSimulation(n_players=args.num_players, visualize=args.visualize)
    # we have 2 scout rounds, then we resolve
    game.scout_round()
    game.scout_round()
    game.resolve_round()

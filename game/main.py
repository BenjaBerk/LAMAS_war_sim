from Player import Player
from Atom import Atom
from Formula import Formula
import random

class WarSimulation:
    # initializes the simulation
    def __init__(self, n_players=3):
        # construct n players
        self.n_players = n_players
        self.names = [
            'Alexander', 
            'Boudica', 
            'Cleopatra', 
            'De Gaulle', 
            'Elizabeth',
            'Frederick'
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
    game = WarSimulation()
    # we have 2 scout rounds, then we resolve
    game.scout_round()
    game.scout_round()
    game.resolve_round()

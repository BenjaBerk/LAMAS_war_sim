from Player import Player
from Atom import Atom
from Formula import Formula
import random
from typing import List
import WorldModel
import argparse
from scenario import scenario
from strategies.Strategy import StrategyEnum

class WarSimulation:
    # initializes the simulation
    def __init__(self, n_players=3, visualize=False, strengths=None):
        # construct n players
        self.visualize = visualize
        self.n_players = n_players
        self.round_count = 1
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
        self.players: List(Player) = []
        self.players_bn = {}
        for i in range(len(self.names)):
            strength = strengths[i] if strengths else None
            player = Player(name=self.names[i], strength=strength, strategy=random.choice([StrategyEnum.AGGRESSIVE, StrategyEnum.DEFENSIVE, StrategyEnum.CAREFUL_BANDING]))
            self.players.append(player)
            self.players_bn[self.names[i]] = player
        self.show_players()

        self.model = WorldModel.WorldModel(n_players=self.n_players, players=self.players)
        print(f"All possible worlds at start of game: {len(self.model.worlds)}")
        if self.visualize:
            self.model.visualize_worlds(f'initial_model_{self.n_players}_players')

    # each player gets to scout
    def scout_round(self, decisions=None):
        print(f"\nPerforming scout round {self.round_count}:")

        # step 1: place scouts
        scout_placement = {}
        for name in self.names: scout_placement[name] = []
        if not decisions: #random
            print(f"random.choice(self.names) {random.choice(self.names)}, name {name}")
            for name in self.names: scout_placement[random.choice(self.names)].append(name)
        else: #scenario editor
            for i in range(len(decisions)):
                scout_placement[self.players[decisions[i]].name].append(self.players[i].name)
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
                # player knows that observed player knows their own strength
                formula = Formula(form_left=strength_atom, op_type='unary', op=f'K_{location[0]}')
                if location != leader: self.players_bn[leader].add_knowledge(formula)
                # other players at the same location know the leader knows the strength
                formula = Formula(form_left=strength_atom, op_type='unary', op=f'K_{leader[0]}')
                for other in scout_placement[location]:
                    if (leader != other): self.players_bn[other].add_knowledge(formula)
                # and if EVERYONE is there, also add common knowledge
                if len(scout_placement[location]) == self.n_players:
                    formula = Formula(form_left=strength_atom, op_type='unary', op='C')
                    self.players_bn[leader].add_knowledge(formula)

        print("\nstate after round:")
        self.show_players()
        self.model.remove_worlds()
        if self.visualize:
            self.model.visualize_worlds(f"model_after_scouting_round{self.round_count}_{self.n_players}_players")
        self.round_count += 1

    # based on knowledge, declare wars
    def resolve_round(self):
        print("Performing resolve round:")
        
        actions = []
        players_initials = map(lambda player: player.name[0], self.players)
        # print("AAAAA", list(players_initials) )
        #TODO
        for player in self.players:
            # print(f"player - {player}")
            # print(f"player.strategy - {player.strategy}")
            # print(f"player.strategy.defineAction - {player.strategy.defineAction}")
            actions.append(player.strategy.defineAction(player, players_initials))
        
        print(actions)
        
    
    def show_players(self):
        for player in self.players:
            print(player)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_players", type=int, choices=range(2, 7), default=3, help="number of players")
    parser.add_argument("-r", "--scout_rounds", type=int, choices=range(1, 7), default=2, help="number of scout rounds")
    parser.add_argument("-v", "--visualize", action="store_true", help="Create and plot model", default=False)
    parser.add_argument("-s", "--scenario", action="store_true", default=False,
                        help="read the input from scenario.py instead of using random actions. Overwrites -n and -r.")
    args = parser.parse_args()
    print(args)

    num_players = args.num_players
    visualize = args.visualize
    scout_rounds = args.scout_rounds
    if (args.scenario):
        print(scenario)
        num_players = len(scenario["strengths"])
        scout_rounds = len(scenario["decisions"])

    if num_players > 4 and visualize:
        print(f"You have chosen to visualize the model for {num_players} players, this can take a very long "
              f"time. \n Do you want to proceed anyway? ")
        answer = input("yes/no: ")
        if answer == "yes":
            pass
        else:
            raise SystemExit()

    game = WarSimulation(n_players=num_players, visualize=visualize, strengths=scenario["strengths"] if args.scenario else None) #Sorry for making this line a hell to read! -S
    # we have some scout rounds, then we resolve
    if args.scenario:
        for i in range(scout_rounds): game.scout_round(scenario["decisions"][i])
    else:
        for i in range(scout_rounds): game.scout_round() #random decisions
    game.resolve_round()

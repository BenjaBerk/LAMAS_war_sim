import Player
from random import shuffle


class WarSimulation:
    def __init__(self, n_players=6):
        self.n_players = n_players
        self.names = ['Ghandi', 'Lincoln', 'Victoria', 'Cleopatra', 'Montezuma', 'Something']
        shuffle(self.names)
        self.names = self.names[:n_players]
        borders = self.create_borders()

        self.players = []
        for name in self.names:
            player = Player.Player(name=name, borders=borders[name])
            self.players.append(player)
            print(player)

    def create_borders(self):
        # Dictionary to store borders for each country
        borders = {}

        # Iterate through the countries to create borders
        for i in range(len(self.names)):
            country = self.names[i]

            # Determine the two neighboring countries
            neighbor1 = self.names[(i - 1) % len(self.names)]
            neighbor2 = self.names[(i + 1) % len(self.names)]

            # Store the borders in the dictionary
            borders[country] = [neighbor1, neighbor2]
        return borders


if __name__ == "__main__":
    # Do stuff
    game = WarSimulation()

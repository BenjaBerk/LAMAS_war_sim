class Player:
    def __init__(self, name, borders):
        self.strength = "strong"
        self.country_borders = borders
        self.name = name

        self.knowledge = self.init_knowledge()

    def init_knowledge(self):
        ...

    def update_knowledge(self):
        ...

    def update_model(self):
        ...

    def scout_border(self):
        ...

    def declare_war(self):
        ...

    def declare_peace(self):
        ...

    def __str__(self):
        return f"player: {self.name}, strength: {self.strength}, borders: {self.country_borders}"

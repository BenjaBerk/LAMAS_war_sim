# simple structure just for standardizing how logical atoms are represented
class Atom:
    # @param name: name of the atom
    # @param about: what player the atom pertains to, None if nothing
    # e.g. Player i is Strong could be type="s" about=i
    def __init__(self, name, about=None):
        self.name = name
        self.about = about
    
    def __str__(self):
        return f"{self.name}_{self.about.name[0]}"
import random
from Atom import Atom
from Formula import Formula

class Player:
    def __init__(self, name):
        self.strength = random.choice(["strong", "medium", "weak"])
        self.name = name
        self.init_knowledge()
    
    # the knowledge is a list of formulas
    # implicitly a conjunction of those formulas each preceded by K_i where i=player
    def init_knowledge(self):
        self.knowledge = {}
        self.add_knowledge(Atom(name=self.strength[0], about=self))
    
    def add_knowledge(self, formula):
        self.knowledge = {*self.knowledge, Formula(form_left=formula, op_type="unary", op=f"K_{self.name[0]}")}

    def __str__(self):
        knowledge_str = ' ^ '.join(str(formula) for formula in self.knowledge)
        return f"player: {self.name}, strength: {self.strength}, knowledge: {knowledge_str}"

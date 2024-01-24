import random
from Atom import Atom
from Formula import Formula
from strategies.Strategy import StrategyEnum
from strategies.StrategyFactory import StrategyFactory

class Player:
    def __init__(self, name, strength=None, strategy=StrategyEnum.DEFENSIVE):
        if not strength:
            self.strength = random.choice(["strong", "medium", "weak"])
        else:
            self.strength = strength
        self.name = name
        self.strategy = StrategyFactory().get(strategy)
        self.init_knowledge()
    
    # the knowledge is a list of formulas
    # implicitly a conjunction of those formulas each preceded by K_i where i=player
    def init_knowledge(self):
        self.knowledge = {}
        self.add_knowledge(Atom(name=self.strength, about=self))
    
    def add_knowledge(self, formula):
        formula = Formula(form_left=formula, op_type="unary", op=f"K_{self.name[0]}")
        if not (str(formula) in [str(knowledge) for knowledge in self.knowledge]):
            self.knowledge = {*self.knowledge, formula}

    def __str__(self):
        knowledge_str = ' ^ '.join(str(formula) for formula in self.knowledge)
        return f"player: {self.name}\n- strength: {self.strength}\n- knowledge: {knowledge_str}"

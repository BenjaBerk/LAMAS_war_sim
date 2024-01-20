
from itertools import product, combinations


class WorldModel:
    knowledge_base = []

    def __init__(self, n_players, players):
        player_ids = [f"{i[0]}" for i in players]
        n_worlds = n_players ** 3

        atoms = [['s', 'Not(m)', 'Not(w)'], ['Not(s)', 'm', 'Not(w)'],
                 ['Not(s)', 'Not(m)', 'w']]
        comb = list(product(player_ids, atoms))
        self.worlds = []
        possible_worlds = []
        world_id = 1
        for combo in combinations(comb, n_players):
            unique_first_elements = set(item[0] for item in combo)
            if len(unique_first_elements) == n_players:
                possible_worlds.append(list(combo))

        for w in possible_worlds:
            for p in w:
                player_id = p[0]
                atom1 = True if p[1][0] == 's' else False
                atom2 = True if p[1][1] == 'm' else False
                atom3 = True if p[1][2] == 'w' else False

                self.worlds.append({f's_{world_id}':
                                   {f'{player_id}:s': atom1, f'{player_id}:m': atom2, f'{player_id}:w': atom3}})
            world_id += 1


def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result


def add_reflexive_edges(worlds, relations):
    """Routine adds reflexive edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
            result[agent] = result_agents
    return result

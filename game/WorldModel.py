
from itertools import product, combinations


class WorldModel:
    knowledge_base = []

    def __init__(self, n_players, players):
        player_ids = [f"{i.name[0]}" for i in players]
        n_worlds = n_players ** 3

        atoms = [['s', 'Not(m)', 'Not(w)'], ['Not(s)', 'm', 'Not(w)'],
                 ['Not(s)', 'Not(m)', 'w']]
        comb = list(product(player_ids, atoms))
        self.worlds = {}
        possible_worlds = []
        world_id = 1
        for combo in combinations(comb, n_players):
            unique_first_elements = set(item[0] for item in combo)
            if len(unique_first_elements) == n_players:
                possible_worlds.append(list(combo))

        for w in possible_worlds:
            self.worlds[f's{world_id}'] = {}
            for p in w:
                player_id = p[0]
                atom1 = True if p[1][0] == 's' else False
                atom2 = True if p[1][1] == 'm' else False
                atom3 = True if p[1][2] == 'w' else False

                self.worlds[f's{world_id}'][f's_{player_id}'] = atom1
                self.worlds[f's{world_id}'][f'm_{player_id}'] = atom2
                self.worlds[f's{world_id}'][f'w_{player_id}'] = atom3
            world_id += 1

        # print(self.worlds)
        # Add relations to the model
        self.relations = {}
        for player in players:
            relations = []
            if player.strength == "strong":
                str_atom = f"s_{player.name[0]}"
            elif player.strength == "medium":
                str_atom = f"m_{player.name[0]}"
            else:
                str_atom = f"w_{player.name[0]}"

            for world in self.worlds:
                true_atom_s1 = [key for key, value in self.worlds[world].items() if value and key[2] == player.name[0]]
                for second_world in self.worlds:
                    if world == second_world:
                        continue
                    true_atom_s2 = [key for key, value in self.worlds[second_world].items() if
                                    value and key[2] == player.name[0]]
                    if true_atom_s1 == true_atom_s2:
                        relations.append((world, second_world))
                # if self.worlds[world][str_atom]:
                #     break
            self.relations[player.name] = relations
        # print(self.relations)
    def remove_worlds(self):
        ...

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

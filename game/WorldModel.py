from itertools import product, combinations
import graphviz
import pydot
from itertools import chain
import copy
from collections import defaultdict


class WorldModel:
    knowledge_base = []

    def __init__(self, n_players, players):
        self.n_players = n_players
        self.players = players
        self.real_atom = []
        for player in players:
            self.real_atom.append(f'{player.strength[0]}_{player.name[0]}')
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

        # for key, value in self.worlds:
        #     for atom in self.real_atom:
        #         if value[atom]:

        # Add relations to the model
        self.relations = {}
        for player in players:
            relations = []

            for world in self.worlds:
                true_atom_s1 = [key for key, value in self.worlds[world].items() if value and key[2] == player.name[0]]
                for second_world in self.worlds:
                    # if world == second_world:
                    #     continue
                    true_atom_s2 = [key for key, value in self.worlds[second_world].items() if
                                    value and key[2] == player.name[0]]
                    if true_atom_s1 == true_atom_s2:
                        relations.append((world, second_world))

            self.relations[player.name[0]] = relations

    def remove_worlds(self):
        for player in self.players:
            worlds_tb_removed = set()

            knowledge = player.knowledge
            # Remove every world that does not hold the current knowledge
            for w, value in self.worlds.items():
                for formula in knowledge:
                    formula_op = str(formula).split(' ')
                    valid = self.check_world_consistency(formula_op, w)
                    if not valid:
                        worlds_tb_removed.add(w)
                        break

            # Remove the relation to the invalid worlds for this player
            relations_tb_removed = []
            for r in self.relations[player.name[0]]:
                if r[0] in worlds_tb_removed or r[1] in worlds_tb_removed:
                    relations_tb_removed.append(r)
            self.relations[player.name[0]] = [r for r in self.relations[player.name[0]] if
                                              r not in relations_tb_removed]

        _, world_w_rel = get_unique_worlds(self.relations)

        current_worlds = list(self.worlds.keys()).copy()
        for w in current_worlds:
            if w not in world_w_rel:
                self.worlds.pop(w)

    def check_world_consistency(self, formula, world):
        for op in formula:
            if op[0] == 'K':  # Check whether the formula is at the end
                accessible_worlds = [t[1] for t in self.relations[op[2]] if t[0] == world]
                for w in accessible_worlds:  # Get all worlds accessible from this world; (w, u) in R_x
                    self.check_world_consistency(formula[1:], w)
            elif op[0] == 'C':
                accessible_worlds = [t[1] for u in self.relations.keys() for t in self.relations[u] if t[0] == world]
                for w in accessible_worlds:
                    self.check_world_consistency(formula[1:], w)
            else:
                # Return the valuation of the atom in this world
                if self.worlds[world][op]:
                    return True
                else:
                    return False

    def visualize_worlds(self, save_name):
        if len(self.worlds) <= 5:
            engine = 'dot'
        else:
            engine = 'circo'
        dot = graphviz.Graph(comment='Round Graph', format='png', engine=engine)
        merged_list, nodes_with_edges = get_unique_worlds(self.relations)

        nodes = [node for node in self.worlds.keys() if node in nodes_with_edges]
        rel_label = get_relation_labels(self.relations)
        print("Visualizing kripke model...\n")
        if self.n_players <= 3 or len(self.worlds) <= 15:
            # add labels, Up to three players, becomes too cluttered if more
            for node in nodes:
                true_atoms = [key for key, value in self.worlds[node].items() if value]
                node_name = f"{node}\n{','.join(true_atoms)}"
                if true_atoms == self.real_atom:
                    dot.node(node, label=node_name, color='red', filled='true')
                else:
                    dot.node(node, label=node_name)
        else:
            for node in nodes:
                dot.node(node)

        for src, dest in merged_list:
            if src == dest:
                continue
            if self.n_players <= 3 or len(self.worlds) <= 10:
                relation = ', '.join(['R' + item for item in rel_label[(str(src), str(dest))]])
                dot.edge(src, dest, dir='both', label=relation)

            else:
                dot.edge(src, dest, dir='none')
        # Save and render the graph
        output_file = f"plots/{save_name}"
        dot.render(output_file, view=True)


def get_relation_labels(relations):
    grouped_dict = defaultdict(list)

    for key, value in relations.items():
        for pair in value:
            grouped_dict[pair].append(key)

    result_dict = dict(grouped_dict)
    return result_dict


def get_unique_worlds(relation_dict):
    unique_tuples = set()

    # Iterate through the tuples in the dictionary value and add them to the set
    for tuple_list in relation_dict.values():
        for tuple_value in tuple_list:
            unique_tuples.add(tuple_value)

    # Convert the set back to a list
    merged_list = list({*map(tuple, map(sorted, list(unique_tuples)))})

    # Remove worlds without any relations
    world_w_rel = set(chain(*merged_list))
    return merged_list, world_w_rel

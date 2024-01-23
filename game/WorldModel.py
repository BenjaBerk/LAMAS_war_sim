
from itertools import product, combinations
import graphviz
import pydot
from itertools import chain


class WorldModel:
    knowledge_base = []

    def __init__(self, n_players, players):
        self.n_players = n_players
        self.players = players
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
            self.relations[player.name[0]] = [r for r in self.relations[player.name[0]] if r not in relations_tb_removed]

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
        dot = graphviz.Graph(comment='Round Graph', format='png', engine='circo')
        unique_tuples = set()

        # Iterate through the tuples in the dictionary value and add them to the set
        for tuple_list in self.relations.values():
            for tuple_value in tuple_list:
                unique_tuples.add(tuple_value)

        # Convert the set back to a list
        merged_list = list({*map(tuple, map(sorted, list(unique_tuples)))})
        # Define nodes and add them to the graph

        # Remove worlds without any relations
        nodes_with_edges = list(set(chain(*merged_list)))
        nodes = [node for node in self.worlds.keys() if node in nodes_with_edges]

        print("Visualizing kripke model...\n")
        if self.n_players <= 3:
            # add labels, Up to three players, becomes too cluttered if more
            for node in nodes:
                true_atoms = [key for key, value in self.worlds[node].items() if value]
                node_name = f"{node}\n{','.join(true_atoms)}"
                dot.node(node, label=node_name)
        else:
            for node in nodes:
                dot.node(node)

        for src, dest in merged_list:
            dot.edge(src, dest, dir='none', constraint='true')
        # Save and render the graph
        output_file = save_name
        dot.render(output_file, view=True)

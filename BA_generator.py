from random import choice
from functools import reduce


class BA_Graph:
    def __init__(self, interactive=True):
        self.nodes = []
        if interactive:
            print('This is Barabási–Albert generator')
            user_input = input(
                'Enter 3 parameters:\n- Node size\n- Number of new edges in connection iteration\n- Output file name\n')

            parameters = user_input.split()
            if len(parameters) < 3:
                exit('Enter all 3 parameters')
            n, m, file_name = parameters

            n_int = int(n)
            if n_int < 10:
                exit('Node size must be greater than 9')

            m_int = int(m)
            if m_int < 2:
                exit('Number of new edges in connection iteration must be greater than 1')

            self.generate(n_int, m_int)
            self.save_to_file(file_name)

    def generate(self, n, m):
        # initialize with C3 triangle
        self.nodes = [
            {1, 2},
            {0, 2},
            {0, 1}
        ]

        # loop
        initial_node_size = len(self.nodes)
        for new_node in range(initial_node_size,  n - initial_node_size):
            probability_2D = [[ix for _ in range(len(vertex))]
                              for ix, vertex in enumerate(self.nodes)]
            probability_flat = [v for prob in probability_2D for v in prob]

            if not probability_flat:
                continue

            self.nodes.append(set())

            for _ in range(m):
                if not probability_flat:
                    break

                connected_node = choice(probability_flat)

                self.nodes[new_node].add(connected_node)
                self.nodes[connected_node].add(new_node)

                probability_flat = list(filter(
                    lambda v: v != connected_node, probability_flat))

    def node_size(self):
        return len(self.nodes)

    def edge_size(self):
        return reduce(lambda acc, v: acc + len(v), self.nodes, 0) // 2

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            print(f'{self.node_size()} {self.edge_size()}', file=f)
            for n in range(len(self.nodes)):
                for neighbour in self.nodes[n]:
                    if n < neighbour:
                        print(f'{n} {neighbour}', file=f)


ba = BA_Graph()

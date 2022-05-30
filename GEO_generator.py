from random import randint
from functools import reduce


class GEO_Graph:
    def __init__(self, interactive=True):
        self.nodes = {}
        self.homomorphism = {}
        if interactive:
            print('This is Random geometric graph generator')
            user_input = input(
                'Enter 4 parameters:\n- Node size\n- Radius\n- Range\n- Output file name\n')

            parameters = user_input.split()
            if len(parameters) < 4:
                exit('Enter all 4 parameters')
            n, radius, range, file_name = parameters

            n_int = int(n)
            if n_int < 10:
                exit('Node size must be greater than 9')

            radius_int = int(radius)
            if radius_int < 2:
                exit('Radius must be greater than 1')

            range_int = int(range)
            if range_int < 200:
                exit('Range size must be greater than 199')

            self.generate(n_int, radius_int, range_int)
            self.save_to_file(file_name)

    def generate(self, n, radius=10, range=200):
        self.radius = radius
        self.range = range
        default_vertex = (self.range // 2, self.range // 2)
        self.nodes = {default_vertex: set()}
        self.homomorphism = {default_vertex: 0}

        # loop
        while self.node_size() < n:
            x = randint(0, self.range)
            y = randint(0, self.range)

            if (x, y) in self.nodes:
                continue

            new_vertex = set()
            for vertex in self.nodes:
                d = ((x - vertex[0]) ** 2 + (y - vertex[1]) ** 2) ** (1/2)
                if d < self.radius:
                    new_vertex.add((vertex[0], vertex[1]))
                    self.nodes[(vertex[0], vertex[1])].add((x, y))
            if new_vertex:
                self.nodes[(x, y)] = new_vertex
                self.homomorphism[(x, y)] = len(self.nodes)

    def node_size(self):
        return len(self.nodes)

    def edge_size(self):
        return reduce(lambda acc, v: acc + len(self.nodes[v]), self.nodes, 0) // 2

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            print(f'{self.node_size()} {self.edge_size()}', file=f)
            for vertex in self.nodes:
                for neighbour in self.nodes[vertex]:
                    v = self.homomorphism[vertex]
                    n = self.homomorphism[neighbour]
                    if v < n:
                        print(f'{v} {n}', file=f)


# interactive mode
# geo = GEO_Graph()


# seed mode
geo = GEO_Graph(False)

max_range = 200
n = 100
r = [2, 5, 8]

for rr in r:
    for i in range(10):
        geo.generate(n, rr, max_range)
        geo.save_to_file(f'geo_n{n}_e{n*rr}_{i}.in.txt')

from random import randrange, randint
from functools import reduce


class ER_Graph:
    def __init__(self, interactive=True, probability=30):
        self.nodes = []
        self.probability = probability
        if interactive:
            print('This is Erdős–Rényi-star-augmented generator')
            user_input = input(
                'Enter 3 parameters:\n- Node size\n- Edge size\n- Output file name\n')

            parameters = user_input.split()
            if len(parameters) < 3:
                exit('Enter all 3 parameters')
            n, e, file_name = parameters

            n_int = int(n)
            if n_int < 10:
                exit('Node size must be greater than 9')

            e_int = int(e)
            if e_int < 20:
                exit('Edge size must be greater than 19')

            self.generate(n_int, e_int)
            self.save_to_file(file_name)

    def generate(self, n, e):
        # augmented initialization with star, so that graph is always connected
        self.nodes = [set() for _ in range(n)]
        for v in range(1, n):
            self.nodes[0].add(v)
            self.nodes[v].add(0)

        # loop
        while self.edge_size() < e:
            u = randrange(0, n)
            v = randrange(0, n)

            if u == v:
                continue

            p = randint(0, 100)
            if p > self.probability:
                self.nodes[u].add(v)
                self.nodes[v].add(u)

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


# interactive mode
# er = ER_Graph()


# seed mode
er = ER_Graph(False)

n = 100
e = [200, 500, 800]

for ee in e:
    for i in range(10):
        er.generate(n, ee)
        er.save_to_file(f'er_n{n}_e{ee}_{i}.in.txt')

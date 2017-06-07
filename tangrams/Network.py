import numpy as np
import copy
from tangrams.Setup import Setup
INHIBITORY = -1.1
EXCITATORY = 1.0
HEBB = 1.0
STABLE = 10
T_INIT = 1
ETA_INIT = 1


class Network:

    def __init__(self):
        self.nodes = [] # list of nodes/pieces
        self.n = 0      # number of nodes
        self.a = []     # vector of activations
        self.solution = [] # proposed solution
        self.w = []     # weight matrix
        self.input = [] # input matrix
        self.T = T_INIT    # temperature
        self.dT = 0.99   # scheduling
        self.iter = 0   # iteration of dynamics
        self.opt_iter = 10.0    # optimal iteration number
        self.e = []     # energy during run
        self.hebb = []  # hebbian learning
        self.eta = ETA_INIT  # learning rate
        self.deta = 1.0 # scheduling
        self.p_base = [] # list of basic pieces the network can use

    def print_me(self):
        print("nodes: " + str(self.n))
        print(self.w)

    def set_network(self, task):
        p_base = Setup.base()
        self.p_base = p_base
        nodes = []
        for p in p_base:
            p_list = p.rotate()
            for q in p_list:
                nodes.extend(q.translate(task.I, task.J))
        self.set_nodes(nodes)

    def set_small_triangle_network(self, task):
        # initialize the network with only one small triangle. This is the starting base for learning.
        # the task is used only for its size.
        p_base = Setup.base()
        triangle = p_base[0] #the first element is small triangle
        nodes = []
        nodes.extend(triangle.translate(task.I, task.J))
        self.set_nodes(nodes)

    def set_partial_network(self, task):
        # set the nodes to be pieces from the task's solution with all translations but without rotations
        piece_list = copy.deepcopy(task.solution)
        for p in piece_list:
            p.x = p.base()
        p_base = piece_list
        self.p_base = p_base
        nodes = []
        for p in p_base:
            nodes.extend(p.translate(task.I, task.J))
        self.set_nodes(nodes)

    def set_available_pieces(self, task):
        # set the nodes to be pieces from the task's solution with all translations and rotations
        piece_list = copy.deepcopy(task.solution)
        for p in piece_list:
            p.x = p.base()
        p_base = piece_list
        self.p_base = p_base
        nodes = []
        for p in p_base:
            p_list = p.rotate()
            for q in p_list:
                nodes.extend(q.translate(task.I, task.J))
        self.set_nodes(nodes)

    def extend_partial_network(self, task):
        # add new pieces or new rotations to p_base
        new_piece_list = copy.deepcopy(task.solution)
        for n_p in new_piece_list:
            exist = False
            for q in self.p_base:
                if n_p.name[0]==q.name[0] and n_p.name[1]==q.name[1]:
                    exist = True
            if exist == False:
                self.p_base.append(n_p)
        nodes = []
        for p in self.p_base:
            p.x = p.base()
            nodes.extend(p.translate(task.I, task.J))
        self.set_nodes(nodes)




    def init_parameters(self):
        self.T = T_INIT    # temperature
        self.eta = ETA_INIT  # learning rate
        self.iter = 0.0
        self.update_scheduling()

    def set_nodes(self, nodes):
        self.nodes = copy.deepcopy(nodes)
        self.n = len(self.nodes)
        self.a = np.zeros(self.n)
        self.w = np.zeros([self.n, self.n])
        self.input = np.zeros(self.n)
        # if len(self.hebb) == 0:
        #     self.hebb = np.zeros([self.n, self.n])
        self.hebb = np.zeros([self.n, self.n])

    def init_network(self):
        for n in self.nodes:
            n.G = np.sum(n.x > 0)

        for n1 in range(0,self.n):
            for n2 in range(0,self.n):
                if not n1==n2:
                    # winner-takes-all, same piece
                    if self.nodes[n1].name[0] == self.nodes[n2].name[0]:
                        self.w[n1, n2] = INHIBITORY

                    # overlapping configurations
                    if self.nodes[n1].overlap(self.nodes[n2]):
                        self.w[n1, n2] = INHIBITORY
        self.e = []

    def find(self, name):
        for t in self.nodes:
            if name[0] == t.name[0] and name[1] == t.name[1] and name[2] == t.name[2]:
                return t
        return None

    def add_task(self, task):
        for i in range(0, self.n):
            x = self.nodes[i].x * task.x
            self.input[i] = EXCITATORY * np.sum(x > 0) / self.nodes[i].G

    def dynamics(self):
        # one time step, updating all neurons

        # excitatory from input
        exc = self.input
        # lateral inhibition
        inh = self.inhibition()

        # sequence of neurons to update
        perm = np.random.permutation(self.n)
        # updating all neurons, asynchronously
        for i in perm:
            prev_a = self.a[i]
            if exc[i] < 1:
                self.a[i] = 0
            else:
                if inh[i] > -0.01:
                    self.a[i] = 1
                else:
                    h = exc[i] + inh[i]
                    p = 1.0 / (1.0 + np.exp(-h/self.T))
                    if np.random.uniform() < p:
                        self.a[i] = 1
                    else:
                        self.a[i] = 0
            if self.a[i] != prev_a:
                inh = self.inhibition()

        self.update_scheduling()
        return self.a, self.energy()

    def inhibition(self):
        return np.dot(self.w + self.eta * self.hebb, self.a)

    def update_scheduling(self):
        self.iter += 1.0
        if self.iter <= self.opt_iter:
            self.T = T_INIT * (self.iter / self.opt_iter)
        else:
            self.T *= self.dT
                #T_INIT * (self.iter / self.opt_iter) * np.exp(1.0 - (self.iter / self.opt_iter))
        # print('T:', self.T)
        # self.T *= self.dT
        self.eta *= self.deta

    def energy(self):
        exc = self.input
        inh = np.dot(self.w, self.a)
        return -np.dot(self.a, inh + exc)

    def get_solution(self):
        self.sol_list = []
        self.solution = np.zeros(self.nodes[0].x.shape)
        for i in range(0, self.n):
            if self.a[i] > 0:
                self.sol_list.append(self.nodes[i])
                self.solution += self.nodes[i].x
        return self.solution, self.sol_list

    def get_solution_pieces(self):
        # returns a list of the pieces in the solution
        l_sol = []
        for i in range(0, self.n):
            if self.a[i] > 0:
                l_sol.append(self.nodes[i])
        return l_sol

    def print_active(self):
        for n in range(0,self.n):
            if self.a[n] > 0:
                self.nodes[n].print_me()

    def run(self, task, duration):
        # run a specific task for a specific duration
        self.init_network()
        self.add_task(task)
        for t in range(0, duration):
            self.dynamics()
            if self.stop_criteria():
                break
        return self.e

    def stop_criteria(self):
        self.e.append(self.energy())
        t = len(self.e)
        if t > STABLE:
            es = list(self.e[t-STABLE:t])
            if es.count(es[0]) == len(es):
                self.e = self.e[:t]
                return True
        return False

    # for learning
    def decompose(self):
        active = np.where(self.a > 0)[0]
        structures = []
        for i in range(0, len(active)):
            a_i = active[i]
            for j in range(i+1, len(active)):
                a_j = active[j]
                if self.nodes[a_i].touch(self.nodes[a_j]):
                    structures.append(self.nodes[a_i].unite(self.nodes[a_j]).base())
        return structures

    def add_hebbian(self, structures):
        for n1 in range(0,self.n):
            for n2 in range(0,self.n):
                if self.nodes[n1].touch(self.nodes[n2]):
                    base = self.nodes[n1].unite(self.nodes[n2]).base()
                    for s in structures:
                        if np.array_equal(s, base):
                            self.hebb[n1, n2] = HEBB


    def set_activation(self, a):
        self.a = copy.deepcopy(a)

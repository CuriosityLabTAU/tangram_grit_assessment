from tangrams import Piece
from tangrams import Setup

import copy
import numpy as np
import random
import json
# import matplotlib.pyplot as plt


class Task:
    I = 3
    J = 3
    name = ''

    def __init__(self):
        self.x = np.zeros([self.I, self.J])
        self.solution = []

    def set_size(self, i, j):
        self.I = 1 + (i-1) * Piece.JUMP
        self.J = 1 + (j-1) * Piece.JUMP
        self.x = np.zeros([self.I, self.J])

    def set_shape(self, t_list):
        self.I = t_list[0].x.shape[0]
        self.J = t_list[0].x.shape[1]
        self.x = np.zeros([self.I,self.J])
        self.solution = copy.deepcopy(t_list)

        for t in t_list:
            self.x += t.x

    def print_me(self):
        print(self.name + "(" + str(self.get_difficulty()) + ")")
        print(self.x)

    def print_solution(self):
        sol = ''
        for s in self.solution:
            sol += str(s.name) + ", "
        print(sol)

    def show(self, temp_x = None):
        if temp_x is None:
            temp_x = self.x
        img_x1 = copy.deepcopy(temp_x)
        img_x2 = copy.deepcopy(temp_x)
        img_x1[img_x1 > 1] = 1
        img_x2[img_x2 < 5] = 0
        # plt.imshow(img_x1 + img_x2, interpolation='none')
        # plt.show()

    def decompose(self):
        structures = []
        for s1 in self.solution:
            for s2 in self.solution:
                if ~np.array_equal(s1.x, s2.x):
                    if s1.touch(s2):
                        structures.append(s1.unite(s2).base())
        return structures

    def check_solution(self, sol, sol_list):
        # sol is the x matrix of the checked solution and sol_list is the list of pieces of the checked solution
        # the target solution is the self task.

        #check that a piece is not used more than once (requires the piece's name to be unique)
        names_list = []
        for i in range(0,len(sol_list)):
            names_list.append(sol_list[i].name[0])
        if len(names_list) != len(set(names_list)): # check that the list is unique
            return False
        if len(np.where(sol > 5)[0]) > 0: # the proposed solution is not a solution
            return False
        task_x = np.clip(self.x, 0, 1)
        sol_x = np.clip(sol, 0, 1)
        return np.array_equal(task_x, sol_x)


    def number_of_connections(self, x = None):
        if x is None:
            x = self.x
        values, counts = np.unique(x, return_index=True)#return_counts=True)
        connections_1 = counts[np.where(values > 1)]
        connections_2 = counts[np.where(values > 4)]
        if len(connections_1) == 0:
            return 0
        return np.sum(connections_1) - np.sum(connections_2[0])

    def random_task(self, net, number_pieces=None):
        # permute base pieces
        p_base = Setup.base()
        order = np.random.permutation(len(p_base))

        if not number_pieces:
            number_pieces = len(p_base)

        t_list = []
        temp_x = copy.deepcopy(self.x)

        for t_iter in range(0, number_pieces):             # go over all the pieces
            p_shape = p_base[order[t_iter]]               # get the next piece
            p_rotate = random.choice(p_shape.rotate())    # get a random possible rotation
            p_pos = np.array([self.I - 1, self.J - 1]) / Piece.JUMP                # start from farthest corner

            temp_connections = self.number_of_connections(temp_x)
            new_connections = self.number_of_connections(temp_x)
            new_pos = p_pos
            temp_x_p = copy.deepcopy(temp_x)
            move = np.array([0, 0])
            overlap = len(np.where(temp_x_p > 5)[0])
            while temp_connections == new_connections and overlap == 0:
                temp_x_p = copy.deepcopy(temp_x)
                choices = []
                if new_pos[0] > 0:
                    choices.append([-1,0])
                if new_pos[1] > 0:
                    choices.append([0,-1])
                if len(choices) == 0:
                    break
                move += np.array(random.choice(choices)) # move one in random direction (up or left)
                new_pos = p_pos + move
                if new_pos[0] < 0 or new_pos[1] < 0:
                    break
                p_name = [p_shape.name[0],
                          p_rotate.name[1],
                          str(p_pos[0] + move[0]) + " " + str(p_pos[1] + move[1])]
                p = net.find(p_name)
                if p is not None:
                    temp_x_p += p.x
                    new_connections = self.number_of_connections(temp_x_p)
                    overlap = len(np.where(temp_x_p > 5)[0])
            if p is not None and overlap == 0:
                new_p = copy.deepcopy(p)
                temp_x += new_p.x
                t_list.append(new_p)
        self.x = temp_x
        self.solution = copy.deepcopy(t_list)

    def get_difficulty(self):
        # connections are never more than 22.0
        return (self.number_of_connections() - 2.0) / (31.0 - 2.0)

    def save_png(self):
        filename = self.name + ".png"
        bare = np.uint8(copy.deepcopy(self.x))
        bare[bare>0] = 128
        s = bare.shape
        img = np.zeros((s[0], s[1], 4), 'uint8')
        img[0:s[0],0:s[1],0] = bare
        img[0:s[0],0:s[1],1] = bare
        img[0:s[0],0:s[1],2] = bare
        img[0:s[0],0:s[1],3] = bare
        Piece().to_image(img).save(filename, 'png')

    def create_from_json(self, json_str):
        # create a task from a json string
        # for example:
        # dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        # json_str = json.dumps(dict)

        task_dict = json.loads(json_str)
        size_i = int(task_dict['size'].split()[0])
        size_j = int(task_dict['size'].split()[1])
        self.set_size(size_i, size_j)
        self.solution = []
        for n in range(len(task_dict['pieces'])):
            name = task_dict['pieces'][n][0]
            rot = task_dict['pieces'][n][1]
            pos = task_dict['pieces'][n][2]
            pos_i = pos.split()[0]
            pos_j = pos.split()[1]
            # check that pos is not fractional and that it is in board boundaries
            if np.floor(float(pos_i)) == float(pos_i) and np.ceil(float(pos_i)) == float(pos_i) \
                    and np.floor(float(pos_j)) == float(pos_j) and np.ceil(float(pos_j)) == float(pos_j) \
                    and 0 <= int(float(pos_i)) <= size_i - 2 and 0 <= int(float(pos_j)) <= size_j - 2 \
                    and (('small triangle' in name) # assert that the shapes are within the board boundaries
                         or ('square' in name)
                         or ('large triangle' in name and int(float(pos_i)) <= size_i - 3 and int(
                            float(pos_j)) <= size_j - 3)
                         or (('medium triangle' in name) and (rot == '0' or rot == '180') and int(
                            float(pos_j)) <= size_j - 3)
                         or (('medium triangle' in name) and (rot == '90' or rot == '270') and int(
                            float(pos_i)) <= size_i - 3)
                         or (('parrallelogram' in name) and (rot == '0' or rot == '180') and int(
                            float(pos_i)) <= size_i - 3)
                         or (('parrallelogram' in name) and (rot == '90' or rot == '270') and int(
                            float(pos_j)) <= size_j - 3)):
                p = Piece()
                p.create(name,rot,[int(float(pos_i)), int(float(pos_j))])
                x_temp = np.zeros([self.I, self.J])
                x_temp[0:p.x.shape[0], 0:p.x.shape[1]] = p.x
                p.x = copy.deepcopy(x_temp)
                self.solution.append(p)
                self.x += p.x

    def export_to_json(self):
        # convert Task to json_string
        task_dict = {}
        (I, J) = self.x.shape
        task_dict['size'] = str((I - 1) / Piece.JUMP + 1) + ' ' + str((J - 1) / Piece.JUMP + 1)
        pieces_vec = []
        for p in self.solution:
            pieces_vec.append((p.name[0], p.name[1], p.name[2]))
        task_dict['pieces'] = pieces_vec
        return json.dumps(task_dict)

    def transfer_json_to_json_initial_pos(self, json_str):
        # transfer a json string of a task to a json string with pieces at initial positions
        task_dict = json.loads(json_str)
        init_dict = {}
        piece_init_vec = []
        init_dict['size'] = task_dict['size']
        for n in range(len(task_dict['pieces'])):
            name = task_dict['pieces'][n][0]
            rot = '0' # task_dict['pieces'][n][1]
            pos = task_dict['pieces'][n][2]
            #init_pos = str(5)+' '+str(3*n-4)
            init_pos = str(-3) + ' ' + str(2 * n - 4) #rinat
            #if n < 4:  # first 4 pieces on the right
            #    init_pos = str(2 * (n)-0.5) + ' ' + str(+5 + (n%2))
            #else:  # rest of pieces on the left
            #    init_pos = str(2 * (n-4)-0.5) + ' ' + str(-3 + (n%2))
            piece_init_vec.append((name,rot,init_pos))
            init_dict['pieces'] = piece_init_vec
        init_json = json.dumps(init_dict)
        return init_json




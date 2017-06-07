from tangrams import *
import numpy as np
import copy
# import matplotlib.pyplot as plt
import json


class Solver:

    n_networks = 10
    efficiency = 1.0

    def __init__(self):
        self.networks = []
        self.learned = []
        self.solutions = []
        self.errors = []
        self.solved_network_index = None
        self.available_pieces = None

        for i in range(0, self.n_networks):
            self.networks.append(Network())
            self.solutions.append([])
            self.errors.append([])

    def set_initial_task(self, task):
        # initialize networks with the current task and efficient
        for net in self.networks:
            net.set_network(task)
            net.init_network()

    def set_blank_solver(self, task):
        # initialize networks with the size of task, and one only small triangle
        for net in self.networks:
            net.set_small_triangle_network(task)
            net.init_network()

    def set_available_pieces(self, task):
        # initialize networks with pieces in task (with all translations and rotations)
        self.available_pieces = copy.deepcopy(task)  #
        for net in self.networks:
            net.set_available_pieces(task)
            net.init_network()

    def run_task(self, task, duration=100, stop=False, init_network=False):
        # stop  -   whether to stop when a correct solution is found
        # return-   network that solved and time it took to solve

        # initialize networks with the current task and efficient

        self.solved_network_index = None #  if solved_network_index remains None then no network solved the task

        for net in self.networks:
            if init_network:
                net.set_network(task)
                net.init_network()
            net.init_parameters()
            net.add_task(task)

        # initialize the solutions and errors
        # these are [i,t], i.e. networks X duration
        for i in range(0, self.n_networks):
            self.solutions[i] = []
            self.errors[i] = []

        # run the task for the given duration
        for t in range(0, duration):
            # efficiency means probability of actual progressing
            if np.random.rand() < self.efficiency:
                # go over all the networks
                for i in range(0, self.n_networks):
                    # run one time-step
                    s_ti, e_ti = self.networks[i].dynamics()
                    # update the solutions and errors with the current ones
                    s_ti_copy = copy.deepcopy(s_ti) # create a copy since s_ti is a pointer to the network's activation
                    self.solutions[i].append(s_ti_copy)
                    self.errors[i].append(e_ti)

                if stop is not False:
                    for i in range(0, self.n_networks):
                        x, sol_list = self.networks[i].get_solution()
                        if task.check_solution(x, sol_list):
                            # return the networked that solved and the time it took to solve
                            self.solved_network_index = i
                            return self.networks[i], t+1
        return None, None

    def get_seq_of_moves(self):
        # return a list, such that each element in the list is a json string of the board pieces
        # should be called after run_task()
        seq = []
        if self.solved_network_index is not None:
            n = self.solved_network_index
            print 'Solver: puzzle solved'
        else:
            n = 0 # none of the networks solved so just choose the first network
            print 'Solver: puzzle not solved'
        print len(self.solutions[n])
        for k in range(len(self.solutions[n])-2, len(self.solutions[n])):
            for i in range(len(self.solutions[n][k])):
                if self.solutions[n][k][i] > 0:
                    seq.append(self.networks[n].nodes[i])

        # return seq
        # convert seq to json of list of board pieces jsons
        # seq_dict = {}
        # (I, J) = self.networks[0].nodes[0].x.shape
        # seq_dict['size'] = str((I - 1) / Piece.JUMP + 1) + ' ' + str((J - 1) / Piece.JUMP + 1)
        # pieces_vec = []
        # for p in seq:
        #     pieces_vec.append((p.name[0], p.name[1], p.name[2]))
        # seq_dict['pieces'] = pieces_vec

        seq_jsons = []
        temp_json = self.available_pieces.export_to_json()
        init_pos_json = self.available_pieces.transfer_json_to_json_initial_pos(temp_json)
        seq_jsons.append(init_pos_json)

        task_dict = json.loads(init_pos_json)
        pieces_vec = task_dict['pieces']
        size = task_dict['size']
        for p in seq:
            for n in range(len(pieces_vec)):
                if p.name[0] == pieces_vec[n][0]:
                    if p.name[1] == pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]:  # check if rotation and position are the same as in previous configuration
                        pass
                    elif (p.name[1] != pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]) \
                            or (p.name[1] == pieces_vec[n][1] and p.name[2] != pieces_vec[n][2]):  # only rotation or only position has changed
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                    else:  # both rotation and position have changed. split the move to position change and rotation change
                        pieces_vec[n] = (p.name[0], pieces_vec[n][1], p.name[2])   # change position
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])  # change rotation
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
        return seq_jsons
        #  return json.dumps(seq_dict)

    def get_seq_of_moves_v2(self, available_pieces):
        # return a list, such that each element in the list is a json string of the board pieces
        # should be called after run_task()
        seq = []
        temp_json = available_pieces.export_to_json()
        init_pos_json = available_pieces.transfer_json_to_json_initial_pos(temp_json)
        task_dict = json.loads(init_pos_json)
        pieces_vec = task_dict['pieces']

        if self.solved_network_index is not None:
            net_ind = self.solved_network_index
            print 'Solver: puzzle solved'
        else:
            net_ind = 0 # none of the networks solved so just choose the first network
            print 'Solver: puzzle not solved'
        print len(self.solutions[net_ind])
        # for k in range(len(self.solutions[net_ind])-2, len(self.solutions[net_ind])):
        #     for i in range(len(self.solutions[net_ind][k])):
        #         if self.solutions[net_ind][k][i] > 0:
        #             seq.append(self.networks[net_ind].nodes[i])

        # Choose the most active node (unless it was already chosen) in each iteration.
        for n in range(len(self.solutions[net_ind])):

            v = np.add(np.dot(self.networks[net_ind].w, self.solutions[net_ind][n]), self.networks[net_ind].input)
            # ADD exp stuff
            temp = copy.deepcopy(self.solutions[net_ind][n])
            ind_active = np.where(self.solutions[net_ind][n])
            # ind_max = np.where(v[ind_active] == max(v[ind_active]))
            ind_max_sorted = [x for (y, x) in sorted(zip(v[ind_active], ind_active[0]),
                                                     reverse=True)]  # sort the active indexes according to v()

            most_active_piece = self.networks[net_ind].nodes[ind_max_sorted[0]].name
            for k in range(len(ind_max_sorted)):
                most_active_piece = self.networks[net_ind].nodes[ind_max_sorted[k]].name
                if most_active_piece not in pieces_vec \
                        and v[ind_max_sorted[k]] > 0.0 \
                        and self.errors[net_ind][n] < 0.0:
                    print(self.errors[net_ind][n])
                    seq.append(self.networks[net_ind].nodes[ind_max_sorted[k]])
                    for piece_iter in range(len(pieces_vec)):
                        if pieces_vec[piece_iter][0] == most_active_piece[0]:  # the name is the same.
                            pieces_vec[piece_iter] = most_active_piece
                    break

        # add pieces from final solution in case they where not included in the most active list
        for k in range(len(self.solutions[net_ind][-1])):
            if self.solutions[net_ind][-1][k] == 1:
                seq.append(self.networks[net_ind].nodes[k])


        # return seq
        # convert seq to json of list of board pieces jsons
        # seq_dict = {}
        # (I, J) = self.networks[0].nodes[0].x.shape
        # seq_dict['size'] = str((I - 1) / Piece.JUMP + 1) + ' ' + str((J - 1) / Piece.JUMP + 1)
        # pieces_vec = []
        # for p in seq:
        #     pieces_vec.append((p.name[0], p.name[1], p.name[2]))
        # seq_dict['pieces'] = pieces_vec

        seq_jsons = []
        temp_json = available_pieces.export_to_json()
        init_pos_json = available_pieces.transfer_json_to_json_initial_pos(temp_json)
        seq_jsons.append(init_pos_json)

        task_dict = json.loads(init_pos_json)
        pieces_vec = task_dict['pieces']
        pieces_vec_initial = copy.deepcopy(pieces_vec)
        size = task_dict['size']
        for p in seq:
            for n in range(len(pieces_vec)):
                if p.name[0] == pieces_vec[n][0]:
                    if p.name[1] == pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]:  # check if rotation and position are the same as in previous configuration
                        pass
                    elif (p.name[1] != pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]) \
                            or (p.name[1] == pieces_vec[n][1] and p.name[2] != pieces_vec[n][2]):  # only rotation or only position has changed
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                    else:  # both rotation and position have changed. split the move to position change and rotation change
                        pieces_vec[n] = (p.name[0], pieces_vec[n][1], p.name[2])   # change position
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])  # change rotation
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))

        # move unused pieces to initial position
        # create dictionary from piece name to node number in network
        dic = {}
        for m in range(len(self.networks[0].nodes)):
            dic[self.networks[0].nodes[m].name[0] + ' ' + self.networks[0].nodes[m].name[1] + ' ' +
                self.networks[0].nodes[m].name[2]] = m
        for k in range(len(task_dict['pieces'])):
            key = task_dict['pieces'][k][0]+' '+task_dict['pieces'][k][1]+' '+task_dict['pieces'][k][2]
            if key in dic:
                node_num = dic[key]
                if self.solutions[net_ind][-1][node_num] == 0: # piece should be removed from the board
                    task_dict['pieces'][k] = pieces_vec_initial[k]
                    seq_jsons.append(json.dumps(task_dict))

        return seq_jsons
        #  return json.dumps(seq_dict)

    def get_seq_of_random_moves(self, task, seq_len):
        # return a list, such that each element in the list is a json string of the board pieces chosen randomly but with intersection with task's shadow.
        # should be called after run_task()
        seq = []
        n = 0  # choose the first network
        rnd_perm = np.random.permutation(self.networks[n].n)
        for i in rnd_perm[0:seq_len]:
            if self.networks[n].nodes[i].overlap(task):
                seq.append(self.networks[n].nodes[i])
        # return seq
        # convert seq to json of list of board pieces jsons
        seq_dict = {}
        (I, J) = self.networks[0].nodes[0].x.shape
        seq_dict['size'] = str((I - 1) / Piece.JUMP + 1) + ' ' + str((J - 1) / Piece.JUMP + 1)
        pieces_vec = []
        for p in seq:
            pieces_vec.append((p.name[0], p.name[1], p.name[2]))
        seq_dict['pieces'] = pieces_vec

        seq_jsons = []
        temp_json = self.available_pieces.export_to_json()
        init_pos_json = self.available_pieces.transfer_json_to_json_initial_pos(temp_json)
        seq_jsons.append(init_pos_json)

        task_dict = json.loads(init_pos_json)
        pieces_vec = task_dict['pieces']
        size = task_dict['size']
        for p in seq:
            for n in range(len(pieces_vec)):
                if p.name[0] == pieces_vec[n][0]:
                    if p.name[1] == pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]:  # check if rotation and position are the same as in previous configuration
                        pass
                    elif (p.name[1] != pieces_vec[n][1] and p.name[2] == pieces_vec[n][2]) \
                            or (p.name[1] == pieces_vec[n][1] and p.name[2] != pieces_vec[n][2]):  # only rotation or only position has changed
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                    else:  # both rotation and position have changed. split the move to position change and rotation change
                        pieces_vec[n] = (p.name[0], pieces_vec[n][1], p.name[2])   # change position
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
                        pieces_vec[n] = (p.name[0], p.name[1], p.name[2])  # change rotation
                        task_dict['pieces'] = pieces_vec
                        seq_jsons.append(json.dumps(task_dict))
        return seq_jsons
        #  return json.dumps(seq_dict)

    def print_current_solutions(self):
        for i in range(0, self.n_networks):
            print(self.solutions[i][-1])
        for i in range(0, self.n_networks):
            print(self.errors[i][-1])

    def analyze_stats(self, show=False):
        # return the error statistics
        duration = len(self.errors[0])
        d = range(0, duration)
        error = np.zeros(self.n_networks)
        avg_error = np.zeros(duration)
        std_error = np.zeros(duration)
        min_error = np.zeros(duration)

        # go over all the time-steps
        for t in d:
            for i in range(0, self.n_networks):
                error[i] = self.errors[i][t]
            if t == d[-1] and t > 0:
                #print('Networks errors: ', error)
                pass
            avg_error[t] = np.average(error)
            std_error[t] = np.std(error)
            min_error[t] = np.min(error)

        if show:
            pass
            # fig, ax = plt.subplots()
            # ax.errorbar(d, avg_error, yerr=std_error)
            # ax.plot(d, min_error, 'r')
            # plt.axis([d[0], d[-1], -5.5, 10])
            # plt.draw()
            # plt.show()

        if duration == 1:   # return numbers, not arrays
            return avg_error[0], std_error[0], min_error[0]
        else:               # return arrays
            return avg_error, std_error, min_error

    # def learn(self, task):
    #     structures = task.decompose()
    #     for net in self.networks:
    #         net.add_hebbian(structures)

    def learn(self, task):
        for net in self.networks:
            net.extend_partial_network(task)
            net.init_network()

    def evaluate_tasks(self, tasks, duration=100, stop=False):
        times = np.zeros(len(tasks))
        for t in range(0, len(tasks)):
            pass

    def set_activation(self, activation):
        for net in self.networks:
            net.set_activation(activation)

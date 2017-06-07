from tangrams import *
import json
import numpy as np
#import matplotlib.pyplot as plt


class SelectionGenerator:

    def __init__(self):
        self.N_dif_levels = 8  # This value is overridden in load_dif_levels(),
        self.max_level = 6
        self.challenge_index = 9 # column number of the challenge level (zero based)
        self.challenge_counter = 0 # counts the challenges
        self.dif_level = []
        self.dif_indexes = np.zeros([self.N_dif_levels], dtype=np.int)
        self.current_level = 2
        for n in range(self.N_dif_levels):
            self.dif_level.append([])

    def load_dif_levels(self, filename='dif1'):
        # read tangrams for each difficulty from tangram_levels.txt
        # file format is:
        #  dif 0
        # {"pieces": [["square", "90", "1 1"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # {"pieces": [["square", "180", "0 0"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # dif 1
        # {"pieces": [["square", "180", "0 0"], ["small triangle2", "180", "0 1"]], "size": "5 5"}
        # ...
        #
        dif_i = -1
        self.dif_level = []
        with open('./game_facilitator/tangram_levels_' + filename + '.txt','r') as fp:
            for line in fp:
                if 'dif' in line:
                    dif_i += 1
                    self.dif_level.append([])
                else:
                    self.dif_level[dif_i].append(line.strip('\n'))
        self.N_dif_levels = dif_i + 1
        self.dif_indexes = np.zeros([self.N_dif_levels], dtype=np.int)



    def get_current_selection(self):
        # return three json_strings
        temp_task = Task()
        T1 = self.dif_level[self.current_level-1][self.dif_indexes[self.current_level-1]]
        T1_init_pos = temp_task.transfer_json_to_json_initial_pos(T1)
        T2 = self.dif_level[self.current_level][self.dif_indexes[self.current_level]]
        T2_init_pos = temp_task.transfer_json_to_json_initial_pos(T2)
        T3 = self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]]
        T3_init_pos = temp_task.transfer_json_to_json_initial_pos(T3)
        return [[T1, T1_init_pos], [T2, T2_init_pos], [T3, T3_init_pos]]

    def update_game_result(self, player, user_selection, game_result):
        # update the selection generator according to user selection and game result
        # player is 'Robot' or 'Child'
        # user_selection is 0/1/2
        # game_result is 'S' or 'F'

        self.dif_indexes[self.current_level - 1] += 1
        self.dif_indexes[self.current_level] += 1
        self.dif_indexes[self.current_level + 1] += 1

        if player == 'Child':
            if game_result == 'F':
                if user_selection == 0:
                    self.current_level -= 1
                    if self.current_level == 0:
                        self.current_level = 1
            elif game_result == 'S':
                self.current_level += 1
                if self.current_level == self.max_level+1:
                    self.current_level = self.max_level
        elif player == 'Robot':
            pass # The current level is not changed if the robot played

    def get_challenge_selection(self):
        # return three json_strings of special challenge level. The challenge tangrams are on the last column
        temp_task = Task()
        T1 = self.dif_level[self.challenge_index-1][self.challenge_counter]
        T1_init_pos = temp_task.transfer_json_to_json_initial_pos(T1)
        T2 = self.dif_level[self.challenge_index][self.challenge_counter]
        T2_init_pos = temp_task.transfer_json_to_json_initial_pos(T2)
        T3 = self.dif_level[self.challenge_index+1][self.challenge_counter]
        T3_init_pos = temp_task.transfer_json_to_json_initial_pos(T3)

        self.challenge_counter += 1
        return [[T1, T1_init_pos], [T2, T2_init_pos], [T3, T3_init_pos]]

    # def display(self):
    #     plt.figure()
    #     task = Task()
    #     num_of_rows = max(len(l) for l in self.dif_level)  # find the maximal length of all sub lists in dif_level
    #     for n in range(self.N_dif_levels):
    #         for k in range(len(self.dif_level[n])):
    #             plt.subplot(num_of_rows,self.N_dif_levels, n+1+k*self.N_dif_levels)
    #             task.create_from_json(self.dif_level[n][k])
    #             if k < self.dif_indexes[n]:
    #                 plt.imshow(task.x*-1, interpolation='none')
    #                 plt.axis('off')
    #             else:
    #                 plt.imshow(task.x, interpolation='none')
    #                 plt.axis('off')
    #     plt.subplot(num_of_rows,self.N_dif_levels,
    #                 self.current_level-1+1+(self.dif_indexes[self.current_level - 1])*self.N_dif_levels)
    #     task.create_from_json(self.dif_level[self.current_level-1][self.dif_indexes[self.current_level - 1]])
    #     plt.imshow(np.sin(task.x), interpolation='none')
    #     plt.axis('off')
    #     plt.subplot(num_of_rows, self.N_dif_levels,
    #                 self.current_level  + 1 + (self.dif_indexes[self.current_level]) * self.N_dif_levels)
    #     task.create_from_json(self.dif_level[self.current_level ][self.dif_indexes[self.current_level ]])
    #     plt.imshow(np.sin(task.x), interpolation='none')
    #     plt.axis('off')
    #     plt.subplot(num_of_rows, self.N_dif_levels,
    #                 self.current_level + 1 + 1 + (self.dif_indexes[self.current_level + 1]) * self.N_dif_levels)
    #     task.create_from_json(self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]])
    #     plt.imshow(np.sin(task.x), interpolation='none')
    #     plt.axis('off')
                # T1 = self.dif_level[self.current_level - 1][self.dif_indexes[self.current_level - 1]]
                # T2 = self.dif_level[self.current_level][self.dif_indexes[self.current_level]]
                # T3 = self.dif_level[self.current_level + 1][self.dif_indexes[self.current_level + 1]]



# task_dic =  {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
# json_str = json.dumps(task_dic)
# dif_level[0].append(json_str)
#
# task_dic =  {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
# json_str = json.dumps(task_dic)
# dif_level[0].append(json_str)



#
# task = Task()
# task.create_from_json(json_str)
#
#
# task_dic =  {'size': '5 5', 'pieces': [('square', '0', '1 1'), ('small triangle2', '0', '0 1')]}
# json_str = json.dumps(task_dic)
# task = Task()
# task.create_from_json(json_str)

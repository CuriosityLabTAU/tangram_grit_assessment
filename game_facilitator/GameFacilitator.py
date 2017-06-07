from tangrams import *
from SelectionGeneratorCuriosity import *

import json


class GameFacilitator():


    def __init__(self):
        self.selected_task_index = 1  # 0/1/2 according to user selected task
        self.selection_tasks = None  # a list of 3 json strings that represent 3 tasks
        self.current_task = Task()  # The selected task as Task() object
        # self.selection_gen = SelectionGenerator()
        self.selection_gen = SelectionGeneratorCuriosity()
        self.selection_gen.load_dif_levels()
        self.current_player = 'Robot'  # current_player can be 'Robot' or 'Child'
        self.game_counter = 0 #  count number of games

    def check_solution(self, json_str_board):
        board_task = Task()
        # print ("check solution: ",json_str_board)
        board_task.create_from_json(json_str_board)
        # print self.current_task.check_solution(board_task.x, board_task.solution)
        return self.current_task.check_solution(board_task.x, board_task.solution)

    def generate_tangram_options(self, challange):
        if challange:
            self.selection_tasks = self.selection_gen.get_challenge_selection()
        else:
            self.selection_tasks = self.selection_gen.get_current_selection()

        # T = []
        # test1_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 1')]}
        # T.append(json.dumps(test1_dict))
        # test2_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 2')]}
        # T.append(json.dumps(test2_dict))
        # test3_dict = {'size': '5 5', 'pieces': [('square', '90', '1 1'), ('small triangle2', '180', '0 3')]}
        # T.append(json.dumps(test3_dict))
        return self.selection_tasks

    def tangram_selected(self, selected_task_index):
        # selected_task_index can be 0/1/2 according to user selection.
        self.selected_task_index = selected_task_index
        #print 'GameFacilitator: '+str(self.selected_task_index)
        self.current_task.create_from_json(self.selection_tasks[self.selected_task_index][0])

    def update_game_result(self, game_result):
        # game_result can be 'S' (Success) or 'F' (Failure)
        #if self.game_counter != 9: #
        self.selection_gen.update_game_result(self.current_player, self.selected_task_index, game_result)
        self.game_counter +=1
        if self.current_player == 'Robot':
            self.current_player = 'Child'
        elif self.current_player == 'Child':
            self.current_player = 'Robot'
        print ('GameFacilitator:updated game result ','#',self.game_counter, 'is:',game_result,'next player is:' ,self.current_player)
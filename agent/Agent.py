from tangrams import *
import json
import time
import pickle
from tablet_app.tangram_game import *


class Agent:
    condition = 'c-g-'
    def __init__(self):
        # print ("TangramGame.SCALE", TangramGame.SCALE)
        self.solver = Solver()
        # self.mindset = Mindset()
        # self.curiosity = Curiosity()
        self.seq_of_jsons = None
        self.current_move = None
        self.efficiency_iter = iter([1,1,1,1,1,1,1]) # determines whether the robot will try to solve or act randomly for each round
        self.current_efficiency = None # efficiency of current round
        self.current_round = 0
        self.child_selected_index = None # indicates the selection of the child. possible values are 0/1/2
        self.child_result = None  # indicates the child result. possible values are 'S' (Success) or 'F' (Fail)
        self.mindset = 0.9
        self.curiosity = 0.9
        with open('agent/' + 'solve_cache_curiosity' + '.pkl', 'rb') as f:
            self.solve_cache_curious = pickle.load(f)
        with open('agent/' + 'solve_cache_curiosity_non' + '.pkl', 'rb') as f:
            self.solve_cache_not_curious = pickle.load(f)
        with open('agent/' + 'selection_cache_curiosity' + '.pkl', 'rb') as f:
            self.selection_sequence_curious = pickle.load(f)
        with open('agent/' + 'selection_cache_curiosity_non' + '.pkl', 'rb') as f:
            self.selection_sequence_not_curious = pickle.load(f)

    def update_condition(self, condition):
        self.condition  = condition
        # self.condition = 'c-g-' #''Mindset' # value can be 'Mindset' or 'Neutral'
        if 'g+' in self.condition:
            self.mindset = 0.9
        elif 'g-' in self.condition:
            self.mindset = 0.1

    def solve_task(self, json_str_task):
        print ('solve task', self.current_round)
        if 'c-' in self.condition:
            # self.seq_of_jsons = self.solve_cache_not_curious[json_str_task]
            self.seq_of_jsons = self.solve_cache_not_curious[str(self.current_round)]
        elif 'c+' in self.condition:
            self.seq_of_jsons = self.solve_cache_curious[str(self.current_round)]
        # self.seq_of_jsons = self.solve_cache[json_str_task]
        self.current_move = 0
        # task = Task()
        # task.create_from_json(json_str_task)
        # self.solver.set_available_pieces(task)
        # self.solver.run_task(task, duration=50, stop=True)
        # seq = self.solver.get_seq_of_moves()
        # self.seq_of_jsons = seq
        # self.current_move = 0

    def solve_task_randomly(self, json_str_task):
        task = Task()
        task.create_from_json(json_str_task)
        self.solver.set_available_pieces(task)
        self.solver.run_task(task, duration=2, stop=True)
        seq = self.solver.get_seq_of_random_moves(task, 50)
        self.seq_of_jsons = seq
        self.current_move = 0

    def play_move(self, json_str_task):
        # currently, only gets the task and generate a sequence of moves
        # future: also gets the current state
        if self.seq_of_jsons is None:
            self.current_efficiency = self.efficiency_iter.next()
            if self.current_efficiency == 1:
                self.solve_task(json_str_task)
            else:
                self.solve_task_randomly(json_str_task)
            print(self.seq_of_jsons)
        if self.current_move+1 < len(self.seq_of_jsons):
            self.current_move += 1
        move = self.seq_of_jsons[self.current_move]
        if self.current_efficiency ==0 and np.random.rand() > self.mindset: #  if mindset is low then wait with high probabilty
            time.sleep(2)
        return move


    def finish_moves(self):
        self.seq_of_jsons = None

    def record_child_selection(self, selected_index):
        self.child_selected_index = selected_index

    def record_child_result(self, result):
        self.child_result = result

    def set_selection(self):
        if 'c+' in self.condition:
            # get H for puzzles
            select = self.selection_sequence_curious[self.current_round]
            TangramGame.cog_tangram_selection = select
        elif 'c-' in self.condition:
            select = self.selection_sequence_not_curious[self.current_round]
            TangramGame.cog_tangram_selection = select
        self.current_round += 1

        # if self.condition == 'c-g+':
        #     if self.child_result == None:
        #         select = 1  # First round, select demo task
        #     elif self.child_result == 'S':
        #         select = min(self.child_selected_index+1,2)
        #     elif self.child_result == 'F':
        #         select = self.child_selected_index
        #     else:
        #         select = 1  # in case of a bug, select 2
        # else:  # ==> self.condition == 'Neutral'
        #     if self.child_result == None:
        #         select = 1 # First round, select demo task
        #     elif self.child_result == 'S':
        #         select = self.child_selected_index
        #     elif self.child_result == 'F':
        #         select = max(self.child_selected_index - 1, 0)
        #     else:
        #         select = 1 # in case of a bug, select 2
        return select






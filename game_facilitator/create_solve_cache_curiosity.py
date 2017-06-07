from tangrams import *
import numpy as np
import random
import pickle

# number of networks in Solver was 10 for this computation

np.random.seed(1)
random.seed(1)

#json_str_task = '{"pieces": [["large triangle2", "90", "1 2"], ["small triangle1", "0", "0 2"], ["parrallelogram", "0", "1 1"]], "size": "5 5"}'
json_all_pieces = '{"pieces": [["square", "0", "0 0"], ["small triangle2", "0", "0 1"], ["small triangle1", "90", "1 0"], ["large triangle1", "0", "1 1"], ["parrallelogram", "0", "2 0"], ["medium triangle", "0", "3 1"], ["large triangle2", "180", "1 1"]], "size": "5 5"}'
task_all_pieces = Task()
task_all_pieces.create_from_json(json_all_pieces)
solver = Solver()
solver_cache = {}
line_num = 1

with open('./game_facilitator/tangram_paths' + '.txt','r') as fp:
    for line in fp:
        print line_num
        line_num += 1
        if 'path' in line:
            pass
        else:
            json_str_task=line.strip('\n')
            task = Task()
            task.create_from_json(json_str_task)
            # solver.set_available_pieces(task)
            solver.set_initial_task(task)
            solver.run_task(task, duration=300, stop=True)
            seq = solver.get_seq_of_moves_v2(task_all_pieces)
            solver_cache[json_str_task]= seq

with open('agent/' + 'solve_cache_curiosity' + '.pkl', 'wb') as f:
    pickle.dump(solver_cache, f, pickle.HIGHEST_PROTOCOL)

with open('agent/' + 'solve_cache_curiosity' + '.pkl', 'rb') as f:
    loaded =  pickle.load(f)

# def save_obj(obj, name ):
#     with open('obj/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#
# def load_obj(name ):
#     with open('obj/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)
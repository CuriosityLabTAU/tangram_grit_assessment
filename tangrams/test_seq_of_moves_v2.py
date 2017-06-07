# from tangrams import *
# import random
# import numpy as np
# import matplotlib.pyplot as plt
#
# def json_to_NN(json_str):
#     sol = Solver()
#     task = Task()
#     task.create_from_json(json_str)
#     sol.set_initial_task(task)
#
#     # dictionary: key = name of node, value = number of node
#     dic = {}
#     for n in range(len(sol.networks[0].nodes)):
#         # print sol.networks[0].nodes[n].name[0] + ' ' + sol.networks[0].nodes[n].name[1] + ' ' + sol.networks[0].nodes[n].name[2]
#         dic[sol.networks[0].nodes[n].name[0] + ' ' + sol.networks[0].nodes[n].name[1] + ' ' + sol.networks[0].nodes[n].name[2]] = n
#
#     # generate a random tangram with N pieces
#     # task.random_task(sol.networks[0], number_pieces=number_pieces)
#     training_task = task
#     training_input = (np.minimum(task.x, 1)).flatten()  # only 0/1 (not 1,2,5)
#
#     # solve the orignial task using the solution
#     activation = np.zeros_like(sol.networks[0].a)
#     for piece in task.solution:
#         node_num = dic[piece.name[0] + ' ' + piece.name[1] + ' ' + piece.name[2]]
#         activation[node_num] = 1
#     training_output = activation
#     return training_task, training_input, training_output
#
# np.random.seed(3)
# random.seed(3)
#
# json_all_pieces = '{"pieces": [["square", "0", "0 0"], ["small triangle2", "0", "0 1"], ["small triangle1", "90", "1 0"], ["large triangle1", "0", "1 1"], ["parrallelogram", "0", "2 0"], ["medium triangle", "0", "3 1"], ["large triangle2", "180", "1 1"]], "size": "5 5"}'
# task_all_pieces = Task()
# task_all_pieces.create_from_json(json_all_pieces)
#
# sol = Solver()
# task = Task()
# task_json = '{"pieces": [["large triangle2", "180", "1 1"], ["medium triangle", "180", "0 1"], ["square", "0", "2 0"], ["small triangle2", "90", "1 0"], ["small triangle1", "0", "2 3"], ["large triangle1", "0", "1 1"]], "size": "5 5"}'
# # task.create_from_json('{"pieces": [["square", "0", "2 2"], ["small triangle2", "270", "3 2"], ["small triangle1", "0", "1 2"]], "size": "5 5"}')
# task.create_from_json(task_json)
#
# training_task, training_input, training_output = json_to_NN(task_json)
#
# sol.set_initial_task(task)
# # sol.set_activation(training_output)
# sol.run_task(task, duration=1000, stop=True)
# seq = sol.get_seq_of_moves_v2(task_all_pieces)
# print seq
# temp = Task()
# plt.figure()
# print(len(seq))
# for s in seq:
#     print s
#     temp.create_from_json(s)
#     plt.imshow(temp.x, interpolation='none')
#     plt.pause(2)
#

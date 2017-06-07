from tangrams import *
import matplotlib.pyplot as plt
b = Task()
b.create_from_json('{"size": "5 5", "pieces": [["square", "0", "-5 -4"], ["small triangle2", "0", "1 2"], ["small triangle1", "270", "2 2"], ["large triangle1", "0", "-5 2"], ["parrallelogram", "0", "2 2"], ["medium triangle", "90", "2 2"], ["large triangle2", "0", "-5 8"]]}')
plt.figure()
plt.imshow(b.x, interpolation = 'none')
t = Task()
t.create_from_json('{"pieces": [["square", "0", "2 2"], ["small triangle2", "270", "3 2"], ["small triangle1", "0", "1 2"]], "size": "5 5"}')
plt.figure()
plt.imshow(t.x, interpolation = 'none')
t.check_solution(b.x, b.solution)
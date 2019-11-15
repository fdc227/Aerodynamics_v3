from shape_gen import shape_gen
import numpy as np
from sympy import *
import numexpr as ne
import pickle

sol_raw = open('sol.pkl', 'rb')
sol = pickle.load(sol_raw)
n = len(sol)
print(sol.shape)

sol_T = np.array(sol).transpose()
zero_array = np.zeros(n)
sol_T = np.insert(sol_T, 40, zero_array, axis=0)
sol_T = np.insert(sol_T, 30, zero_array, axis=0)
sol_T = np.insert(sol_T, 20, zero_array, axis=0)
sol_T = np.insert(sol_T, 10, zero_array, axis=0)
sol_T = np.insert(sol_T, 0, zero_array, axis=0)
print(sol_T.shape)

y, L = symbols('y, L')
shapes = shape_gen(4)
shape_funcs = []
for i in shapes:
    shape_funcs.append(lambdify(y, i.subs({L:1})))

def function_generator(list1, list2, list3, list4):
    def output_function(y):
        l1 = list1
        l2 = list2
        l3 = list3
        l4 = list4
        q1 = shape_funcs[0](y)
        q2 = shape_funcs[1](y)
        q3 = shape_funcs[2](y)
        q4 = shape_funcs[3](y)
        final_list = ne.evaluate('q1*l1+q2*l2+q3*l3+q4*l4')
        return final_list
    return output_function

beam_functions = []
for i in range(10):
    beam_functions.append(function_generator(sol_T[i], sol_T[i+11], sol_T[i+1], sol_T[i+12]))

yspace = np.linspace(0, 1, 10, endpoint=False)

def beam_shape_gen(i):
    local_storage = []
    for y in yspace:
        local_storage.append(beam_functions[i](y))
    print(f'Finished {i+1}/{len(beam_functions)}th section')
    return local_storage

r = [r for r in range(len(beam_functions))]
final_output = [beam_shape_gen(i) for i in r]

final_output_unpacked = []
for i in final_output:
    final_output_unpacked += i

final_output_unpacked_T = np.array(final_output_unpacked).transpose()

output_raw = open('final_output_v2.pkl', 'wb')
pickle.dump(final_output_unpacked_T, output_raw)
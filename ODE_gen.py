from sympy import *
from shape_gen import shape_gen
from multiprocessing.pool import Pool
import pickle
from scipy.integrate import odeint
from numpy.linalg import inv
import numpy as np

E, I, m, x_f, L, G, J = symbols('E, I, m, x_f, L, G, J')
y, t = symbols('y, t')
rho, a_w, V_inf, e, M_theta = symbols('rho, a_w, V_inf, e, M_theta')

shapes = shape_gen(4)
S1 = shapes[0]
S2 = shapes[1]
S3 = shapes[2]
S4 = shapes[3]

q_bending_sym = []
q_bending_dot_sym = []
q_torsion_sym = []
q_inplane_sym = []
q_inplane_dot_sym = []
q_bending_dt_sym = []
q_bending_dot_dt_sym = []
q_torsion_dt_sym = []
q_inplane_dt_sym = []
q_inplane_dot_dt_sym = []
q_bending_dt_dt_sym = []
q_bending_dot_dt_dt_sym = []
q_torsion_dt_dt_sym = []
q_inplane_dt_dt_sym = []
q_inplane_dot_dt_dt_sym = []


for i in range(10):
    q_bending_sym.append(symbols(f'q{i}_bending'))
    q_bending_dt_sym.append(symbols(f'q{i}_bending_dt'))
    q_bending_dt_dt_sym.append(symbols(f'q{i}_bending_dt_dt'))
    q_bending_dot_sym.append(symbols(f'q{i}_bending_dot'))
    q_bending_dot_dt_sym.append(symbols(f'q{i}_bending_dot_dt'))
    q_bending_dot_dt_dt_sym.append(symbols(f'q{i}_bending_dot_dt_dt'))
    q_torsion_sym.append(symbols(f'q{i}_torsion'))
    q_torsion_dt_sym.append(symbols(f'q{i}_torsion_dt'))
    q_torsion_dt_dt_sym.append(symbols(f'q{i}_torsion_dt_dt'))
    q_inplane_sym.append(symbols(f'q{i}_inplane'))
    q_inplane_dt_sym.append(symbols(f'q{i}_inplane_dt'))
    q_inplane_dt_dt_sym.append(symbols(f'q{i}_inplane_dt_dt'))
    q_inplane_dot_sym.append(symbols(f'q{i}_inplane_dot'))
    q_inplane_dot_dt_sym.append(symbols(f'q{i}_inplane_dot_dt'))
    q_inplane_dot_dt_dt_sym.append(symbols(f'q{i}_inplane_dot_dt_dt'))

param = {E:200*10**6, I:1, m:7800, x_f:0.5, L:1, G:10**6, J:1, rho:1.225, a_w:3.14, V_inf:10, e:0.3, M_theta:0.3} 

IC = []
for i in range(10):
    IC.append(0.2*(i+1))
for i in range(10):
    IC.append(0.2)
for i in range(10):
    IC.append(0.1*(i+1))
for i in range(10):
    IC.append(0.2*(i+1))
for i in range(10):
    IC.append(0.2)
for i in range(50):
    IC.append(0.0)
IC = np.array(IC, dtype=float)
# print(IC.shape)

A_raw = open('A.pkl', 'rb')
A = pickle.load(A_raw)
A = Matrix(A).xreplace(param)

C_raw = open('C.pkl', 'rb')
C = pickle.load(C_raw)
C = Matrix(C).xreplace(param)

W_raw = open('delta.pkl', 'rb')
W = pickle.load(W_raw)
W = Matrix(W).xreplace(param)
print(W.shape)

var_list = [*q_bending_sym, *q_bending_dot_sym, *q_torsion_sym, *q_inplane_sym, *q_inplane_dot_sym, *q_bending_dt_sym, *q_bending_dot_dt_sym, *q_torsion_dt_sym, *q_inplane_dt_sym, *q_inplane_dot_dt_sym]
n = len(var_list)
A_np = np.array(A, dtype=float)
C_np = np.array(C, dtype=float)
W_f = lambdify(var_list, W, 'numpy')
print(W_f(*IC))

def beam_func(y, t):
    y_upper = y[50:100]
    state_var = np.array(y[0: 50]).reshape((50, 1))
    W_np = W_f(*y)
    RHS = -np.dot(C_np, state_var) + W_np
    y_lower = (np.dot(inv(A_np), RHS)).flatten()
    output = np.concatenate((y_upper, y_lower))
    # print(f'{y}')
    return output

t = np.linspace(0, 10, 100)
sol = odeint(beam_func, IC, t, mxstep=5000000)

sol_raw = open('sol.pkl', 'wb')
pickle.dump(sol, sol_raw)
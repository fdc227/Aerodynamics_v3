from sympy import *
from shape_gen import shape_gen
from torsion_shape_gen import torsion_shape_gen
from multiprocessing.pool import Pool
import pickle

E, I, m, x_f, L, G, J, x_f = symbols('E, I, m, x_f, L, G, J, x_f')
y, t = symbols('y, t')

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

T_raw = open('T.pkl', 'rb')
T = pickle.load(T_raw)
U_raw = open('U.pkl', 'rb')
U = pickle.load(U_raw)
W_raw = open('delta.pkl', 'rb')
W = pickle.load(W_raw)

T_var_input = [*q_bending_dt_dt_sym, *q_bending_dot_dt_dt_sym, *q_torsion_dt_dt_sym, *q_inplane_dt_dt_sym, *q_inplane_dot_dt_dt_sym]
U_var_input = [*q_bending_sym, *q_bending_dot_sym, *q_torsion_sym, *q_inplane_sym, *q_inplane_dot_sym]
# W_var_input = [*q_bending_dt_sym, *q_bending_dot_dt_sym, *q_torsion_dt_sym, *q_inplane_dt_sym, *q_inplane_dot_dt_sym]

A, b = linear_eq_to_matrix(T, T_var_input)
C, d = linear_eq_to_matrix(U, U_var_input)
# E, F = linear_eq_to_matrix(W, W_var_input)
# G, h = linear_eq_to_matrix(F, U_var_input)

# print(G)
# print(h)

A_raw = open('A.pkl', 'wb')
pickle.dump(A, A_raw)
# b_raw = open('b.pkl', 'wb')
# pickle.dump(b, b_raw)
C_raw = open('C.pkl', 'wb')
pickle.dump(C, C_raw)
# d_raw = open('d.pkl', 'wb')
# pickle.dump(d, d_raw)
# E_raw = open('E.pkl', 'wb')
# pickle.dump(E, E_raw)
# G_raw = open('G.pkl', 'wb')
# pickle.dump(G, G_raw)
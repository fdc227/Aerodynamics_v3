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

torsions = torsion_shape_gen()
S5 = torsions[0]
S6 = torsions[1]

q_bending_funct = []
q_bending_dot_funct = []
q_bending_sym = []
q_bending_dot_sym = []
q_torsion_funct = []
q_torsion_sym = []
q_inplane_funct = []
q_inplane_dot_funct = []
q_inplane_sym = []
q_inplane_dot_sym = []

q_bending_dt_funct = []
q_bending_dot_dt_funct = []
q_bending_dt_sym = []
q_bending_dot_dt_sym = []
q_torsion_dt_funct = []
q_torsion_dt_sym = []
q_inplane_dt_funct = []
q_inplane_dot_dt_funct = []
q_inplane_dt_sym = []
q_inplane_dot_dt_sym = []

q_bending_dt_dt_funct = []
q_bending_dot_dt_dt_funct = []
q_bending_dt_dt_sym = []
q_bending_dot_dt_dt_sym = []
q_torsion_dt_dt_funct = []
q_torsion_dt_dt_sym = []
q_inplane_dt_dt_funct = []
q_inplane_dot_dt_dt_funct = []
q_inplane_dt_dt_sym = []
q_inplane_dot_dt_dt_sym = []

for i in range(10):
    globals()[f'q{i}_bending'] = Function(f'q{i}_bending')(t)
    globals()[f'q{i}_bending_dot'] = Function(f'q{i}_bending_dot')(t)
    globals()[f'q{i}_torsion'] = Function(f'q{i}_torsion')(t)
    globals()[f'q{i}_inplane'] = Function(f'q{i}_inplane')(t)
    globals()[f'q{i}_inplane_dot'] = Function(f'q{i}_inplane_dot')(t)
    q_bending_funct.append(globals()[f'q{i}_bending'])
    q_bending_dot_funct.append(globals()[f'q{i}_bending_dot'])
    q_torsion_funct.append(globals()[f'q{i}_torsion'])
    q_inplane_funct.append(globals()[f'q{i}_inplane'])
    q_inplane_dot_funct.append(globals()[f'q{i}_inplane_dot'])
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

for i in range(10):
    q_bending_dt_funct.append(diff(q_bending_funct[i], t))
    q_bending_dt_dt_funct.append(diff(q_bending_funct[i], (t, 2)))
    q_bending_dot_dt_funct.append(diff(q_bending_dot_funct[i], t))
    q_bending_dot_dt_dt_funct.append(diff(q_bending_dot_funct[i], (t, 2)))
    q_torsion_dt_funct.append(diff(q_torsion_funct[i], t))
    q_torsion_dt_dt_funct.append(diff(q_torsion_funct[i], (t, 2)))
    q_inplane_dt_funct.append(diff(q_inplane_funct[i], t))
    q_inplane_dt_dt_funct.append(diff(q_inplane_funct[i], (t, 2)))
    q_inplane_dot_dt_funct.append(diff(q_inplane_dot_funct[i], t))
    q_inplane_dot_dt_dt_funct.append(diff(q_inplane_dot_funct[i], (t, 2)))


q_funct_list = [*q_bending_funct, *q_bending_dt_funct, *q_bending_dt_dt_funct, *q_bending_dot_funct, *q_bending_dot_dt_funct, *q_bending_dot_dt_dt_funct,
                *q_torsion_funct, *q_torsion_dt_funct, *q_torsion_dt_dt_funct,
                *q_inplane_funct, *q_inplane_dt_funct, *q_inplane_dt_dt_funct, *q_inplane_dot_funct, *q_inplane_dot_dt_funct, *q_inplane_dot_dt_dt_funct]

q_sym_list = [*q_bending_sym, *q_bending_dt_sym, *q_bending_dt_dt_sym, *q_bending_dot_sym, *q_bending_dot_dt_sym, *q_bending_dot_dt_dt_sym,
                *q_torsion_sym, *q_torsion_dt_sym, *q_torsion_dt_dt_sym,
                *q_inplane_sym, *q_inplane_dt_sym, *q_inplane_dt_dt_sym, *q_inplane_dot_sym, *q_inplane_dot_dt_sym, *q_inplane_dot_dt_dt_sym]

replacement = {}
for i in range(len(q_sym_list)):
    replacement[q_funct_list[i]] = q_sym_list[i]

bending_q_funct = q_bending_funct.copy()
bending_q_funct.insert(0, 0)
bending_q_dot_funct = q_bending_dot_funct.copy()
bending_q_dot_funct.insert(0, 0)
torsion_q_funct = q_torsion_funct.copy()
torsion_q_funct.insert(0, 0)
inplane_q_funct = q_inplane_funct.copy()
inplane_q_funct.insert(0, 0)
inplane_q_dot_funct = q_inplane_dot_funct.copy()
inplane_q_dot_funct.insert(0, 0)

bending_shape_func = []
torsion_shape_func = []
inplane_shape_func = []
for i in range(10):
    bending_out = S1 * bending_q_funct[i] + S2 * bending_q_dot_funct[i] + S3 * bending_q_funct[i+1] + S4 * bending_q_dot_funct[i+1]
    bending_shape_func.append(bending_out)
    torsion_out = S5 * torsion_q_funct[i] + S6 * torsion_q_funct[i+1]
    torsion_shape_func.append(torsion_out)
    inplane_out = S1 * inplane_q_funct[i] + S2 * inplane_q_dot_funct[i] + S3 * inplane_q_funct[i+1] + S4 * inplane_q_dot_funct[i+1]
    inplane_shape_func.append(inplane_out)

T_var_list = [*q_bending_dt_funct, *q_bending_dot_dt_funct, *q_torsion_dt_funct, *q_inplane_dt_funct, *q_inplane_dot_dt_funct]
U_var_list = [*q_bending_funct, *q_bending_dot_funct, *q_torsion_funct, *q_inplane_funct, *q_inplane_dot_funct]

def T_gen(i):
    fb = bending_shape_func[i]
    ft = torsion_shape_func[i]
    fi = inplane_shape_func[i]
    dT_rotate = Rational(1/6)*m*(1-2*x_f+2*x_f**2)*diff(ft, t)**2
    dT_linear = Rational(1/2)*m*(diff(fb, t)**2+diff(fi, t)**2)
    T = integrate(dT_rotate + dT_linear, (y, 0, L))
    output = []
    for j in T_var_list:
        output.append(diff(diff(T, j), t).xreplace(replacement))
    print(f'{i+1}/10 of T generated')
    return output

def U_gen(i):
    fb = bending_shape_func[i]
    ft = torsion_shape_func[i]
    fi = inplane_shape_func[i]
    U = Rational(1/2)*E*I*integrate(diff(fb,(y, 2))**2+diff(fi,(y, 2))**2, (y, 0, L)) + Rational(1/2)*G*J*integrate(diff(ft, y)**2, (y, 0, L))
    output = []
    for j in U_var_list:
        output.append(diff(U, j).xreplace(replacement))
    print(f'{i+1}/10 of U generated')
    return output

p = Pool(10)
R = [r for r in range(10)]
T_lists = p.map(T_gen, R)
U_lists = p.map(U_gen, R)

T_list_final = Matrix(T_lists).T.tolist()
U_list_final = Matrix(U_lists).T.tolist()

T = [nsimplify(sum(i)) for i in T_list_final]
U = [nsimplify(sum(i)) for i in U_list_final]

T_raw = open('T.pkl', 'wb')
U_raw = open('U.pkl', 'wb')
pickle.dump(T, T_raw)
pickle.dump(U, U_raw)


rho, a_w, V_inf, e, M_theta = symbols('rho, a_w, V_inf, e, M_theta')

q_bending_delta = []
q_bending_dot_delta = []
q_torsion_delta = []
q_inplane_delta = []
q_inplane_dot_delta = []

for i in range(10):
    q_bending_delta.append(symbols(f'q{i}_bending_delta'))
    q_bending_dot_delta.append(symbols(f'q{i}_bending_dot_delta'))
    q_torsion_delta.append(symbols(f'q{i}_torsion_delta'))
    q_inplane_delta.append(symbols(f'q{i}_inplane_delta'))
    q_inplane_dot_delta.append(symbols(f'q{i}_inplane_dot_delta'))

bending_q_delta = q_bending_delta.copy()
bending_q_delta.insert(0, 0)
bending_q_dot_delta = q_bending_dot_delta.copy()
bending_q_dot_delta.insert(0, 0)
torsion_q_delta = q_torsion_delta.copy()
torsion_q_delta.insert(0, 0)
inplane_q_delta = q_inplane_delta.copy()
inplane_q_delta.insert(0, 0)
inplane_q_dot_delta = q_inplane_dot_delta.copy()
inplane_q_dot_delta.insert(0, 0)

bending_shape_delta = []
torsion_shape_delta = []
inplane_shape_delta = []
for i in range(10):
    bending_out = S1 * bending_q_delta[i] + S2 * bending_q_dot_delta[i] + S3 * bending_q_delta[i+1] + S4 * bending_q_dot_delta[i+1]
    bending_shape_delta.append(bending_out)
    torsion_out = S5 * torsion_q_delta[i] + S6 * torsion_q_delta[i+1]
    torsion_shape_delta.append(torsion_out)
    inplane_out = S1 * inplane_q_delta[i] + S2 * inplane_q_dot_delta[i] + S3 * inplane_q_delta[i+1] + S4 * inplane_q_dot_delta[i+1]
    inplane_shape_delta.append(inplane_out)

dL_list = []
for i in range(10):
    out = Rational(1/2)*rho*V_inf**2*a_w*((1/V_inf + 1/V_inf**2*diff(inplane_shape_func[i], t)) * diff(bending_shape_func[i], t) + torsion_shape_func[i])
    dL_list.append(out)

dM_list = []
for i in range(10):
    out = Rational(1/2)*rho*V_inf**2*(e*a_w*((1/V_inf + 1/V_inf**2*diff(inplane_shape_func[i], t)) * diff(bending_shape_func[i], t) + torsion_shape_func[i]) + M_theta*Rational(1/4)*(1/V_inf + 1/V_inf**2*diff(inplane_shape_func[i], t))*diff(torsion_shape_func[i], t))
    dM_list.append(out)

delta_variable = [*q_bending_delta, *q_bending_dot_delta, *q_torsion_delta, *q_inplane_delta, *q_inplane_dot_delta]

def delta_gen(i):
    dL = dL_list[i]
    dM = dM_list[i]
    fbd = bending_shape_delta[i]
    ftd = torsion_shape_delta[i]
    dW = integrate(dL*fbd+dM*ftd, (y, 0, L))
    output = []
    for j in delta_variable:
        output.append(diff(dW, j).xreplace(replacement))
    print(f'{i+1}/10 of delta generated')
    return output

P = Pool(10)
delta_list = P.map(delta_gen, R)
delta_list_final = Matrix(delta_list).T.tolist()
delta = [nsimplify(sum(i)) for i in delta_list_final]
delta_raw = open('delta.pkl', 'wb')
pickle.dump(delta, delta_raw)

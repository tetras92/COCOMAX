from cocomax import *

N = 6
X = all_possible_allocations(N)
L_C = L_couple_single_peaked_preferences(N)
M_PO = matrix_of_PO_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)

for i in range(len(L_C)):
    s = ""
    for j in range(len(X)):
        s += str(M_PO[i, j])
        s += " "
    print(s)
# print(M_PO)

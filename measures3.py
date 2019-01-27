from cocomax import *
from algorithms import *
import time
import matplotlib.pyplot as plt

Nmin = 4
Nmax = 4

for N in range(Nmin, Nmax+1, 2):
    L_C = L_couple_single_peaked_preferences(N)
    X = all_possible_allocations(N)
    M_PO = matrix_of_PO_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    M_EF = matrix_of_EF_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    M_MM = matrix_of_MM_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)

    os_number_of_allocations = 0
    os_number_of_p_ef_mm_allocations = 0
    for i_p in range(len(L_C)):
        profile_A, profile_B = L_C[i_p]
        U = {i for i in range(1, N+1)}
        Allocations = TR(N=N, A_pprofile=profile_A, B_pprofile=profile_B)
        # Allocations = OS(Alloc=list(), Z_A=set(), Z_B=set(), A_pprofile=profile_A, B_pprofile=profile_B, U=U)
        if len(Allocations) == 0:
            print("no found")
        os_number_of_allocations += len(Allocations)
        for alloc in Allocations:
            ix = 0
            alloc_found_in_X = False
            while not alloc_found_in_X:
                if X[ix] == alloc:
                    alloc_found_in_X = True
                else:
                    ix += 1

            # if M_PO[i_p, ix]  and M_EF[i_p, ix] and M_MM[i_p, ix]:
            if M_EF[i_p, ix]:
                os_number_of_p_ef_mm_allocations += 1
    print(round(100.*os_number_of_p_ef_mm_allocations/os_number_of_allocations, 2))



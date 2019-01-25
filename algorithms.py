


def OS(Alloc=list(), Z_A=set(), Z_B=set(), U=set(), A_pprofile=[], B_pprofile=[], l=1):

    def H(agent_pprofile, l):
        return U & set(agent_pprofile[:l])

    if len(U) == 0:
        if Z_A not in Alloc:
            print(Z_A)
            Alloc.append(Z_A)
        return
    H_A_l = H(A_pprofile, l)
    H_B_l = H(B_pprofile, l)
    # print("HA", H_A_l)
    # print("HB", H_B_l)
    found = False
    for i_A in H_A_l:
        for i_B in H_B_l:
            if i_A != i_B:
                Z_A_c = Z_A.copy()
                Z_B_c = Z_B.copy()
                U_c = U.copy()
                Z_A.add(i_A)
                Z_B.add(i_B)
                U.remove(i_A)
                U.remove(i_B)
                found = True
                OS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
                Z_A = Z_A_c
                Z_B = Z_B_c
                U = U_c

    if not found:
        OS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
    return Alloc


A = OS(A_pprofile=[1, 2, 3, 4], B_pprofile=[1, 3, 2, 4], U=set([1, 2, 3, 4]))
print (A)

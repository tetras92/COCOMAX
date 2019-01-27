


def OS(Alloc=list(), Z_A=set(), Z_B=set(), U=set(), A_pprofile=[], B_pprofile=[], l=1):

    def H(agent_pprofile, l):
        return U & set(agent_pprofile[:l])

    if len(U) == 0:
        if Z_A not in Alloc:
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





def RS(Alloc=list(), Z_A=set(), Z_B=set(), U=set(), A_pprofile=[], B_pprofile=[], l=1):

    def H(agent_pprofile, l):
        return U & set(agent_pprofile[:l])

    def Top(agent_pprofile):           #agent_pprofile est une liste ordonnee des items
        for item in agent_pprofile:
            if item in U:
                return item

    def Sb(agent_pprofile):           #agent_pprofile est une liste ordonnee des items
        U_without_Top = U - {Top(agent_pprofile)}
        for item in agent_pprofile:
            if item in U_without_Top:
                return item

    if len(U) == 0:
        if Z_A not in Alloc:
            Alloc.append(Z_A)
        return
    H_A_l = H(A_pprofile, l)
    H_B_l = H(B_pprofile, l)

    top_A = Top(A_pprofile)
    top_B = Top(B_pprofile)
    found = False
    if top_A != top_B:
        Z_A_c = Z_A.copy()
        Z_B_c = Z_B.copy()
        U_c = U.copy()
        Z_A.add(top_A)
        Z_B.add(top_B)
        U.remove(top_A)
        U.remove(top_B)
        RS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
        found = True
        Z_A = Z_A_c
        Z_B = Z_B_c
        U = U_c
    else:
        if len(H_A_l) > 1:
            Z_A_c = Z_A.copy()
            Z_B_c = Z_B.copy()
            U_c = U.copy()
            second_A = Sb(A_pprofile)
            Z_A.add(second_A)
            Z_B.add(top_B)
            U.remove(second_A)
            U.remove(top_B)
            RS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
            found = True
            Z_A = Z_A_c
            Z_B = Z_B_c
            U = U_c

        if len(H_B_l) > 1:
            Z_A_c = Z_A.copy()
            Z_B_c = Z_B.copy()
            U_c = U.copy()
            second_B = Sb(B_pprofile)
            Z_A.add(top_A)
            Z_B.add(second_B)
            U.remove(top_A)
            U.remove(second_B)
            RS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
            found = True
            Z_A = Z_A_c
            Z_B = Z_B_c
            U = U_c

    if not found:
        RS(Alloc, Z_A, Z_B, U, A_pprofile, B_pprofile, l+1)
    return Alloc


# A = RS(A_pprofile=[1, 2, 3, 4], B_pprofile=[1, 3, 2, 4], U=set([1, 2, 3, 4]))
# print (A)

def BU(N=0, A_pprofile=[], B_pprofile=[]):
    # at most 2 allocations

    def Last(agent_pprofile):
        for item in agent_pprofile[::-1]:
            if item in U:
                return item

    U = {i for i in range(1, N+1)}
    Alloc = list()
    Z_A = set()
    Z_B = set()
    # Ordre des joueurs A puis B
    while len(U) != 0:
        if len(U) % 2 == 0:
            last_A = Last(A_pprofile)
            Z_B.add(last_A)
            U.remove(last_A)
        else:
            last_B = Last(B_pprofile)
            Z_A.add(last_B)
            U.remove(last_B)

    Alloc.append(Z_A.copy())
    Z_A.clear()
    Z_B.clear()
    U = {i for i in range(1, N+1)}
    # Ordre des joueurs B puis A
    while len(U) != 0:
        if len(U) % 2 != 0:
            last_A = Last(A_pprofile)
            Z_B.add(last_A)
            U.remove(last_A)
        else:
            last_B = Last(B_pprofile)
            Z_A.add(last_B)
            U.remove(last_B)
    # print(Z_A)
    if Z_A != Alloc[0]:
        Alloc.append(Z_A)

    return Alloc
#
# B = BU(4, A_pprofile=[1, 2, 3, 4], B_pprofile=[1, 3, 2, 4])
#
# print(B)

def TR(N=0, A_pprofile=[], B_pprofile=[]):


    def H(agent_pprofile, l, U):
        return U & set(agent_pprofile[:l])


    def Last(agent_pprofile, U):
        for item in agent_pprofile[::-1]:
            if item in U:
                return item

    def TR_according_to_players_order(P_profiles_ordered_List):
        L_B = [set() for n in range(2)]
        U = {i for i in range(1, N+1)}
        for l in range(1, N+1, 2):
            for pprofile_id in range(len(P_profiles_ordered_List)):
                pprofile = P_profiles_ordered_List[pprofile_id]
                H_m_l = H(pprofile, l, U)
                if len(H_m_l) == 0:
                    return False, None #No envy-free allocations exists
                opponent_id = (pprofile_id + 1)%2
                opprofile = P_profiles_ordered_List[opponent_id]

                item_to_allocate = Last(opprofile, H_m_l)
                U.remove(item_to_allocate)
                L_B[pprofile_id].add(item_to_allocate)

        return True, L_B

    Alloc = list()
    ef_alloc_found, A = TR_according_to_players_order([A_pprofile, B_pprofile])
    if ef_alloc_found:
        Alloc.append(A[0])

    ef_alloc_found, A = TR_according_to_players_order([B_pprofile, A_pprofile])
    if ef_alloc_found:
        if Alloc[0] != A[1]:
            Alloc.append(A[1])

    return Alloc

# [2, 3, 1, 4], [1, 2, 3, 4
# B = BU(4, A_pprofile=[2, 3, 1, 4], B_pprofile=[1, 2, 3, 4])
# #
# print(B)

import itertools as ite
import numpy as np
from single_peaked import *
import time

def all_possible_allocations(N):
    """int -> List[Set[int]]
    retourne l'ensemble exhaustif de tous les bundles de taille N/2
    N etant le nombre total d'objets"""

    L = list(ite.combinations([i for i in range(1, N+1)], int(N/2)))
    return [set(E) for E in L]

#Alias  Profile : List[int]
#Alias Bundle : Set[int]
def borda_score(N, agent_pprofile=[], agent_bundle={}):
    """int * Profile * Bundle -> int
    retourne le score de Borda d'un agent dont le profil de preferences
    est agent_pprofile et qui recoit le bundle agent_bundle
    HYPOTHESE : len(agent_bundle) == N/2; len(agent_pprofile) = N"""
    score = 0
    for i in range(len(agent_pprofile)):
        rank_i = i + 1
        item_at_rank_i = agent_pprofile[i]
        if item_at_rank_i in agent_bundle:
            score += (N + 1 - rank_i)
    return score


#Alias Allocations : List[Set[int]] : une allocation decrite par le bundle de l'agent 1.
def matrix_of_borda_scores(N=0, X=[], agent1_pprofile=[], agent2_pprofile=[]):
    """int * Allocation * Profile * Profile -> Matrix(len(X), 1)
    retourne une matrice des scores de Borda (sous forme de couple) de 2
    agents 1 et 2 ayant respectivement comme profils de preference agent1_pprofile et
    agent2_pprofile et ce, etant donne les affectations decrites dans X
    HYPOTHESE : len(agent[I]_pprofile) = N/2 """
    if len(agent1_pprofile) != N or len(agent2_pprofile) != N:
        raise Exception("profile length must be {}".format(N))
    BSM = np.zeros((0, 2))
    for i in range(len(X)):
        agent1_bscore = borda_score(N, agent_pprofile=agent1_pprofile, agent_bundle=set(X[i]))
        agent2_bundle = set([j for j in range(1, N+1)]) - set(X[i])

        agent2_bscore = borda_score(N, agent_pprofile=agent2_pprofile, agent_bundle=agent2_bundle)
        BSM = np.vstack((BSM, np.array([agent1_bscore, agent2_bscore])))
    return BSM


def PO_allocations_values(X=[], BSM=None):
    """Allocations * Matrix(len(X),1) -> List[bool]
    retourne une liste de booleens. Elle est telle que la valeur a la position i  est
    vraie ssi l'allocation a la position i dans X est Pareto-optimale etant donne la
    matrice des Borda Scores possibles
    HYPOTHESE: len(X) == len(BSM)"""
    PO_list = list()
    for i in range(len(X)):
        j = 0
        i_Pdominated = False
        while (j < len(X) and not(i_Pdominated)):
            #allocation j domine -t- elle i :

            Eval = BSM[i] > BSM[j]
            if Eval[0] or Eval[1]: # i a une composante strictement superieure a la meme dans j : i n'est pas domine par j
                j += 1
                continue
            Eval = BSM[j] > BSM[i]
            if Eval[0] or Eval[1]:   # sinon si j a une composante strictement superieure a la meme de i : i est domine par j
                i_Pdominated = True
            j += 1
        PO_list.append(not i_Pdominated)
    return PO_list


def matrix_of_PO_allocations_values(N=0, X=[], L_of_couple_of_pprofiles=(None, None)):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> Matrix[len(L_of_couple_of_pprofiles), len(X)]
    retourne une matrice dont chaque ligne represente un couple de profils de preference des agents 1 et 2
    et chaque colonne une allocation possible. A l'intersection on a un booleen b indiquant si l'allocation (en colonne)
    est Pareto-Optimale etant donne le couple de profils de preference (en ligne)"""
    M = np.zeros((0, len(X)))
    for i in range(len(L_of_couple_of_pprofiles)):
        agent1_pprofile, agent2_pprofile = L_of_couple_of_pprofiles[i]
        B = matrix_of_borda_scores(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
        PO_values = PO_allocations_values(X=X, BSM=B)
        M = np.vstack((M, np.array(PO_values)))
    return M


def EF_allocations_values(N=0, X=[], agent1_pprofile=[], agent2_pprofile=[]):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> List[bool]
    retourne une liste de booleens. Elle est telle que la valeur a la position i  est
    vraie ssi l'allocation a la position i dans X est proportionnel (ou envy-free dans notre projet)"""
    EF_list = list()
    for i in range(len(X)):
        agent1_bundle = X[i]
        agent2_bundle = {j for j in range(1, N+1)} - X[i]
        # agent 1 evaluation eq. (7) article
        i_proportional_for_agent1 = borda_score(N, agent1_pprofile, agent1_bundle) >= borda_score(N, agent1_pprofile, agent2_bundle)
        i_proportional_for_agent2 = borda_score(N, agent2_pprofile, agent2_bundle) >= borda_score(N, agent2_pprofile, agent1_bundle)
        EF_list.append(i_proportional_for_agent1 and i_proportional_for_agent2)
    return EF_list



def matrix_of_EF_allocations_values(N=0, X=[], L_of_couple_of_pprofiles=(None, None)):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> Matrix[len(L_of_couple_of_pprofiles), len(X)]
    retourne une matrice dont chaque ligne represente un couple de profils de preference des agents 1 et 2
    et chaque colonne une allocation possible. A l'intersection on a un booleen b indiquant si l'allocation (en colonne)
    est Envy-Free etant donne le couple de profils de preference (en ligne)"""
    M = np.zeros((0, len(X)))
    for i in range(len(L_of_couple_of_pprofiles)):
        agent1_pprofile, agent2_pprofile = L_of_couple_of_pprofiles[i]
        EF_values = EF_allocations_values(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
        # print(EF_values)
        M = np.vstack((M, np.array(EF_values)))
    return M


def MM_allocations_values(N=0, X=[], agent1_pprofile=[], agent2_pprofile=[]):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> List[bool]
    retourne une liste de booleens. Elle est telle que la valeur a la position i  est
    vraie ssi l'allocation a la position i dans X est max-min"""
    MM_list = list()
    B = matrix_of_borda_scores(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
    L_of_min_B_X_m = [min(B[j]) for j in range(len(X))]
    member_droit = max(L_of_min_B_X_m)
    for i in range(len(X)):
        # (8) : member gauche : min_{m = 1,2} B_m(X_m)
        member_gauche = L_of_min_B_X_m[i]
        MM_list.append(member_gauche == member_droit)
    return MM_list


def matrix_of_MM_allocations_values(N=0, X=[], L_of_couple_of_pprofiles=(None, None)):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> Matrix[len(L_of_couple_of_pprofiles), len(X)]
    retourne une matrice dont chaque ligne represente un couple de profils de preference des agents 1 et 2
    et chaque colonne une allocation possible. A l'intersection on a un booleen b indiquant si l'allocation (en colonne)
    est Max-min etant donne le couple de profils de preference (en ligne)"""
    M = np.zeros((0, len(X)))
    for i in range(len(L_of_couple_of_pprofiles)):
        agent1_pprofile, agent2_pprofile = L_of_couple_of_pprofiles[i]
        MM_values = MM_allocations_values(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
        # print(MM_values)
        M = np.vstack((M, np.array(MM_values)))
    return M


def S_allocations_values(N=0, X=[], agent1_pprofile=[], agent2_pprofile=[]):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> List[bool]
    retourne une liste de booleens. Elle est telle que la valeur a la position i  est
    vraie ssi l'allocation a la position i dans X respecte la propriete Borda - Sum"""

    S_list = list()
    B = matrix_of_borda_scores(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
    L_of_sum_B_X_m = [sum(B[j]) for j in range(len(X))]
    member_droit = max(L_of_sum_B_X_m)
    for i in range(len(X)):
        # (6) pg 6 : sum_{m} Bm(Xm)
        member_gauche = L_of_sum_B_X_m[i]
        S_list.append(member_gauche == member_droit)

    return S_list

def matrix_of_BS_allocations_values(N=0, X=[], L_of_couple_of_pprofiles=(None, None)):
    """int * Allocations * Liste[Couple[Profile, Profile]] -> Matrix[len(L_of_couple_of_pprofiles), len(X)]
    retourne une matrice dont chaque ligne represente un couple de profils de preference des agents 1 et 2
    et chaque colonne une allocation possible. A l'intersection on a un booleen b indiquant si l'allocation (en colonne)
    respecte le propriete Borda-Sum etant donne le couple de profils de preference (en ligne)"""
    M = np.zeros((0, len(X)))
    for i in range(len(L_of_couple_of_pprofiles)):
        agent1_pprofile, agent2_pprofile = L_of_couple_of_pprofiles[i]
        BS_values = S_allocations_values(N=N, X=X, agent1_pprofile=agent1_pprofile, agent2_pprofile=agent2_pprofile)
        M = np.vstack((M, np.array(BS_values)))
    return M





# N = 4
# X = all_possible_allocations(N)
# print(X)
# # # # # B = matrix_of_borda_scores(X=X, N=N, agent1_pprofile=[1, 2, 3, 4, 5, 6], agent2_pprofile=[6, 5, 4, 3, 2, 1])
# L_C = L_couple_single_peaked_preferences(N)
# # #
# # # print(L_C)
# M_PO = matrix_of_PO_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
# # # print(M_PO)
# # # M_EF = matrix_of_EF_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
# # # # print(M_EF)
# # #
# # M_MM = matrix_of_MM_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
#
# for i in range(len(L_C)):
#     print(L_C[i])
#     s = ""
#     for j in range(len(X)):
#         s += str(M_PO[i, j])
#         s += " "
#     print(s)

# M_MM = matrix_of_MM_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
# print(M_MM)

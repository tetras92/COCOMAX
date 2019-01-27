from cocomax import *
import time
import matplotlib.pyplot as plt

Nmin = 4
Nmax = 8
Borda_Pareto = list()
Borda_EF = list()
Borda_MM = list()
Borda_S = list()
Borda_Pareto_EF_MM_S = list()

for N in range(Nmin, Nmax+1, 2):
    L_C = L_couple_single_peaked_preferences(N)
    # L_C = L_couple_toutes_preferences(N)
    print("Number of problems : {}".format(len(L_C)))
    X = all_possible_allocations(N)
    print("Number of balanced allocations : {}".format(len(X)))
    t1 = time.time()
    M_PO = matrix_of_PO_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    print("Pareto", time.time() - t1)
    print("Matrix generated!")

    nb_p = 0
    for i in range(len(L_C)):
        for j in range(len(X)):
            if M_PO[i, j]:
                nb_p += 1

    Borda_Pareto.append(round(100.* nb_p/(len(L_C) * len(X)), 2))



    t1 = time.time()
    M_EF =  matrix_of_EF_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    print("Envy-Free", time.time() - t1)
    print("Matrix generated!")

    nb_e = 0
    for i in range(len(L_C)):
        for j in range(len(X)):
            if M_EF[i, j]:
                nb_e += 1

    Borda_EF.append(round(100.* nb_e/(len(L_C) * len(X)), 2))



    t1 = time.time()
    M_MM = matrix_of_MM_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    print("Max-Min", time.time() - t1)
    print("Matrix generated!")

    nb_m = 0
    for i in range(len(L_C)):
        for j in range(len(X)):
            if M_MM[i, j]:
                nb_m += 1

    Borda_MM.append(round(100.* nb_m/(len(L_C) * len(X)), 2))


    t1 = time.time()
    M_S = matrix_of_BS_allocations_values(N=N, X=X, L_of_couple_of_pprofiles=L_C)
    print("Borda-Sum", time.time() - t1)
    print("Matrix generated!")

    nb_s = 0
    for i in range(len(L_C)):
        for j in range(len(X)):
            if M_S[i, j]:
                nb_s += 1

    Borda_S.append(round(100.* nb_s/(len(L_C) * len(X)), 2))


    nb_all = 0
    for i in range(len(L_C)):
        for j in range(len(X)):
            if M_MM[i, j] and M_EF[i, j] and M_PO[i, j] and M_S[i, j]:
                nb_all += 1

    Borda_Pareto_EF_MM_S.append(round(100. * nb_all / (len(L_C) * len(X)), 2))


pa, = plt.plot(range(Nmin, Nmax+1, 2), Borda_Pareto, color="blue")
ef, = plt.plot(range(Nmin, Nmax+1, 2), Borda_EF, color="red")
mm, = plt.plot(range(Nmin, Nmax+1, 2), Borda_MM, color="yellow")
bs, = plt.plot(range(Nmin, Nmax+1, 2), Borda_S, color="magenta")
al, = plt.plot(range(Nmin, Nmax+1, 2), Borda_Pareto_EF_MM_S, color="green")

plt.legend([pa, ef, mm, bs, al], ["BP : {}".format(Borda_Pareto), "BE : {}".format(Borda_EF), "BM : {}".format(Borda_MM),"BS : {}".format(Borda_S), "ALL : {}".format(Borda_Pareto_EF_MM_S)],
           loc = 'upper right', markerscale = 100, frameon = False, fontsize = 10)
plt.title("Fraction of allocations with Borda properties")
plt.savefig("Fraction_of_allocations_with_Borda_properties[{}].png".format(Nmax))
plt.close()



# for i in range(len(L_C)):
#     s = ""
#     for j in range(len(X)):
#         s += str(M_PO[i, j])
#         s += " "
#     print(s)
# print(M_PO)

# print(M_PO[1, 2]==True)

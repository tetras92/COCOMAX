#je definis d'abord des fonctions d'overlaping entre 2 listes
def all_overlaps(list1, list2,res):
    done = []
    all_overlaps2(list1,list2,done,res)

def all_overlaps2(_list1,_list2,_done,res):
    #print("all_overlaps2 with ",_list1,_list2,_done)
    list1=list(_list1)
    list2=list(_list2)
    done = list(_done)

    if(len(list1)==0):
        res.append(done+list2)
        return

    if(len(list2)==0):
        res.append(done+list1)
        return

    done.append(list1.pop(0))
    overlap_fromleft(_list1,_list2,_done,res)

    done.append(list2.pop(0))
    overlap_fromright(_list1,_list2,_done,res)

def overlap_fromleft(_list1,_list2,_done,res):
    #print("overlap_fromleft with ",_list1,_list2,_done)
    list1=list(_list1)
    list2=list(_list2)
    done = list(_done)

    done.append(list1.pop(0))
    all_overlaps2(list1,list2,done,res)

def overlap_fromright(_list1,_list2,_done,res):
    #print("overlap_fromright with ",_list1,_list2,_done)
    list1=list(_list1)
    list2=list(_list2)
    done = list(_done)

    done.append(list2.pop(0))
    all_overlaps2(list1,list2,done,res)


#code pour tester les fonction d'overlap
# l1=[1,2]
# l2=[3,4]
# res=[]
# all_overlaps(l1,l2,res)
# print(res)

import itertools


def list_of_all_objects(N):
    listallobjects = range(1, N + 1)
    return list(listallobjects)



#fonction recursive
def single_peak_branch(listobjects, listalloc):
    if(len(listobjects) == 1):
        return listobjects

    #on prends en compte les objets un par un comment correspond au peak
    for i, objecti in enumerate(listobjects):
        remain_left = list(reversed(list(listobjects[0:i])))
        remain_right =list(listobjects[i+1:])
        #print("objet ", objecti)
        #print("\t remain_left = ", remain_left)
        #print("\t remain_right = ", remain_right)

        if(len(remain_left)==0):
            alloc = list()
            alloc.append(objecti)
            alloc = alloc + list(remain_right)
            #print("\t final alloc found : ", alloc)
            listalloc.append(alloc)

        if(len(remain_right)==0):
            alloc = list()
            alloc.append(objecti)
            alloc = alloc + list(remain_left)
            #print("\t final alloc found : ", alloc)
            listalloc.append(alloc)

        #if we have two non-empty lists, we want to combine them
        if(len(remain_left)>0 and len(remain_right)>0):
            list1=remain_left
            list2=remain_right
            res=[]
            all_overlaps(remain_left,remain_right,res)
            #add objecti to each element of res
            objectilist = []
            objectilist.append(objecti)
            final_res = [objectilist+x for x in res]
            #print("\t combine : ",final_res)
            [listalloc.append(x) for x in final_res]



def single_peaked_preferences(N):
    L_of_preferences = list()
    list_of_objects = list_of_all_objects(N)
    single_peak_branch(list_of_objects, L_of_preferences)
    return L_of_preferences

def L_couple_single_peaked_preferences(N):
    L_of_preferences = single_peaked_preferences(N)
    L_couple_of_preferences = list()

    for i in range(len(L_of_preferences)):
        for j in range(0, len(L_of_preferences)):
            L_couple_of_preferences.append((L_of_preferences[i], L_of_preferences[j]))
    return L_couple_of_preferences

# listalloc = list()
# single_peak_branch(listallobjects, listalloc)
#
# print("listalloc = ", listalloc)
# print("size = ",len(listalloc))

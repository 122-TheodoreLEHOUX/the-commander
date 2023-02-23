    
import numpy as np
import math

    
AA = np.array([[0,0],[1,0],[0,1],[1,1]])
BB = np.array([[2,2],[0,2],[2,0],[0,0]])
print(type(BB))
print(BB)
    
def distance(p0, p1): #Fonction de calcul de la distance entre deux points.
    print("hey")
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def sortArray(A:np.array,B:np.array): #permet de ranger 2 listes par proximité.
    i=0
    listA = []
    listB = []
    while i<len(A):
        j=0
        print("i",i)
        dist = distance(A[i],B[0])
        indice = 0
        while j<len(B):
            shortest = distance(A[i],B[j])
            if shortest<dist:
                indice = j
                dist = shortest
            j=j+1
        listA.append(A[i])
        listB.append(B[indice])
        B = np.delete(B, indice, 0)
        print("B:",B)
        i=i+1
    listA = np.array(listA)
    listB = np.array(listB)
    return listA,listB

print(sortArray(AA,BB))
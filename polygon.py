# a class file to define Units object representing combat units in the game.


from queue import Empty
import random
import scipy.spatial
import math
from random import randint
import numpy as np
import pandas
import geopandas
from numpy.linalg import norm 
from shapely.geometry import Polygon, multipolygon, LineString, Point, mapping

class Unit:
    def __init__(self,coo: list,color,force: int):
        self.target= np.array(coo)
        self.velocity=np.array([[0,0],[0,0],[0,0]],dtype=float)
        print(self.target.shape)
        self.velocity= np.resize(self.velocity, self.target.shape)
        print(self.velocity)
        self.coordinates = np.array(coo)
        self.color = color
        self.geo = Polygon([tuple(x) for x in coo])
        self.area = self.geo.area
        self.combatValue = force
        self.fight = []
       
    def resizeShape(self,shape):
        self.coordinates = np.resize(self.coordinates,shape)
        self.target = np.resize(self.target,shape)

    def updateForm(self,newCoo): # met à jour la forme du polygone avec de nouveaux coo
        self.coordinates = np.array(newCoo)
        forme = self.coordinates.shape
        self.resizeShape(forme)
        self.geo.buffer(0) #buffer pour "trier" le polygon
        
      
    def computeAngle(self,a,b):   #compute anglet between actual position and target
        if a[0] == b[0] and a[1] == b[1]:
            return [0,0]
        else:
            angle = math.atan2((b[1] - a[1]),(b[0] - a[0]))
            return [math.cos(angle),math.sin(angle)]
        
    def setVelocity(self): # update direction
        if np.array_equal(self.target,self.coordinates)==False :
            z=0
            while z < len(self.velocity):
                self.velocity[z] = np.array([self.computeAngle(self.coordinates[z],self.target[z])])
                z=z+1
        
    def move(self): #move
        SortedArray = self.sortArray(self.coordinates,self.target) #sort target and coordinates points so they are associates by proximity with each other.
        self.target = SortedArray[1] #return first array sorted
        self.coordinates = SortedArray[0]
        self.setVelocity()
        self.coordinates = self.coordinates + self.velocity
        self.geo = Polygon([(i[0], i[1]) for i in self.coordinates])

    def setTarget(self,newTarget): #define new target
        newTarget = np.array(newTarget)
        if len(newTarget) != len(self.coordinates):
            forme = (np.array(newTarget)).shape
            self.resizeShape(forme)
            self.target = newTarget
        else:
            self.target = newTarget
        
    def distance(self, p0, p1): #Compute distance between two points.
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def sortArray(self,A:np.array,B:np.array): #Sort two list by proximity bewteen each points.
        i=0
        listA = []
        listB = []
        while i<len(A):
            j=0
            dist = self.distance(A[i],B[0])
            indice = 0
            while j<len(B):
                shortest = self.distance(A[i],B[j])
                if shortest<dist:
                    indice = j
                    dist = shortest
                j=j+1
            listA.append(A[i])
            listB.append(B[indice])
            B = np.delete(B, indice, 0)
            i=i+1
        listA = np.array(listA)
        listB = np.array(listB)
        return listA,listB

    def collision(self,poly): # vérifie s'il y'a une collision à découper en deux
        if self.geo.intersects(poly.geo):
            self.geo = self.geo.buffer(0)
            poly.geo = poly.geo.buffer(0)
            intersection = self.geo.intersection(poly.geo)
            #print(intersection.is_valid)
            intersection = intersection.buffer(0)
            if intersection.geom_type == 'Polygon':
                geometry = self.geo.intersection(poly.geo)
                if geometry.area >1500:
                    return True
                else:
                    return False
            elif intersection.geom_type == 'multiPolygon':
                exit
                if geometry.area >1500:
                    return True
                else:
                    return False
            else : 
                return False
        else:
            return False
#Si point sur un segment alors il est supprimé
#Trier les points par proximité pour la target et la position.
    def transformation(self,poly):
        if self.collision(poly):
            intersection = self.geo.intersection(poly.geo)
            self.target = self.coordinates
            fight = self.combat(poly)
            self.velocity = self.velocity*0
            if fight == True: # problème les élèments et les targets sont mals associés.
                addition = self.geo.union(intersection)
                addition = list(addition.exterior.coords)
                difference = poly.geo.difference(intersection)
                difference = list(difference.exterior.coords)
                self.updateForm(addition)
                poly.updateForm(difference)
            elif fight == False:
                addition = poly.geo.union(intersection)
                addition = list(addition.exterior.coords)
                difference = self.geo.difference(intersection)
                difference = list(difference.exterior.coords)
                self.updateForm(difference)
                poly.updateForm(addition)
                
            else:
                pass


    def combat(self,poly): # détermine le combat
        rand = self.combatValue*random.randint(1, 2) - poly.combatValue*random.randint(1, 2)
        if rand <-5:
            return False
        elif rand > 5:
            return True
        else:
            return 'Draw'


class combatArea(): # classe pour gérer les combats
    def __init__(self,coo,color: tuple,p1: Unit,p2: Unit):
        self.Unit1 = p1
        self.Unit2 = p2
        self.coordinates = np.array(coo)
        self.color = color
        self.geo = Polygon([tuple(x) for x in coo])
        
    def IsTheSame(self, zone):
        if self.geo.intersects(zone.geo) != Empty : 
            return True
        else:
            return False
    
    def combat(self):
        rand = self.Unit1.combatValue*random.randint(1, 2) - self.Unit2.combatValue*random.randint(1, 2)
        if rand <-5:
            return False
        elif rand > 5:
            return True
        else:
            return 'Draw'

   

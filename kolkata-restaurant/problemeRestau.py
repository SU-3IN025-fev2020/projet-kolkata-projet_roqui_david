import numpy as np
import copy
import heapq
import Probleme
from Probleme import Probleme



def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
    """
    print("mana: ",p1[0]," mana2: ",p2,"  ")
    return abs(p1[0][0]-p2[0][0])+abs(p1[1][1]-p2[1][1]) 	

def randomPuzzle(n):
    """
    genere un taquin aleatoire de taille n
    """
    tiles = np.random.permutation(range(0,n**2)) # 0 is the empty slot
    puzzle = np.array(tiles)
    puzzle = np.reshape(puzzle,(n, n))
    return puzzle



    

###############################################################################


class ProblemeRestaurant(Probleme): 
    """ On definit un probleme du restaurant comme etant: 
        - un etat initial du taquin
        - un etat but du restaurant
        - une heuristique (supporte nombre de tiles, Manhattan, uniforme)
        """
    
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
    
    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            toujours 1 pour le taquin
            """
        return 1
       
    """
    def estBut(self,e):
    retourne vrai si l'etat e est un etat but
	return (self.but==e).all()
    """
    def estBut(self,e):
        """ retourne vrai si l'etat e est un etat but
        """
        return self.but==e
    
    def calculManhattan(self,t1,t2):
    	""" calcule la somme des distances de Manhattan entre 
    	    deux grille t1 et t2
    	    """
    	#print("t1 :",t1)
    	sommeMan = 0
    	sommeMan = sommeMan + distManhattan(t1,t2)
    	return sommeMan 

    #def calculManhattan(self,t1,t2):
    #    """ calcule la somme des distances de Manhattan entre 
    #        deux taquins t1 et t2
    #        """
    #	print("t1 :",t1)
    #    (s,_) = t1.shape
    #    sommeMan = 0
    #    for i in range(s): 
    #        for j in range(s):
    #            tile = t1[i][j]
    #            ([x],[y]) = np.where(t2==tile)      # where retourne les coord
    #            sommeMan += distManhattan((i,j),(x,y))
    #    return sommeMan  
        
    def calculPieces(self,e1,e2):
        """ au moins sommePieces doient etre deplaces pour arriver au but
        """
        
        (s,_) = e1.shape
        sommePieces=0
        for i in range(s): 
            for j in range(s):
                if e1[i][j] != e2[i][j]:
                    sommePieces+=1
        return sommePieces
        
    def h_value(self,e1,e2):
        """ applique l'heuristique pour le calcul 
            """
        if self.heuristique=='manhattan':
            h = self.calculManhattan(e1,e2)
        elif self.heuristique=='pieces':
            h = self.calculPieces(e1,e2)
        elif self.heuristique=='uniform':
            h = 1
        return h
       
    
        

        
    def successeurs(self,etat,actualPos):
        """ retourne une liste avec les taquins successeurs possibles
        """
        directions = ('g','d','h','b')
        listeSuc =[]
        
        swapApToAR = list(actualPos)

       
        print("newer pos: ", actualPos)   
        xposi = swapApToAR[0] + 1 #On affecte les differentes valeurs possibles de successeurs a des variables
        xneg = swapApToAR[0] - 1
        yposi = swapApToAR[1] + 1
        yneg = swapApToAR[1] - 1
        #On teste si les differentes valeurs possibles sont dans les valeurs permisent (pas les murs)
        for dir in directions:
            #print("etat: ", etat)
            if dir=='g':
                print("enter g")
                swapApToAR[0] = xneg
                potentSuc = tuple(swapApToAR)
                if(actualPos in etat):
                    print("enter enter g")
                    listeSuc.append(potentSuc)
            elif dir=='d':
                print("enter d")
                swapApToAR[0] = xposi
                potentSuc = tuple(swapApToAR)
                if(actualPos in etat):
                    print("enter enter d")
                    listeSuc.append(potentSuc)
            elif dir=='h':
                print("enter h")
                swapApToAR[0] = yposi
                potentSuc = tuple(swapApToAR)
                if(actualPos in etat):
                    print("enter enter h")
                    listeSuc.append(potentSuc)
            elif dir=='b':
                print("enter b")
                swapApToAR[0] = yneg
                potentSuc = tuple(swapApToAR)
                if(actualPos in etat):
                    print("enter enter b")
                    listeSuc.append(potentSuc)
            print("suceeees: ",listeSuc)
            return listeSuc
        
    def immatriculation(self,etat):
        """ genere une chaine permettant d'identifier un etat de maniere unique
            """
        s=""
        for l in etat:
            for c in l:  
                s+=str(c)
        return s

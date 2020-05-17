# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import Probleme
import pygame
import glo
import Noeud
import heapq
import random 
import numpy as np
import sys
import time
import problemeRestau


    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

#Méthode qui permet de retourner l'indice d'un élément préçis dans un tableau
def index_return(tab,elem):
    cpt = 0
    for i in tab:
        cpt += 1
        if(i == elem):
            return cpt
game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)
                        
    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 
    print("allowed states:", goalStates[1])
    
    problemeStates =  [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 
        
   
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------
        
    posPlayers = initStates

    
    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)
    time.sleep(5)
    print("fin du placement aléatoire des joueurs")

    #Pour chaque noeud à atteindre on cherche son emplacement dans le tableau de base puis on échange la positoin initale avec la position 
    #Finale dans le but de créer un tableau but 
    
    #-------------------------------
    # Création du tableau but
    #-------------------------------
    cptInit = 0
    for i in goalStates:
        cptInit += 1
        for x in range(nbLignes): 
            for y in range(nbColonnes):
                if(i == (x,y)):
                    print("indice: ",index_return(problemeStates,(x,y)))
                    print("init: ",initStates[cptInit])
                    print("actu: ",problemeStates[index_return(problemeStates,(x,y))])
                    problemeStates[index_return(problemeStates,(x,y))] = posPlayers[cptInit]
                    
    #print("Tableau but: ", problemeStates)
    print("diff: ",allowedStates[168]," ",problemeStates[168])
    
    
    #-------------------------------
    # Verification des différnce entre le tableau initial et le tableau but
    #-------------------------------
    
    cptTest = 0
    for x in range(nbLignes):
        
        for y in range(nbColonnes):
            #print("diff: ",problemeStates[cptTest]," ",allowedStates[cptTest])
            if(problemeStates[cptTest]!= allowedStates[cptTest]):
                print("ok3")
                print("diff: ",problemeStates[cptTest]," ",allowedStates[cptTest])
            cptTest += 1
    


    val = abs(posPlayers[0][0]-goalStates[0][0])+abs(posPlayers[1][1]-goalStates[1][1]) 
    print("vale: ",val)
    #sommeMan += distManhattan(,(x,y))
    #return sommeMan   

    p1 = problemeRestau.ProblemeRestaurant(allowedStates,problemeStates,'manhattan')  
    for w in range(nbPlayers):
        Probleme.astar(p1, posPlayers[w],True, False)
    
    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        c = random.randint(0,nbRestaus-1)
        #print(c)
        restau[j]=c
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    
    for i in range(iterations):
        
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]

            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()
    
                col=next_col
                row=next_row
                posPlayers[j]=(row,col)
            
      
        
            
            # si on est à l'emplacement d'un restaurant, on s'arrête
            if (row,col) == restau[j]:
                #o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Le joueur ", j, " est à son restaurant.")
               # goalStates.remove((row,col)) # on enlève ce goalState de la liste
                
                
                break
            
    
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    



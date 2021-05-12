# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:39:45 2021

@author: rayan
"""

import time
import numpy as np
from random import randint

# On définit le plateau
class Plateau:    
    def __init__(self,tab=np.array([[None for x in range(12)] for x in range(12)])):
        if (tab.shape!=(12,12)):
            self.tab=np.array([[None for x in range(12)] for x in range(12)])
        else:
            self.tab=tab    
    def __str__(self):
        msg=""
        for i in range(self.tab.shape[0]):
            for j in range(self.tab.shape[1]):
                if self.tab[i][j]==None:
                    msg+="_ "
                else:
                    msg+=str(self.tab[i][j])+" "
            msg+="\n"
        return msg

    
#%% Méthodes pour jouer


def Action(plateau):
    """On renvoie une liste contenant toutes les positions qui ne sont pas occupées"""
    l = []
    for i in range(plateau.tab.shape[0]):
        for j in range(plateau.tab.shape[1]):	
            if plateau.tab[i][j] == None:
                l.append([i,j])
    return l

def Result(plateau,a,symbolJoueur):
    """actualise le plateau du jeu en ajoutant le pion du joueur en a=[x,y]"""
    x,y=a[0],a[1]    
    plateau.tab[x][y]=symbolJoueur    
    return plateau


def Terminal_Test(plateau):
    """renvoie True si il y a un gagnant, False si il n'y en a pas et None si match nul"""
    # i,j sont les coord du pion qui vient juste d'être posé
    # on vérifie que le plateau n'est pas entièrement rempli
    plateauRempli=False
    caseVide=[x[i] for x in plateau.tab for i in range(12) if x[i]==None]
    if len(caseVide)==0:
        plateauRempli=True  

    # on vérifie sur les lignes qu'il n'y ait pas de gagnant
    presenceGagnant=False
    for i in range(plateau.tab.shape[0]):
        for j in range(plateau.tab.shape[1]-3):
            if(plateau.tab[i][j]==plateau.tab[i][j+1]==plateau.tab[i][j+2]==plateau.tab[i][j+3]!=None):
                presenceGagnant=True

    # on vérifie sur les colonnes qu'il n'y ait pas de gagnant   
    for j in range(plateau.tab.shape[1]):
        for i in range(plateau.tab.shape[0]-3):
            if(plateau.tab[i][j]==plateau.tab[i+1][j]==plateau.tab[i+2][j]==plateau.tab[i+3][j]!=None):
                presenceGagnant=True

    # on vérifie sur les diagonales à pentes positives qu'il n'y ait pas de gagnant
    for x in range(3,plateau.tab.shape[0]):
        for y in range(3,plateau.tab.shape[1]):
            for k in range (4):
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<4 and x-2+k<4 and x-1+k<4 and x+k<4 and y-3+k>-1 and y-2+k>-1 and y-1+k>-1 and y+k>-1 and y-3+k<4 and y-2+k<4 and y-1+k<4 and y+k<4):
                    if (plateau.tab[x-3+k][y-3+k]==plateau.tab[x-2+k][y-2+k]==plateau.tab[x-1+k][y-1+k]==plateau.tab[x+k][y+k]!=None):
                        presenceGagnant=True
    
    # on vérifie sur les diagonales à pentes négatives qu'il n'y ait pas de gagnant
    for x in range(3,plateau.tab.shape[0]):
        for y in range(plateau.tab.shape[1]-3):
            for k in range (4):
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<4 and x-2+k<4 and x-1+k<4 and x+k<4 and y+3-k>-1 and y+2-k>-1 and y+1-k>-1 and y-k>-1 and y+3-k<4 and y+2-k<4 and y+1-k<4 and y-k<4):
                    if (plateau.tab[x-3+k][y+3-k]==plateau.tab[x-2+k][y+2-k]==plateau.tab[x-1+k][y+1-k]==plateau.tab[x+k][y-k]!=None):                            
                        presenceGagnant=True

    # on affiche match None si il y a un match nul
    return None if plateauRempli==True and presenceGagnant==False else presenceGagnant


def Utility(plateau,symbolJoueur):#n'est utlisé que sur un plateau dont la partie est fini
    """met 0 pour un match nul, 1 si l'IA gagne et -1 si elle perd"""
    resultat=Terminal_Test(plateau)
    score=0
    if (resultat==True and symbolJoueur=="x"):
        score=10
    elif (resultat==True and symbolJoueur=="o"):
        score=-10
    return score

def MaxValue(plateau):
    """retourne le max des options que l'adversaire nous laisse jouer (parmis tous les min restant)"""
    value=-2000
    if (Terminal_Test(plateau)!=False):
        print("fin")
        return Utility(plateau,'o')
    else:
        for a in Action(plateau):
            Result(plateau, a,None)
            value=max(value,MinValue(Result(plateau,a,'x')))
            Result(plateau,a,None)
    return value

def MinValue(plateau):
    """retourne le min des options parmis tous les max restant"""
    value=2000
    if (Terminal_Test(plateau)!=False):
        return Utility(plateau,'x')
    else:
        for a in Action(plateau):
            Result(plateau, a,None)
            value=min(value,MaxValue(Result(plateau,a,'o')))
            Result(plateau,a,None)
            print(plateau)
    return value


    
# pb avec cette fonction car au lieu d'actualiser seulement le statetemp elle actualise aussi le state
def Decision(plateau):
    """retourne la décision de l'action que l'on va jouer sous forme de coordonnées de l'emplacement à jouer"""
    #plateau doit rester le même, on ne modifiera que copiePlateau qui servira pour les simulations
    
    print("plateau:\n",plateau,sep="")
    
    
    listePlaces=Action(plateau)
    maxAct=listePlaces[0]
    # valeurMax est la valeur max que le joueur peut obtenir en jouant son meilleur coup
    valeurMax=MinValue(Result(plateau,Action(plateau)[0],'x'))
    print("valeurMax: ",valeurMax)
    Result(plateau,maxAct,None)
    # on parcours toutes les actions pour retrouver celle qui correspond à ce meilleur coup
    for place in Action(plateau):
        print("action: ",place)
        if MinValue(Result(plateau,place,'x'))>valeurMax:
            valeurMax=MinValue(Result(plateau,place,'x'))
            maxAct=place
            print("valeurMax: ",valeurMax)
        Result(plateau, place,None)
    return maxAct
#%% Elagage alpha beta
def MaxValue_ab(plateau,alpha,beta):
    value=-2000
    if (Terminal_Test(plateau)!=False):
        print("fin")
        return Utility(plateau,'o')
    for a in Action(plateau):
        Result(plateau, a,None)
        value=max(value,MinValue_ab(Result(plateau,a,'x'),alpha,beta))
        print(plateau)
        Result(plateau, a,None)
        print("value: ",value)
        print("beta: ",beta)
        if value>=beta:
            return value
        alpha=max(alpha,value)
        print("alpha: ",alpha)
    return value

def MinValue_ab(plateau,alpha,beta):
    value=2000
    if (Terminal_Test(plateau)!=False):
        print("fin")
        return Utility(plateau,'x')
    for a in Action(plateau):
        Result(plateau, a,None)
        value=min(value,MaxValue_ab(Result(plateau,a,'o'),alpha,beta))
        print(plateau)
        Result(plateau, a,None)
        print("value2: ",value)
        print("alpha2: ",alpha)
        if value<=alpha:
            return value
        print("beta2: ",beta)
        beta=min(beta,value)
    return value            


def abSearch(plateau):
    value=MaxValue_ab(plateau,-2000, 2000)
    res=Action(plateau)[0]
    print(value)
    for a in Action(plateau):
        print("action: ",a)
        print(Utility(Result(plateau, a, 'x'),'x'))
        if value==MinValue_ab(Result(plateau,a,'x'),-2000, 2000):
        # if value==MaxValue(Result(plateau, a, 'x')):            
            res=a
        #     value=MinValue(Result(plateau,a,'o'))
        print(Result(plateau, a, 'x'))
        Result(plateau, a, None)  
    return res
    
#%% Elagage alpha beta + euristique

def MaxValue_ab_A(plateau,alpha,beta,profondeur):
    value=-2000
    if profondeur < 10:
        
        if (Terminal_Test(plateau)!=False):
            print("fin")
            return Utility(plateau,'o')
        for a in heuristique(plateau):
        #for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            print(profondeur)
            if (value == 10) :
                return value
            value=max(value,MinValue_ab_A(Result(plateau,a,'x'),alpha,beta,profondeur))
            print(plateau)
            Result(plateau, a,None)
            print("value: ",value)
            print("beta: ",beta)
            if value>=beta:
                return value
            alpha=max(alpha,value)
            print("alpha: ",alpha)
    print("valeur finale: ",value)
    return value

def MinValue_ab_A(plateau,alpha,beta,profondeur):
    value=2000
    if profondeur < 10:
        
        if (Terminal_Test(plateau)!=False):
            print("fin")
            return Utility(plateau,'x')
        for a in heuristique(plateau):
        #for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            print(profondeur)
            if (value == -10) :
                return value
            value=min(value,MaxValue_ab_A(Result(plateau,a,'o'),alpha,beta,profondeur))
            print(plateau)
            Result(plateau, a,None)
            print("value2: ",value)
            print("alpha2: ",alpha)
            if value<=alpha:
                return value
            print("beta2: ",beta)
            beta=min(beta,value)
    print("valeur finale: ",value)
    return value            


def abSearch_A(plateau):
    for a in heuristique(plateau):
    #for a in Action(plateau):
        # Joue vers le milieu du plateau si on est les premiers à jouer
        if ( len(Action(plateau)) == 12*12 ):
            r1 = randint(3,plateau.tab.shape[0]-4)
            r2 = randint(3,plateau.tab.shape[0]-4)
            return [[r1,r2]]
        else : 
            res=heuristique(plateau)[0]
            value=MaxValue_ab_A(plateau,-2000, 2000,0)
            print(value)
            print("action: ",a)
            print(Utility(Result(plateau, a, 'x'),'x'))
            if value==MinValue_ab_A(Result(plateau,a,'x'),-2000, 2000,0):
            # if value==MaxValue(Result(plateau, a, 'x')):            
                res=a
            #     value=MinValue(Result(plateau,a,'o'))
            print(Result(plateau, a, 'x'))
            Result(plateau, a, None)  
        return res

#retourne une liste d'action contenant les "meilleurs actions" en premier et les "mauvaises actions" en dernier
def heuristique(plateau):
    """ Ne marche que sur les plateau de taille au moins 7x7"""
    """On appelera, heuristique(plateau)"""
    """ Elle permet de regarder en premier les actions ayant le plus de potentiel """
    compteur = -1
    listeAction = Action(plateau)
    listeNote = [ 0 for x in range (len(Action(plateau))) ]
    

    for a in listeAction :
        compteur += 1
        ai = a[0]
        aj = a[1]

# Si une action est "évidente, optimal" on l'a renvoie
    
# Si la partie se termine en ajoutant une croix, on met l'action en tête de liste et on retourne la listes des actions
    
#%%  On regarde les colonnes ( pour les croix )
    

        # Extrémités supérieur
        
        if (ai == 0) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' ):
                listeNote[compteur] += 10000
            
        # Extrémités inférieur
        
        elif (ai == plateau.tab.shape[0]-1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' ):
                listeNote[compteur] += 10000
    

    
    # à une case du bord supérieur
    

        elif (ai == 1) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x'):
                listeNote[compteur] += 10000
    
    # à une case du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 10000
            
    # à deux cases du bord supérieur
    

        elif (ai == 2) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 10000
    
    # à deux cases du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 10000
            
    # à trois cases ou plus des bords (inférieur et supérieur)
    

        else :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x'):
                listeNote[compteur] += 10000
            

#%%  On regarde les lignes ( pour les croix )


        # Extrémités gauche
        
        if (aj == 0) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' ):
                listeNote[compteur] += 10000
            
        # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' ):
                listeNote[compteur] += 10000
    

    
    # à une case du bord gauche
    

        elif (aj == 1) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x'):
                listeNote[compteur] += 10000
    
    # à une case du bord droite
    

        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 10000
                
    # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 10000
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 10000
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x'):
                listeNote[compteur] += 10000
            
#%%  On regarde les diagonales à pentes négatives ( pour les croix )


        # Extrémités gauche

        if (aj == 0) : 
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            
        # à une case du bord gauche
    

        elif (aj == 1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            
        # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai-1][aj-1] == plateau.tab[ai-2][aj-2] == 'x' ):
                    listeNote[compteur] += 10000
   
            
   
    # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
    # à une case du bord droite
    
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] =='x' ):
                    listeNote[compteur] += 10000

#%%  On regarde les diagonales à pentes positives ( pour les croix )


        # Extrémités gauche

        if (aj == 0) : 
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            
        # à une case du bord gauche
    

        elif (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
        # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
   
            
   
        # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
        # à une case du bord droit
    
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
                
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX              

    # Si la partie se termine en jouant un rond sur une case, on met la case en tête de liste et on retourne la listes des actions
    
#%%  On regarde les colonnes ( pour les ronds )
    

        # Extrémités supérieur
        
        if (ai == 0) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' ):
                listeNote[compteur] += 5000
            
        # Extrémités inférieur
        
        elif (ai == plateau.tab.shape[0]-1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' ):
                listeNote[compteur] += 5000
    

    
    # à une case du bord supérieur
    

        elif (ai == 1) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o'):
                listeNote[compteur] += 5000
    
    # à une case du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 5000
            
    # à deux cases du bord supérieur
    

        elif (ai == 2) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 5000
    
    # à deux cases du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 5000
            
    # à trois cases ou plus des bords (inférieur et supérieur)
    

        else :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o'):
                listeNote[compteur] += 5000
            

#%%  On regarde les lignes ( pour les ronds )


        # Extrémités gauche
        
        if (aj == 0) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' ):
                listeNote[compteur] += 5000
            
        # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' ):
                listeNote[compteur] += 5000
    

    
    # à une case du bord gauche
    

        elif (aj == 1) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o'):
                listeNote[compteur] += 5000
    
    # à une case du bord droite
    

        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 5000
            
    # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 5000
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 5000
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o'):
                listeNote[compteur] += 5000
            
#%%  On regarde les diagonales à pentes négatives ( pour les ronds )


        # Extrémités gauche

        if (aj == 0) : 
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à une case du bord gauche
    

        elif (aj == 1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai-1][aj-1] == plateau.tab[ai-2][aj-2] == 'o' ):
                    listeNote[compteur] += 5000
   
            
   
    #     # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
    # # à une case du bord droite
    
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000

#%%  On regarde les diagonales à pentes positives ( pour les ronds )


        # Extrémités gauche

        if (aj == 0) : 
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à une case du bord gauche
    

        elif (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
        # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
   
            
   
        # Extrémités droite
        
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # à une case du bord droit
    
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
    
    
    #On priorise ensuite les actions où l'on gagne en deux tours
    
    
#%%  On regarde les colonnes ( victoire en deux tours )
    
    

    
    # à une case du bord supérieur
    

        if (ai == 1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 1000
    
            
    # à deux cases du bord supérieur
    

        elif (ai == 2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 1000
            
            
    # à une case du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 1000
            
    
    # à deux cases du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 1000
            
    # à trois cases ou plus des bords (inférieur et supérieur)
    

        else :
            if ( ai != 0 and ai != plateau.tab.shape[0]-1 ):    
                if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                    listeNote[compteur] += 1000
            

#%%  On regarde les lignes ( victoire en deux tours )

    
    # à une case du bord gauche
    

        if (aj == 1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 1000
    
            
    # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 1000
            
            
    # à une case du bord droit
    

        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 1000
            
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 1000
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj != 0 and aj != plateau.tab.shape[1]-1 ):         
                if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                    listeNote[compteur] += 1000

#%% On regarde les diagonales à pentes négatives ( victoire en deux tours )


    # à une case du bord gauche
        
    
        if (aj == 1) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
                
    # à deux cases du bord gauche
    

        if (aj == 2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
                
    # à une case du bord droit
    

        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à deux cases du bord droit
    

        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                        listeNote[compteur] += 1000
                        ###
                    
#%% On regarde les diagonales à pentes positives ( victoire en deux tours )


    # à une case du bord gauche
        
    
        if (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
                
    # à deux cases du bord gauche
    

        if (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
                
    # à une case du bord droit
    

        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
                
    # à deux cases du bord droit
    

        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                        listeNote[compteur] += 1000
                        

#%%  On regarde les colonnes ( défaite en deux tours )
    
    

    
    # à une case du bord supérieur
    

        if (ai == 1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 500
    
            
    # à deux cases du bord supérieur
    

        elif (ai == 2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 500
            
            
    # à une case du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 500
            
    
    # à deux cases du bord inférieur
    

        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 500
            
    # à trois cases ou plus des bords (inférieur et supérieur)
    

        else :
            if ( ai != 0 and ai != plateau.tab.shape[0]-1 ):    
                if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                    listeNote[compteur] += 500
            

#%%  On regarde les lignes ( défaite en deux tours )

    
    # à une case du bord gauche
    

        if (aj == 1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 500
    
            
    # à deux cases du bord gauche
    

        elif (aj == 2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 500
            
            
    # à une case du bord droit
    

        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 500
            
    
    # à deux cases du bord droit
    

        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 500
            
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj != 0 and aj != plateau.tab.shape[1]-1 ):         
                if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                    listeNote[compteur] += 500

#%% On regarde les diagonales à pentes négatives ( défaite en deux tours )


    # à une case du bord gauche
        
    
        if (aj == 1) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
                
    # à deux cases du bord gauche
    

        if (aj == 2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
                
    # à une case du bord droit
    

        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à deux cases du bord droit
    

        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                        listeNote[compteur] += 500
                        ###
                    
#%% On regarde les diagonales à pentes positives ( défaite en deux tours )


    # à une case du bord gauche
        
    
        if (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
                
    # à deux cases du bord gauche
    

        if (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
                
    # à une case du bord droit
    

        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
                
    # à deux cases du bord droit
    

        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
    # à trois cases ou plus des bords (gauche et droit)
    

        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                        listeNote[compteur] += 500
                
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX              
# S'il n'y as pas d'action "évidente", on triera la liste des actions en fonction des notes (qu'on zippera a la liste d'action pour les trier a la fin par note) :
    
    
    #On pénalise les actions sur les bords

        if ( ai == 0 or ai == plateau.tab.shape[0]-1):
            listeNote[compteur] -= 0.5
        if ( aj == 0 or aj == plateau.tab.shape[1]-1):
            listeNote[compteur] -= 0.5
    # Si l'action est a une case du bord, on de fait rien

        # if ( ai == 1 or ai == plateau.tab.shape[0]-2):
        #     listeNote[compteur] -= 0
        # if ( aj == 1 or aj == plateau.tab.shape[1]-2):
        #     listeNote[compteur] -= 0
      
    # On favorise les cases à deux cases du bord
    
        if ( ai == 2 or ai == plateau.tab.shape[0]-3):
            listeNote[compteur] += 0.25
        if ( aj == 2 or aj == plateau.tab.shape[1]-3):
            listeNote[compteur] += 0.25
            
    # On favorise les cases à trois cases ou plus du bord
    
        if ( ai >= 3 and ai <= plateau.tab.shape[0]-4):
            listeNote[compteur] += 0.5
        if ( aj >= 3 and aj <= plateau.tab.shape[1]-4):
            listeNote[compteur] += 0.5
      
    # La note variera surtout en fonction des cases adjacentes à l'action
    
    
    # On compte le nombre de cases différentes de None autour de l'action, plus il y en a, meilleur sera l'action
    
        # Cas où l'action est à trois cases ou plus du bord
        
        if ( ai >= 3 and ai <= plateau.tab.shape[0]-4 and aj >= 3 and aj <= plateau.tab.shape[1]-4):
            for k in range(ai-3,ai+4):
                for l in range(aj-3,aj+4):
                    if (plateau.tab[k][l] != None):
                        listeNote[compteur] += 0.25
                        
                        
                    
                    
            
            
    
    
    
     
    nStruct = list(zip(listeAction, listeNote))
    nStruct.sort(key = lambda tup : tup[1], reverse = True)
    listeAction = []
    for elem in nStruct:
        listeAction.append(elem[0])
    del listeAction[5:]
    return listeAction

# %% TESTS

plateau=Plateau()
plateau.tab=np.array([[None,None,None,None],
                     [None,None,None,'x'],
                     [None,None,None,'x'],
                     [None,None,None,'x']])

# plateau.tab=np.array([['x','o',None,None,'x',None,'x','o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,None,'o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None]])

plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None]])

plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,'x',None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,'x',None,None,None,None,None],
                      [None,'x',None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,'x',None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,'x',None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None]])


plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,'x',None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,'x',None,None,None],
                      [None,'x',None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,'o',None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,'x','o','x',None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None]])


# plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,'o',None,None,None,None,None,None],
#                       [None,None,None,'o','x','x','o',None,None,None,None,None],
#                       [None,None,None,'x',None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None]])

# plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,'x',None,None,None,None,None,None,None],
#                       [None,None,None,None,'o',None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,'o','x','o','x',None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None],
#                       [None,None,None,None,None,None,None,None,None,None,None,None]])


plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,'o','o',None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None]])


# plateau.tab=np.array([['x','o',None,None,'x',None,'x','o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,None,'o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None]])



#Affichache du tableau : MARCHE
print(plateau) 
#Terminal_Test : MARCHE
#print(Terminal_Test(plateau)) 

#Méthode Action : MARCHE
# print(Action(plateau))
 
#Méthode Result : MARCHE
# print("pTest avant\n",plateau,sep="")
# Result(plateau.tab,[0,5],"x")
# print("pTest après\n",plateau,sep="")

#Méthode utility : MARCHE
# print(Utility(plateau,'x'))
# print(MinMax(plateau,'x'))
# print(Action(plateau))
# print(Result(plateau,Decision(plateau,'x'),'x'))

#Les deux méthodes de recherche
# print(Decision(plateau))
temps1 = time.time()
print(abSearch_A(plateau))
temps2 = time.time()
print("Temps d'execution :",temps2-temps1)
#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n",heuristique(plateau))

# a = [1,5]
# b = [4,7]
# c = [0,2]
# L = [ a,b,c ]
# print(L)
# L.remove(b)
# print(L)
# L.insert(0,b)
# print(L)
# del L[1:]
# print(L)

# def toto(a):

#     if a > 10 :
#         if a == 15:
#             return a
#     else:
#         if a == 3:
#             return a
#     if a == 12:
#         return a
#     return 5
        
#print(toto(12)) 
#print(plateau.tab.shape[0])
ai = 1
aj = 0
# print(plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'x')
# print(len([[2,0]]))
# x1 = (1)
# x2 = "[3,4]"
# nStruct = dict(zip([x1,x2], [4,6]))
#nStruct = { k:v for (k,v) in (listeAction, listeNote)}
#nStruct = { k:v for (k,v) in ([[1,2],[3,4]], [4,6])}
# print(nStruct)
# nStruct.sort(key = lambda tup : tup[1])
#         self.population = []
#     for elem in nStruct:
#         self.population.append(elem[0])
# print(list(x2))
#print([ 0 for x in range(3)])
# l = [1,2,2,7]
# l[0] += 1
# print(l)
a= heuristique(plateau)
print(a)

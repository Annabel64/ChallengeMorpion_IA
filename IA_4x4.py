# -*- coding: utf-8 -*-
"""
Created on Wed May  5 20:15:47 2021

@author: victo
"""

import numpy as np
# On définit le plateau
class Plateau:    
    def __init__(self,tab=np.array([[None for x in range(4)] for x in range(4)])):
        if (tab.shape!=(12,12)):
            self.tab=np.array([[None for x in range(4)] for x in range(4)])
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
    caseVide=[x[i] for x in plateau.tab for i in range(4) if x[i]==None]
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
    if profondeur <15:
        
        if (Terminal_Test(plateau)!=False):
            print("fin")
            return Utility(plateau,'o')
        for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            print(profondeur)
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
    if profondeur <15:
        
        if (Terminal_Test(plateau)!=False):
            print("fin")
            return Utility(plateau,'x')
        for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            print(profondeur)
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
    value=MaxValue_ab_A(plateau,-2000, 2000,0)
    res=Action(plateau)[0]
    print(value)
    for a in Action(plateau):
        print("action: ",a)
        print(Utility(Result(plateau, a, 'x'),'x'))
        if value==MinValue_ab_A(Result(plateau,a,'x'),-2000, 2000,0):
        # if value==MaxValue(Result(plateau, a, 'x')):            
            res=a
        #     value=MinValue(Result(plateau,a,'o'))
        print(Result(plateau, a, 'x'))
        Result(plateau, a, None)  
    return res


# %% TESTS

plateau=Plateau()
plateau.tab=np.array([['x','x','o','x'],
                     [None,None,'o',None],
                     [None,None,'o',None],
                     [None,None,None,None]])
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
print(Terminal_Test(plateau)) 

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

print(abSearch_A(plateau))
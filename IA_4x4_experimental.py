# -*- coding: utf-8 -*-
"""
Created on Wed May  5 20:15:47 2021

@author: victo
"""

import numpy as np
import time
import random as rd
# On définit le plateau
class Plateau:    
    def __init__(self,tab=None):
        if (tab==None or tab.shape!=(12,12)):
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
    valeurMax=MinValue(Result(plateau,Action(plateau)[0],'x'))
    Result(plateau,maxAct,None)
    for place in Action(plateau):
        print("action: ",place)
        if MinValue(Result(plateau,place,'x'))>valeurMax:
            valeurMax=MinValue(Result(plateau,place,'x'))
            maxAct=place
        Result(plateau, place,None)
    return maxAct


#%% Elagage alpha beta
def MaxValue_ab(plateau,alpha,beta,profondeur):
    value=-2000
    if (Terminal_Test(plateau)!=False or profondeur>5):
        # print("fin")
        return Utility(plateau,'o')
    for a in Action(plateau):
        Result(plateau, a,None)
        profondeur+=1
        value=max(value,MinValue_ab(Result(plateau,a,'x'),alpha,beta,profondeur))
        # print(plateau)
        Result(plateau, a,None)
        if value>=beta:
            return value
        alpha=max(alpha,value)
    return value

def MinValue_ab(plateau,alpha,beta,profondeur):
    value=2000
    if (Terminal_Test(plateau)!=False or profondeur>5):
        # print("fin")
        return Utility(plateau,'x')
    for a in Action(plateau):
        Result(plateau, a,None)
        profondeur+=1
        value=min(value,MaxValue_ab(Result(plateau,a,'o'),alpha,beta,profondeur))
        # print(plateau)
        Result(plateau, a,None)
        if value<=alpha:
            return value
        beta=min(beta,value)
    return value            


def abSearch(plateau,profondeur):
    t1=time.time()
    value=MaxValue_ab(plateau,-2000, 2000,profondeur)
    res=Action(plateau)[0]
    print("value max que l'on peut obtenir avec cette limite de profondeur': ",value)
    for a in Action(plateau):
        # print("action: ",a)
        # print(Utility(Result(plateau, a, 'x'),'x'))
        if value==MinValue_ab(Result(plateau,a,'x'),-2000, 2000,profondeur):
              
            res=a
        #     value=MinValue(Result(plateau,a,'o'))
        # print(Result(plateau, a, 'x'))
        Result(plateau, a, None)  
        t2=time.time()
        # print("Le temps d'éxécution est de :",t2-t1,"s")
    return res
    
# def Choix(plateau,symbolJoueur):
#     """retourne le meilleur coup"""
#     #--> le meilleur coup est celui qui retourne Utility(joueur)=1 ou qui empeche Utility(adversaire)=1
#     #on privilégie l'attaque si elle permet de gagner
#     #si on ne peut pas gagner, on privilégie la défence si elle permet de ne pas perdre
#     #si on ne peut pas perdre ni gagner, on attaque
    
#     #on copie le plateau pour éviter de le modifier accidentellement
#     copiePlateau=Plateau()
#     copiePlateau.tab=np.array(plateau.tab)
    
#     symbolAdversaire=''
#     if symbolJoueur=='x':symbolAdversaire='o'
#     else: symbolAdversaire='x'
    
#     listePlaces=Action(plateau) #liste des places libres à jouer
#     meilleurCoup=listePlaces[0]
        
       
#     # 1) on recherche le meilleur coup ie. si une place peut nous faire gagner
#     for place in listePlaces:
#         #si le utility de la place vaut 1, meilleurcoup=place
#         if(Utility(Joue(copiePlateau,place,symbolJoueur),symbolJoueur)==1):
#             meilleurCoup=place
#             break;
#             #on arrête le programme, le coup qui permet de gagner a été trouvé
#         copiePlateau.tab=np.array(plateau.tab)

    
#     # 2) si le meilleur coup ne peut pas nous faire gagner, on regarde si un coup de l'ennemi peut nous faire perdre
#     if Utility(Joue(copiePlateau,meilleurCoup,symbolJoueur),symbolJoueur)==0:
#         for place in listePlaces:
#         #si le utility de la place vaut 1, ie. l'adversaire peut gagner, on doit jouer à cette place: meilleurcoup=place
#             if(Utility(Joue(copiePlateau,place,symbolAdversaire),symbolAdversaire)==1):
#                 meilleurCoup=place
#                 break;
#                 # on arrête le programme, le coup qui permet de ne pas perdre a été trouvé
#             copiePlateau.tab=np.array(plateau.tab)
        
        
#     # 3) si aucun coup ne peut ni nous faire gagner ni empêcher qu'on perde, on va placer un pion là où la densité de nos pions est maximale
#     if Utility(Joue(copiePlateau,meilleurCoup,symbolAdversaire),symbolAdversaire)==0:
#             meilleurCoup=1


#     return meilleurCoup
        
        
# def MinMax(plateau,symbolJoueur):
#     """retourne l'utility du meilleur coup"""
    
#     #A FAIRE : je veux retourner une liste des meilleurs coups à faire
#     #méthode récursive
    
#     if Terminal_Test(plateau):
#         return Utility(plateau,symbolJoueur)
    
#     elif symbolJoueur=='x':
#         extr = MinMax(Result(plateau,Action(plateau)[0],symbolJoueur),symbolJoueur)
#         # print(extr)
#         Result(plateau,Action(plateau)[0],None)
#         for i in Action(plateau):
#             # print(MinMax(Result(plateau,i,symbolJoueur),symbolJoueur),extr,"\n")
            
#             if MinMax(Result(plateau,i,symbolJoueur),symbolJoueur)>extr:
#                 Result(plateau,i,None)
#                 extr = MinMax(Result(plateau,i,symbolJoueur),symbolJoueur)
                
#             Result(plateau,i,None)
#         return extr
#     else :
#         extr = MinMax(Result(plateau,Action(plateau)[0],symbolJoueur),symbolJoueur)
#         Result(plateau,i,None)
#         for i in Action(plateau):
#             # print(MinMax(Result(plateau,i,symbolJoueur),symbolJoueur),extr,"\n")
#             if MinMax(Result(plateau,i,symbolJoueur),symbolJoueur)<extr:
#                 Result(plateau,i,None)
#                 extr = MinMax(Result(plateau,i,symbolJoueur),symbolJoueur)
                
#             Result(plateau,i,None)
#         return extr


#%% BOUCLE FINALE


def BoucleFinale():
    plateau=Plateau()    
    # plateau.tab=np.array([['x','o',None,'x','x',None,'x','o','x',None,'x','o'],
    #                   ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
    #                   ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
    #                   ['o',None,'o',None,None,None,'o',None,'o','x','o',None],
    #                   ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
    #                   ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
    #                   ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
    #                   ['o',None,'o',None,'o','x','o',None,'o','x','o',None],
    #                   ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
    #                   ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
    #                   ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
    #                   ['o',None,'o',None,None,'x','o',None,'o','x','o',None]])
    tour=1
    i=-1
    j=-1
    while not Terminal_Test(plateau):        
        print("Tour numéro ",tour,' :\n')
        print(plateau)
        
        if(tour%2==0):
            symbolJoueur='x'
            if (tour <10):
                print("i: ",i," j: ",j)
                i=rd.randint(max(0,i-4),min(11,i+4))
                j=rd.randint(max(0,j-4),min(11,j+4))
                while (plateau.tab[i][j]!=None):
                    i=rd.randint(max(0,i-4),min(11,i+4))
                    j=rd.randint(max(0,j-4),min(11,j+4))
                coup=[i,j]
            else:
                #on détermine le meilleur coup à jouer grâce à MinMax
                coup=abSearch(plateau,0)   
            print("coup",coup)
            plateau=Result(plateau, coup, symbolJoueur)
            
        else:
            symbolJoueur='o'
            
            #on demande à l'utilisateur où veut-il placer son pion
            i=int(input("Veuillez saisir i"))
            j=int(input("Veuillez saisir j"))
            coup=[i,j] #juste pour le test
            
            plateau=Result(plateau, coup, symbolJoueur)
            
        tour+=1
    print(plateau)
    if(Terminal_Test(plateau)==None):
        print("Match nul")
    else :
        #méthode afin de déterminer le gagnant : est-ce qu'on modifie Terminal_Test ? Nouvelle méthode ?
        if(tour%2==0): # alors le prochain a joué est 'x' donc celui qui vient de jouer est 'o'
            print('Le joueur avec les pions "o" a gagné')
        else:
            print('Le joueur avec les pions "x" a gagné')
    

# %% TESTS

# plateau=Plateau()
# plateau.tab=np.array([[None,None,None,None],
#                      [None,None,None,None],
#                      [None,None,None,None],
#                      [None,None,None,None]])

# plateau.tab=np.array([['x','o',None,'x','x',None,'x','o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,None,'o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o',None,'o','x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o',None,'o','x',None,'x','o'],
#                       ['o',None,'o','x',None,'x','o',None,'o','x','o',None],
#                       ['x','o',None,None,'x','o','x','o','x',None,'x','o'],
#                       ['o',None,'o',None,None,'x','o',None,'o','x','o',None]])


#Affichache du tableau : MARCHE
# print(plateau) 
#Terminal_Test : MARCHE
# print(Terminal_Test(plateau)) 

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

# print(abSearch(plateau,10))

BoucleFinale()
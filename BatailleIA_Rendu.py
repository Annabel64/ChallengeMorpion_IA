# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:39:45 2021

@author: rayan
"""
import numpy as np

#%% A faire dans l'ordre

#méthode de décision (minmax)
#programme final qui regroupe tout
#faire ça : "Les IA devront reposer sur un Minimax avec id´ealement un ´elagage Alpha-Beta" (faire en sorte de ne pas regarder les options inintéressantes)
#retester dans le programme final
#euristique (repérer là où est la densité la plus importante de pions ennemis, pour repérer la zone la plus "dangereuse" pour nous))
#l'intégrer

#%% classe Plateau

# symbolJoueur vaut soit "x" soit "o"

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
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y-3+k>-1 and y-2+k>-1 and y-1+k>-1 and y+k>-1 and y-3+k<12 and y-2+k<12 and y-1+k<12 and y+k<12):
                    if (plateau.tab[x-3+k][y-3+k]==plateau.tab[x-2+k][y-2+k]==plateau.tab[x-1+k][y-1+k]==plateau.tab[x+k][y+k]!=None):
                        presenceGagnant=True
    
    # on vérifie sur les diagonales à pentes négatives qu'il n'y ait pas de gagnant
    for x in range(3,plateau.tab.shape[0]):
        for y in range(plateau.tab.shape[1]-3):
            for k in range (4):
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y+3-k>-1 and y+2-k>-1 and y+1-k>-1 and y-k>-1 and y+3-k<12 and y+2-k<12 and y+1-k<12 and y-k<12):
                    if (plateau.tab[x-3+k][y+3-k]==plateau.tab[x-2+k][y+2-k]==plateau.tab[x-1+k][y+1-k]==plateau.tab[x+k][y-k]!=None):                            
                        presenceGagnant=True

    # on affiche match None si il y a un match nul
    return None if plateauRempli==True and presenceGagnant==False else presenceGagnant


def Utility(plateau,symbolJoueur):#n'est utlisé que sur un plateau dont la partie est fini
    """met 0 pour un match nul, 1 si l'IA gagne et -1 si elle perd"""
    resultat=Terminal_Test(plateau)
    score=0
    if (resultat==True and symbolJoueur=="x"):
        score=1
    elif (resultat==True and symbolJoueur=="o"):
        score=-1
    return score

# def MaxValue(plateau,symbolJoueur):
#     """retourne le max des options que l'adversaire nous laisse jouer (parmis tous les min restant)"""
#     value=-200
#     if (Terminal_Test(plateau)!=False):
#         print("fin")
#         return Utility(plateau,symbolJoueur)
#     else:
#         for a in Action(plateau):
#             value=max(value,MinValue(Joue(plateau,a,'x'),symbolJoueur))
#     return value

# def MinValue(plateau,symbolJoueur):
#     """retourne le min des options parmis tous les max restant"""
#     value=200
#     if (Terminal_Test(plateau)!=False):
#         return Utility(plateau,symbolJoueur)
#     else:
#         for a in Action(plateau):
#             value=min(value,MaxValue(Joue(plateau,a,'x'),symbolJoueur))
#     return value


# # pb avec cette fonction car au lieu d'actualiser seulement le statetemp elle actualise aussi le state
# def Decision(plateau,symbolJoueur):
#     """retourne la décision de l'action que l'on va jouer sous forme de coordonnées de l'emplacement à jouer"""
#     #plateau doit rester le même, on ne modifiera que copiePlateau qui servira pour les simulations
#     copiePlateau=plateau
#     print("plateau:\n",plateau,sep="")
#     print("copiePlateau:\n",copiePlateau,sep="")
    
#     listePlaces=Action(plateau)
#     maxAct=listePlaces[0]
#     valeurMax=MaxValue(copiePlateau,symbolJoueur)
    
#     for place in Action(plateau):
#         print("action: ",place)
#         if MaxValue(Joue(copiePlateau,place,'x'),symbolJoueur)<valeurMax:
#             maxAct=place
#     return maxAct


            

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
        
        
def MinMax(plateau,symbolJoueur,rslt=0):
    """retourne le nombre de coups au prochain tour qui peuvent mener à la victoire finale"""
    #méthode récursive
    #retourne le Utility() du meilleur coup
    if Terminal_Test(plateau):
        return rslt+Utility(plateau,symbolJoueur)
    
    elif symbolJoueur=='x':
        extr = MinMax(Result(plateau,Action(plateau)[0],symbolJoueur),symbolJoueur,rslt+1)
        for i in Action(plateau):
            if MinMax(Result(plateau,i,symbolJoueur),symbolJoueur,rslt)>extr:
                extr = MinMax(Result(plateau,i,symbolJoueur),symbolJoueur,rslt+1)
        return extr
    else :
        extr = MinMax(Result(plateau,Action(plateau)[0],symbolJoueur),symbolJoueur,rslt)
        for i in Action(plateau):
            if MinMax(Result(plateau,i,symbolJoueur),symbolJoueur,rslt-1)<extr:
                extr = MinMax(Result(plateau,i,symbolJoueur),symbolJoueur,rslt-1)
        return extr






# %% TESTS

    
plateau=Plateau()
plateau.tab=np.array([['x','x','x',None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,'x',None,None,None,None,None,None],
                      [None,None,None,None,None,'o',None,None,None,None,None,None],
                      [None,None,None,'o',None,'x',None,None,None,None,None,None],
                      [None,None,None,None,None,'x',None,'x','x',None,None,None],
                      [None,None,None,None,None,'o',None,'o','o',None,None,None],
                      [None,None,'x',None,None,None,'o',None,None,None,None,None],
                      [None,None,None,'x',None,None,'o',None,None,None,None,None],
                      ['o',None,None,None,'x',None,None,None,None,None,None,None],
                      [None,'o',None,None,None,None,None,None,'o',None,None,None],
                      [None,None,'x',None,None,None,None,None,None,'o',None,None],
                      [None,'x',None,'o',None,None,None,None,None,None,None,None]])




#Affichache du tableau : MARCHE
print(plateau) 
#Terminal_Test : MARCHE
# print(Terminal_Test(plateau)) 

#Méthode Action : MARCHE
#print(Action(plateau.tab))
 
#Méthode Result : MARCHE
# print("pTest avant\n",plateau,sep="")
# Result(plateau.tab,[0,5],"x")
# print("pTest après\n",plateau,sep="")

#Méthode utility : MARCHE
#print(Utility(plateau,'x'))

print(MinMax(plateau,'x'))
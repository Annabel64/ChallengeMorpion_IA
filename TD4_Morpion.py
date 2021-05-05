# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:50:19 2021

@author: Annabel
"""
import random

import numpy as np

#%% Code Antoine

# On définit le plateau de jeu
class Morpion:
	def __init__(self,tab=None):
		if (tab ==None)or tab.shape!=(3,3):
			self.tab= np.array([[None,None,None],[None,None,None],[None,None,None]])
		else:
			self.tab = tab
	
	def __str__(self):
		msg = ""
		for i in self.tab:
			if i == None:
				msg += " "
			else:
				msg += str(i)
		return msg

# On renvoie une liste contenant toutes les positions qui ne sont pas occupés
# s est le plateau
def Action(s):
	l = []
	for i in range(s.shape[0]):
		for j in range(s.shape[1]):	
			if s[i][j] == None:
				l.append([i,j])
	return l

#On joue le pion sur l'emplacement 
# s est le plateau et a?
def Result(s,a):
	s[a[0]][a[1]]=a[2]
	return s

def Terminal_Test(s):
    #test si le jeu est fini ou non
	flag = True
    # On teste si il y a au moins un emplacement de vide
	for i in range(s.shape[0]):
		for j in range(s.shape[1]):	
			if s[i][j] == None:
				flag = False
    # si il y a au moins un emplacement de vide on regarde si il y a 3 pions alignés
	if not flag:
		for j in range(s.shape[1]):
			#colonnes
			flagTemp = True
			for i in range(s.shape[0]-1):
				if (s[i][j]!=s[i+1][j])or(s[i][j]==None):
					flagTemp = False
			flag = flag	or flagTemp	
		if not flag :
			for i in range(s.shape[0]):
				#lignes
				flagTemp = True
				for j in range(s.shape[1]-1):
					if (s[i][j]!=s[i][j+1])or(s[i][j]==None):
						flagTemp = False
				flag = flag or flagTemp
			if not flag :
				flag = True
				for i in range(min(s.shape[0]-1,s.shape[1]-1)):
					if (s[i][i]!=s[i+1][i+1])or(s[i][j]==None):
						flag = False
				if not flag:
					flag = True
					n = s.shape[0]
					for i in range(min(s.shape[0]-1,s.shape[1]-1)):
						if (s[n-i-1][i]!=s[n-i-2][i+1])or(s[n-i-1][i]==None):
							flag = False
	return flag
			
def Utility(s):
    #note la fiche de morpion (1 si gagné, 0 si match null, -1 si perdu)
	res = 0
	flag = False
	for j in range(s.shape[1]):
		#colonnes
		flagTemp = True
		for i in range(s.shape[0]-1):
			if (s[i][j]!=s[i+1][j])or(s[i][j]==None):
				flagTemp = False
		if flagTemp :
			if s[0][j] == "X":
				res = 1
			else:
				res = -1
		flag = flag or flagTemp
	if not flag:
		for i in range(s.shape[0]):
			#lignes
			flagTemp = True
			for j in range(s.shape[1]-1):
				if (s[i][j]!=s[i][j+1])or(s[i][j]==None):
					flagTemp = False
			if flagTemp:
				if s[i][0]=="X":
					res = 1
				else:
					res = -1
			flag = flag or flagTemp
		if not flag:
			flag = True
			for i in range(min(s.shape[0]-1,s.shape[1]-1)):
				if (s[i][i]!=s[i+1][i+1])or(s[i][j]==None):
					flag = False
			if flag:
				if s[0][0]=="X":
					res=1
				else:
					res = -1
			if not flag:
				flag = True
				n = s.shape[0]
				for i in range(min(s.shape[0]-1,s.shape[1]-1)):
					if (s[n-i-1][i]!=s[n-i-2][i+1])or(s[n-i-1][i]==None):
						flag = False
				if flag:
					if s[n-1][0]=="X":
						res = 1
					else:
						res = -1
	return res
		
def MinMax(s):
    #méthode récursive
    #retourne le Utility() du meilleur coup
	if Terminal_Test(s):
		return Utility(s)
	elif (np.count_nonzero(s == "X"))<=(np.count_nonzero(s == "O")): #pour savoir à qui c'est le tour
		extr = MinMax(Result(s,Action(s)[0]+["X"]))
		for i in Action(s):
			if MinMax(Result(s,i+["X"]))>extr:
				extr = MinMax(Result(s,i+["X"]))
		return extr
	else :
		extr = MinMax(Result(s,Action(s)[0]+["O"]))
		for i in Action(s):
			if MinMax(Result(s,i+["O"]))<extr:
				extr = MinMax(Result(s,i+["O"]))
		return extr

mp = Morpion(np.array([["X",None,None],[None,None,None],[None,None,None]]))

print(MinMax(mp.tab))


#%% ma méthode (sans minmax)

def action(plateau,perso):#perso='O' ou 'X'
    n=-1
    while (n==-1 or plateau[n][1]==True):
        n=random.randint(0,8)
    plateau[n]=[perso,True]
    return plateau

def testFin(plateau):
    fin=False
    gagnant=""
    
    #Si on a des diagonales
    if(plateau[0][0]==plateau[4][0] and plateau[0][0]==plateau[8][0] and plateau[0][1]==True and plateau[4][1]==True and plateau[8][1]==True):
        fin=True
        gagnant=plateau[0][0]
    elif(plateau[2][0]==plateau[4][0] and plateau[2][0]==plateau[6][0] and plateau[2][1]==True and plateau[4][1]==True and plateau[6][1]==True):
        fin=True
        gagnant=plateau[2][0]
    
    else : 
        #Si on a des colonnes de sigles alignées
        for i in range(3): 
            if(plateau[i][0]==plateau[i+3][0] and plateau[i][0]==plateau[i+6][0] and plateau[i][1]==True and plateau[i+3][1]==True and plateau[i+6][1]==True):
                fin=True
                gagnant=plateau[i][0]
                
        #Si on a des lignes de sigles alignées
        for i in range(0,9,3): 
            if(plateau[i][0]==plateau[i+1][0] and plateau[i][0]==plateau[i+2][0] and plateau[i][1]==True and plateau[i+1][1]==True and plateau[i+2][1]==True):
                fin=True
                gagnant=plateau[i][0]
        
        #Si toutes les cases sont remplies et qu'on a un match nul
        n=0
        for i in range(8):
            if plateau[i][1]==True:
                n+=1
        if n==9:
            fin=True
                
    return fin,gagnant

def resultat(perso,plateau):
    res=0
    if(perso=='O'):
        print("Les O ont gagné : +1")
        res=1
    elif(perso=='X'):
        print("Les X ont gagné : -1")
        res=-1
    else:
        print("Match nul : 0")
    return res


def morpion():
    plateau=[['',False],['',False],['',False],['',False],['',False],['',False],['',False],['',False],['',False]]
    fin,perso=testFin(plateau)
    print("Les O commencent.\n")
    n=0 #nombre de tours nécessaires
    while not fin:
        n+=1
        plateau=action(plateau, 'O')
        #print(plateau,'\n')
        fin,perso=testFin(plateau)
        
        plateau=action(plateau,'X')  
        #print(plateau,'\n')
        fin,perso=testFin(plateau)
    resultat(perso,plateau)


    
# morpion()

# %%% VERSION ROMANE NE MARCHE PAS



import numpy as np

def MaxValue(state,joueur):
    value=-200
    if (Terminal(state)[0]!=False):
        print("fin")
        return Utility(state,joueur)
    else:
        for a in Actions(state):
            value=max(value,MinValue(Result(state,a,joueur),joueur))
    return value

def MinValue(state,joueur):
    value=200
    if (Terminal(state)[0]!=False):
        return Utility(state,joueur)
    else:
        for a in Actions(state):
            value=min(value,MaxValue(Result(state,a,joueur),joueur))
    return value

# pb avec cette fonction car au lieu d'actualiser seulement le statetemp elle actualise aussi le state
def Decision(state2,joueur): 
    statetemp=[x for x in state2]
    print("statetemppp: ",statetemp)
    print("stat: ",state2)
    maxAct=None
    print("statetemppp: ",statetemp)
    print("stat: ",state2)
    valeurMax=MaxValue(statetemp,joueur)
    print("statetemppp: ",statetemp)
    print("stat: ",state2)
    
    print("maxxx",valeurMax)
    print("stateee: ",state2)
    for a in Actions(state2):
        print("actionnn: ",a)
        print("dddddd",MaxValue(Result(statetemp,a,joueur),joueur))
        if MaxValue(Result(statetemp,a,joueur),joueur)==valeurMax:
            maxAct=a
    return maxAct
    

print(Decision(plateauTest,1))    

plateau=np.zeros((3,3))
plateauTest=[[-1,1,0],[1,0,1],[-1,-1,1]]

# un état est la disposition d'un plateau avec les cases remplies et vides
# exemple de state:[[1,2,1],[1,2,0],[0,0,0]]
# -1 pour l'adversaire et 1 pour nous

def Actions(plateau):
    act=[]
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if plateau[i][j]==0:
                act.append([i,j])
    return act


def Terminal(plateau):
    res=False
    symbolJoueur=0
    partieTerminee=False
    # on gère les colonnes
    if (plateau[0][0]==plateau[1][1]==plateau[2][2]!=0):
        res=True
        symbolJoueur=plateau[0][0]
    elif (plateau[0][2]==plateau[1][1]==plateau[2][0]!=0):
        res=True
        symbolJoueur=plateau[0][2]
    # on gère les lignes
    for i in plateau:
        if(i[0]==i[1]==i[2]!=0):
            res=True
            symbolJoueur=i[1]
    # on gère les colonnes
    for j in range(3):
        if (plateau[0][j]==plateau[1][j]==plateau[2][j]!=0):
            res=True
            symbolJoueur=plateau[1][j]
    # match nul
    presenceZero=[x[i] for x in plateau for i in range(3) if x[i]==0]
    if len(presenceZero)==0:
        partieTerminee=True    
    return None if partieTerminee==True and res==False else res,symbolJoueur


def Utility(plateau,joueur):
    resultatPartie=0
    res=Terminal(plateau)
    if (res[0]==None):
        # match nul
        resultatPartie+=1
    else:
        if (res[1]==joueur):
            # le joueur a gagné
            resultatPartie+=10
        else:
            # le joueur a perdu
            resultatPartie-=10
    return resultatPartie
        

def Result(plateau,a,joueur):
    plateau[a[0]][a[1]]=joueur
    return plateau
    
# joueur1 est l'IA (max)
def Minmax(plateau,joueur1,joueur2):
    joueur=joueur1
    if (Terminal(plateau)):
        return Utility(plateau,joueur)
    elif(joueur==joueur1):
        Decision(plateau)
    else:
        Decision(plateau)




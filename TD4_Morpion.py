# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:50:19 2021

@author: Annabel
"""
import random

import numpy as np

#%% Code Antoine
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
	
def Action(s):
	l = []
	for i in range(s.shape[0]):
		for j in range(s.shape[1]):	
			if s[i][j] == None:
				l.append([i,j])
	return l

def Result(s,a):
	s[a[0]][a[1]]=a[2]
	return s

def Terminal_Test(s):
    #test si le jeu est fini ou non
	flag = True
	for i in range(s.shape[0]):
		for j in range(s.shape[1]):	
			if s[i][j] == None:
				flag = False
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
	elif (np.count_nonzero(s == "X"))<=(np.count_nonzero(s == "O")):
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

mp = Morpion()

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


    
#morpion()






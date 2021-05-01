# -*- coding: utf-8 -*-
"""
Created on Sat May  1 10:36:47 2021

@author: victo
"""
#%% Code Romane
import numpy as np

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


# On renvoie une liste contenant toutes les positions qui ne sont pas occupés
# p est le plateau
def Action(p):
	l = []
	for i in range(p.shape[0]):
		for j in range(p.shape[1]):	
			if p[i][j] == None:
				l.append([i,j])
	return l

# On actualise le plateau du jeu
def Result(p,a,symbolJoueur):
	p[a[0]][a[1]]=symbolJoueur
	return p


# i,j sont les coord du pion qui vient juste d'être posé
def Terminal_Test(p,x,y):
    # on vérifie que le plateau n'est pas entièrement rempli
    plateauRempli=False
    caseVide=[x[i] for x in p for i in range(12) if x[i]==None]
    if len(caseVide)==0:
        plateauRempli=True  
    
    # on vérifie sur les lignes qu'il n'y ait pas de gagnant
    presenceGagnant=False
    for i in range(p.shape[0]):
        for j in range(p.shape[1]-3):
            if(p[i][j]==p[i][j+1]==p[i][j+2]==p[i][j+3]!=None):
                presenceGagnant=True
                
    # on vérifie sur les colonnes qu'il n'y ait pas de gagnant   
    for j in range(p.shape[1]):
        for i in range(p.shape[0]-3):
            if(p[i][j]==p[i+1][j]==p[i+2][j]==p[i+3][j]!=None):
                presenceGagnant=True
                
    # on vérifie sur les diagonales qu'il n'y ait pas de gagnant
    for k in range (4):
        if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y-3+k>-1 and y-2+k>-1 and y-1+k>-1 and y+k>-1 and y-3+k<12 and y-2+k<12 and y-1+k<12 and y+k<12):
            if (p[x-3+k][y-3+k]==p[x-2+k][y-2+k]==p[x-1+k][y-1+k]==p[x+k][y+k]!=None):
                presenceGagnant=True
    
  
    for k in range (4):
        if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y+3-k>-1 and y+2-k>-1 and y+1-k>-1 and y-k>-1 and y+3-k<12 and y+2-k<12 and y+1-k<12 and y-k<12):
            if (p[x-3+k][y+3-k]==p[x-2+k][y+2-k]==p[x-1+k][y+1-k]==p[x+k][y-k]!=None):
                presenceGagnant=True
    
    
    return None if plateauRempli==True and presenceGagnant==False else presenceGagnant # on affiche match None si il y a un match nul

 
    

# %% TESTS

# Tests sur la classe Plateau       
plateau=Plateau()
print(plateau)
plateauTest=np.array([['x','x','o','x',None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,'o',None,'o',None,None,None,None],
                      [None,None,None,None,None,'x','x',None,None,None,None,None],
                      [None,None,None,'o',None,'x',None,None,None,None,None,None],
                      [None,None,None,None,'x','x',None,None,'x','x',None,None],
                      [None,None,None,None,None,'o',None,None,'o',None,None,None],
                      [None,None,None,None,None,None,'o','o','o','x',None,None],
                      [None,None,None,'x',None,None,'o',None,'x',None,None,None],
                      ['x',None,'x',None,None,'x','o',None,'o',None,None,None],
                      [None,'x',None,None,'o',None,'x',None,'x',None,None,None],
                      ['x',None,'o',None,None,None,None,'x',None,None,None,None],
                      [None,None,None,'x',None,None,None,None,'o',None,None,None]])

# plateauTest=np.array([['x','o','x','x','o','x','o','x','o','x','o','x'],
#                       ['o','o','x','x','x','o','o','o','x','o','x','o'],
#                       ['x','x','o','o','o','x','o','o','o','x','x','o'],
#                       ['x','o','x','o','o','o','x','x','x','o','x','x'],
#                       ['x','x','o','x','o','x','o','o','x','o','o','o'],
#                       ['o','o','o','x','x','x','o','x','o','x','x','x'],
#                       ['o','x','x','o','o','x','x','o','x','o','o','x'],
#                       ['x','x','o','x','x','o','o','x','o','x','x','o'],
#                       ['o','o','x','x','x','o','o','o','x','x','o','o'],
#                       ['x','o','x','x','o','x','x','o','o','o','x','x'],
#                       ['o','x','o','o','x','o','x','o','o','x','o','o'],
#                       ['x','o','x','o','o','x','x','x','o','o','x','x']])


pTest=Plateau(plateauTest)

# Tests sur la fonctions Actions
print(Action(pTest.tab))

# Tests sur la fonctions Result
print("pTest avant\n",pTest,sep="")
Result(pTest.tab,[0,5],"x")
print("pTest après\n",pTest,sep="")

# Tests sur la fonction Terminal Test
print(Terminal_Test(pTest.tab,8,2))
print(Terminal_Test(pTest.tab,9,1))
print(Terminal_Test(pTest.tab,10,0))
print(Terminal_Test(pTest.tab,1,7))



#%% Code Victor


def Utility(p):#n'est utlisé que sur un plateau dont la partie est fini
    score=0
    presenceGagnant=False
    for i in range(p.shape[0]):
        indj=0
        presenceGagnantTemp=False
        for j in range(p.shape[1]-3):
            if(p[i][j]==p[i][j+1]==p[i][j+2]==p[i][j+3]!=None):
                presenceGagnantTemp=True
                indj=j
        if presenceGagnantTemp:
            if p[i][indj]=='x':
                score=1
            else:
                score=-1
        presenceGagnant=presenceGagnantTemp
    if not presenceGagnant:           
            
# on vérifie sur les colonnes s'il y a un gagnant, si x (l'IA) gagne, le score vaut 1 sinon -1 et 0 si match null
        for j in range(p.shape[1]):
            indi=0
            presenceGagnantTemp=False
            for i in range(p.shape[0]-3):
                if(p[i][j]==p[i+1][j]==p[i+2][j]==p[i+3][j]!=None):
                    presenceGagnantTemp=True
                    indi=i
            if presenceGagnantTemp:
                if p[indi][j]=='x':
                    score=1
                else:
                    score=-1
            presenceGagnant=presenceGagnantTemp        
   
                
    # on vérifie sur les diagonales à pente négative s'il y a un gagnant, si x (l'IA) gagne, le score vaut 1 sinon -1 si match null
    if not presenceGagnant:
        for x in range(3,p.shape[0]):
            indy=0
            presenceGagnantTemp=False
            for y in range(3,p.shape[1]):
                for k in range (4):
                    if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y-3+k>-1 and y-2+k>-1 and y-1+k>-1 and y+k>-1 and y-3+k<12 and y-2+k<12 and y-1+k<12 and y+k<12):
                        if (p[x-3+k][y-3+k]==p[x-2+k][y-2+k]==p[x-1+k][y-1+k]==p[x+k][y+k]!=None):
                            presenceGagnantTemp=True
                            indy=y
                if presenceGagnantTemp:
                    if p[x][indy]=='x':
                        score=1
                    else:
                        score=-1
            presenceGagnant=presenceGagnantTemp      
    # on vérifie sur les diagonales à pente positive s'il y a un gagnant, si x (l'IA) gagne, le score vaut 1 sinon -1 si match null        
    if not presenceGagnant:
        for x in range(3,p.shape[0]):
            indy=0
            presenceGagnantTemp=False
            for y in range(p.shape[1]-3):
                for k in range (4):
                    if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y+3-k>-1 and y+2-k>-1 and y+1-k>-1 and y-k>-1 and y+3-k<12 and y+2-k<12 and y+1-k<12 and y-k<12):
                        if (p[x-3+k][y+3-k]==p[x-2+k][y+2-k]==p[x-1+k][y+1-k]==p[x+k][y-k]!=None):                            
                            presenceGagnantTemp=True
                            indy=y
                if presenceGagnantTemp:
                    if p[x][indy]=='x':
                        score=1
                    else:
                        score=-1
    return score
        
print(Utility(pTest.tab))        
    
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 08:29:48 2021

@author: kasumi
"""

from tkinter.ttk import *
from tkinter import *
from random import randint
from tkinter.messagebox import *
from ZoneAffichage import *
from MonBoutonLettre import *
from MonBoutonTheme import *
import sqlite3




class FenPrincipale(Tk):
    
    def __init__(self,joueur):
        Tk.__init__(self)
        
        #database connection
        self.bd="pendu.db"
        try :
            self.conn=sqlite3.connect(self.bd)
            self.curseur=self.conn.cursor()
        except Exception as err:
            print("erreur de connexion à la base de donnee",err)
        
        self.joueur=joueur
        self.joueurId=self.getJoueurId()
        self.joueurScore=self.getJoueurScore()
        print(self.joueurScore)
        self.colorTheme="#2687bc"
        self.configure(bg=self.colorTheme)
        
        # paramètres de la fenêtre
        self.title('Jeu du Pendu')
        self.geometry('650x600+200+50')
        self.resizable(0,0)

    
        # constitution de son arbre de scène
        
        # frame 1: menu du haut
        Frame1 = Frame(self)
        
        #boutons du menu
        self.__boutonLancer = Button(Frame1, text='Nouvelle partie')
        self.__boutonTheme = Button(Frame1, text='Theme')
        self.__boutonQuitter = Button(Frame1, text='Quitter')
        
        joueurFrame=Frame(self,bg="#2687bc")
        
        #affichage du nom du joueur et du score enregistré
        self.joueurLabel=Label(joueurFrame,text=self.joueur,bg="#2687bc",fg="white")
        self.joueurScoreLabel=Label(joueurFrame,text="Score: ",bg="#2687bc",fg="white")
        #bouton pour afficher l'historique
        self.boutonHistorique=Button(joueurFrame,text="Voir historique",command=self.historique,bg="white")
        
        #undo button
        self.__undo = Button(self, text='Undo')
        
        #création du canva 
        self.__canvas = ZoneAffichage(self,420,320)
        
        #mot caché (declaration)
        self.__lmot=Label(self,text='Mot: ')
        #initialisation nombre d'essais manqués
        self.__nbManque=0
        #le clavier
        self.__clavier=Frame(self)

        #creation des boutons du clavier
        self.__boutons=[]
        for i in range(26):
            self.__boutons.append(MonBoutonLettre(self.__clavier,self.afficherLettre,chr(ord('A')+i)))
            self.__boutons[i].config(command=self.__boutons[i].cliquer)
        
        
        
        #placement et disposition
        joueurFrame.pack(side=LEFT,padx=(20,10))
        Frame1.pack(side=TOP, padx=50, pady=0)
        self.joueurLabel.pack()
        self.joueurScoreLabel.pack()
        self.boutonHistorique.pack(pady=10)
        self.__boutonLancer.pack(side=LEFT, padx=15, pady=10)
        self.__boutonTheme.pack(side=LEFT, padx=15, pady=10)
        self.__boutonQuitter.pack(side=LEFT, padx=15, pady=10)
        self.__undo.pack(side=RIGHT, padx=15, pady=10)
        
        self.__canvas.pack(pady=10)
        self.__lmot.pack()
        
        #disposition clavier
        self.__clavier.pack(side=BOTTOM,padx=5,pady=5,expand="yes")
        
        for i in range(3):
            for j in range(7):
                self.__boutons[i*7+j].grid(row=i,column=j,ipadx=20)
        for j in range(5):
            self.__boutons[21+j].grid(row=3,column=j+1,ipadx=20)
          
            
        #commandes
        self.__boutonQuitter.config(command=self.destroy)
        self.__boutonLancer.config(command=self.lancer)
        self.__boutonTheme.config(command=self.choixTheme)
        self.__undo.config(command=self.undo)
       

        
 
    
#methodes

    def choixTheme(self):
        #create popup window with different options
        self.popup=Toplevel(self)
        self.popup.geometry('300x100+300+300')
        self.popup.title("Theme")
        self.b=Button(self.popup,text='Changer',command=self.popup.destroy)
        
        
        #theme options
        
        choix1 = MonBoutonTheme(self.popup,self.colorSet,"Brown")
        choix2 = MonBoutonTheme(self.popup,self.colorSet,"green")
        choix3 = MonBoutonTheme(self.popup, self.colorSet,"#ec4062")
        choix4 = MonBoutonTheme(self.popup,self.colorSet ,"#2687bc")
        
        #disposition
        choix1.pack(side=LEFT, padx=10)
        choix2.pack(side=LEFT, padx=10)

        choix3.pack(side=LEFT, padx=10)
        choix4.pack(side=LEFT, padx=10)
        
        
        self.b.pack(side=BOTTOM,padx=5, pady=10)
        
        #commandes
        
        choix1.config(command=choix1.cliquer)
        choix2.config(command=choix2.cliquer)
        choix3.config(command=choix3.cliquer)
        choix4.config(command=choix4.cliquer)
    
    #theme change
    def colorSet(self,color):
        self.colorTheme=color
        self.configure(bg=self.colorTheme)
    

    #chargement de la base de mots cachés
    def chargeMots(self):
    	f = open('mots.txt', 'r')
    	s = f.read()
    	self.__mots = s.split('\n')
    	f.close()

    #lancement du jeu, creation du mot caché et activation du clavier
    def lancer(self):
        
        #activation du clavier et effacage de la pendule
        self.forme=self.__canvas.getForme()
        for i in range(len(self.forme)):
            self.forme[i].setState("hidden")
        self.__nbManque=0
        for i in range(26):
            self.__boutons[i].config(state=NORMAL)
        
        #affichage du score
        self.joueurScoreLabel.config(text='Score: '+str(self.joueurScore))
            
        #nouveau mot
        self.chargeMots()
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]
        self.__motAffiche=len(self.__mot)*'*'
        self.__lmot.config(text='Mot: '+self.__motAffiche)
        
        
    #cette methode permet de recuperer l'IdJoueur du joueur ayant ce nom dans la table joueur
    def getJoueurId(self):
        try:
            self.requete="SELECT IdJoueur FROM joueur WHERE Pseudo='{}'".format(self.joueur)
            self.curseur.execute(self.requete)
            joueurId=self.curseur.fetchone()
            return joueurId[0]
        except:
            return -1
    
    def getJoueurScore(self):
        try:
            self.requete="SELECT SUM(score) FROM Partie WHERE IdJoueur='{}'".format(self.joueurId)
            self.curseur.execute(self.requete)
            score=self.curseur.fetchone()
            print(score[0])
            if score[0]!=None:
                score=score[0]
            else:
                score=0
                
            print(score)
            return score
        except:
            print("erreur")
            return -1
    
    #cette methode se charge d'enregistrer le score du joueur apres le jeu
    def saveGame(self,score):
        try:
            self.curseur.execute("INSERT INTO Partie(IdJoueur,Mot,score) VALUES ('{}','{}','{}')".format(self.joueurId,self.__mot,score))
            self.conn.commit()
        except:
            print("echec")
            return -1
    
    #affichage d'une lettre trouvée        
    def afficherLettre(self,lettre):
        cpt=0
        lettres=list(self.__motAffiche)
        for i in range(len(self.__mot)):
            if self.__mot[i]==lettre:
                cpt+=1
                lettres[i]=lettre
        self.__motAffiche=''.join(lettres)
        
        #si la lettre n'est pas dans le mot caché
        if cpt==0:
            #affichage de la pendule
            self.forme[self.__nbManque].setState("normal")
            self.__nbManque+=1
            if self.__nbManque>=10:
                self.finPartie(False)
        else:
            self.__lmot.config(text='Mot: '+self.__motAffiche)
            if self.__mot==self.__motAffiche:
                self.finPartie(True)
    
    
    def finPartie(self,gagne):
        for b in self.__boutons:
            b.config(state=DISABLED)
            
        if gagne==True:
            self.__lmot.config(text=self.__mot+'-Bravo!! Vous avez gagne')
            score=1
        else:
            self.__lmot.config(text=self.__mot+'-Vous avez perdu, le mot etait:'+self.__mot)
            score=0
        
        #sauvegarde du score dans la base de donnée
        self.saveGame(score)
        
        #update affichage du score
        self.joueurScore=self.getJoueurScore() 
        self.joueurScoreLabel.config(text='Score: '+str(self.joueurScore))


    def undo(self):
        if self.__nbManque>=1:
            self.__nbManque=self.__nbManque-1
            #masquage de la pendule
            self.forme[self.__nbManque].setState("hidden")
        
    
    def historique(self):
        #create popup window with game history
        self.historique=Toplevel(self)
        self.historique.title("Historique des parties")
        
        try:
            self.requete="SELECT * FROM Partie WHERE IdJoueur='{}'".format(self.joueurId)
            self.curseur.execute(self.requete)
            histoArray=self.curseur.fetchall()
        except:
            print("oups")
            return 0
            
        #creation du tableau de l'historique
        tableau = Treeview(self.historique, columns=('Mot', 'Resultat'))
        tableau.column("Resultat", width=20)
        tableau.column("Resultat", width=70)

        tableau.heading('Mot', text='Mot')
        
        tableau.heading('Resultat', text='Resultat')
        
        tableau['show'] = 'headings' # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert
        
        tableau.pack(padx = 10, pady = (0, 10))
        print(histoArray)
        
        for enreg in histoArray:
            tableau.insert('', 'end', iid=enreg[0], values=(enreg[2], enreg[3]))
        
        
        self.quit=Button(self.historique,text='Fermer',command=self.historique.destroy).pack(side=BOTTOM,pady=10)
 

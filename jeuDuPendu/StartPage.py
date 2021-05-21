# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 19:26:46 2021

@author: kasumi
"""
import sqlite3
from tkinter import *
from FenPrincipale import *


class StartPage(Tk):
    
    playerlimit=3

    def __init__(self):
        Tk.__init__(self)
        
        self.colorTheme="#2687bc"
        self.configure(bg=self.colorTheme)
        
        self.title('Jeu du Pendu')
        self.geometry('650x600+200+50')
        self.resizable(0,0)
        
        
        #database connection
        self.bd="pendu.db"
        try :
            self.conn=sqlite3.connect(self.bd)
            self.curseur=self.conn.cursor()
        except Exception as err:
            print("erreur de connexion à la base de donnee",err)
            
        
        #main frame
        self.frame=Frame(self,bg="#2687bc")
        self.frame.pack()
        
        #game title
        label = Label(self.frame, bg="#2687bc",text="LE JEU DU PENDU\n",fg='White',font=("Courier", 30))
        label.pack(side=TOP,padx=50, pady=(70,0))
        
        
        #player frame
        self.frame2=Frame(self.frame,bg="#2687bc")
        self.frame2.pack(side=TOP,pady=(0,20))
        
        #show existing players
        self.players=self.getPlayers()
        self.playersButton=[]
        #player buttons create
        self.value=StringVar()
        for i in range(len(self.players)):
            self.playersButton.append(Radiobutton(self.frame2,text=self.players[i],variable=self.value, value=i,relief=RAISED,font=("Courier", 13), bg="white"))
            self.playersButton[i].pack(side=LEFT,ipady=1,ipadx=10,padx=20,pady=5)
        
        #player delete button
        delete=Button(self.frame,text="supprimer un joueur",font=("Courier", 10), bg="#ee9999",command=self.deletePlayer).pack()
        
        self.pseudoFrame=Frame(self.frame,bg="#2687bc")
        self.pseudoFrame.pack(pady=30)
        
        
        #pseudo input
        textvalue = StringVar() 
        textvalue.set("joueur")
        self.entree = Entry(self.pseudoFrame, textvariable=textvalue, width=50)
        self.entree.pack(side=TOP,pady=20,ipady=5)
        
        
        #create player button
        ajouter = Button(self.pseudoFrame, text="Ajouter un joueur",font=("Courier", 10), bg="#aaEfff",command=self.ajouterJoueur)
        ajouter.pack(side=TOP,ipady=2,ipadx=10)

        #player limit message
        self.message = Label(self.pseudoFrame,text="",font=("bold", 8),bg="#2687bc",fg="white")


        #play button
        button1 = Button(self.frame, text="Jouer",font=("Courier", 16), bg="white",command=self.startnext)
        button1.pack(side=BOTTOM,ipady=10,ipadx=50,pady=(20,50))
        
                
    
    #cette methode actualise l'affichage de la liste des joueurs disponibles
    def playerButtonListUpdate(self):
        #old players button list hide
        for j in range(len(self.playersButton)):
            self.playersButton[j].pack_forget()
        #new player button list show
        self.playersButton.clear()
        for i in range(len(self.players)):
            self.playersButton.append(Radiobutton(self.frame2,text=self.players[i],variable=self.value, value=i,relief=RAISED,font=("Courier", 13), bg="white"))
            self.playersButton[i].pack(side=LEFT,ipady=1,ipadx=10,padx=20,pady=5)
        
        
        
    def startnext(self):
        try:
            playerIndex=int(self.value.get())
            player=self.players[playerIndex]
            app = FenPrincipale(player)
            StartPage.destroy(self)
        except:
            self.message.config(text="Il faut selectionner un joueur d'abord")
            self.message.pack(pady=10)
        
            

    
    #cette fonction a été créée pour recuperer les premiers elements de l'objet afin de pouvoir utiliser la fonction map apres.
    def assign(self,x):
        x=x[0]
        return x
    
    #cette methode recupere les joueurs de la base de donnée
    def getPlayers(self):
        self.requete="SELECT Pseudo FROM joueur"
        self.curseur.execute(self.requete)
        players=self.curseur.fetchall()  
        players=list(map(self.assign,players))      
        return players
    
        
        
    #cette methode va executer la methode new player et traiter son resultat
    def ajouterJoueur(self):
        result=self.newPlayer()
        if result==2:
            self.message.config(text="Cet utilisateur existe deja veuillez le selectionner")
            self.message.pack(pady=10)
        if result==3:
            self.message.config(text="Vous ne pouvez pas creer plus de 3 joueurs,\n il faut en supprimer un")
            self.message.pack(pady=5)
        if result==0:
            self.message.config(text="ohh!! l'ajout du joueur a echoué, reessaie pour voir!")
            self.message.pack(pady=10)
        if result==1:
            #on affiche le nouveau joueur créé dans la liste des joueurs disponibles. 
            #la variable self.joueur a été créée dans la fonction newplayer et elle contient l'entrée de l'utilisateur
            self.message.config(text="Super! l'ajout a reussi")
            self.message.pack(pady=10)
            #player list update
            self.players.append(self.joueur)
            #player button list update
            self.playerButtonListUpdate()
            
            
    #cette methode va recuperer l'entree saisie et verifier l'existence de l'utilisateur puis l'ajouter dans la base de donnée si il n'existe pas deja
    def newPlayer(self):
        self.joueur=self.entree.get()
        
        try:           
            #verification de l'existence du joueur
            self.requete="SELECT IdJoueur FROM joueur WHERE Pseudo='{}'".format(self.joueur)
            self.curseur.execute(self.requete)
            self.pseudo=self.curseur.fetchall()
            #si le client est deja la
            if self.pseudo!=[]:
                return 2
        
            #si c'est un nouveau joueur
            if len(self.players)<self.playerlimit:
                self.curseur.execute("INSERT INTO joueur(Pseudo) VALUES ('{}')".format(self.joueur))
                self.conn.commit()
            else:
                return 3
        
        except:
            return 0

        #si la requete reussi et qu'un nouveau client est ajouté
        return 1
    
    
    
    def deletePlayer(self):
        try:
            toDeleteIndex=int(self.value.get())
        except:
            self.message.config(text="Il faut selectionner le joueur à supprimer d'abord")
            self.message.pack(pady=10)
            
        toDelete=self.players[toDeleteIndex]
        #requete de suppression
        self.requete="DELETE FROM joueur WHERE Pseudo='{}'".format(toDelete)
        self.curseur.execute(self.requete)
        self.conn.commit()
        
        #players list update
        self.players.pop(toDeleteIndex)
        
        #players button list update (on refait l'affichage car les indexes on maintenant changé, donc la valeur des boutons doit aussi changer sinon nous aurons une out of range error)
        self.playerButtonListUpdate()
        
        #message update
        self.message.config(text="Le joueur '{}' a ete supprime".format(toDelete))
        self.message.pack(pady=10)
  
        
if __name__ == "__main__":
    app = StartPage()
    app.mainloop()
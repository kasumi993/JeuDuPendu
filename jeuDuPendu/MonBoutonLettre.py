# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:38:54 2021

@author: kasumi
"""

from tkinter import *


class MonBoutonLettre(Button):
    def __init__(self,parent,methode,t):
        Button.__init__(self,master=parent,text=t,state=DISABLED)
        self.methode=methode
        self.__lettre=t
        
    def cliquer(self):
        self.config(state=DISABLED)
        self.methode(self.__lettre)
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:11:38 2021

@author: kasumi
"""

from tkinter import *


class MonBoutonTheme(Button):
    def __init__(self,parent,methode,color):
        Button.__init__(self,master=parent,bg=color,height = 1, width = 3)
        self.methode=methode
        self.__color=color
        
    def cliquer(self):
        self.methode(self.__color)
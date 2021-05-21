# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 08:45:23 2021

@author: kasumi
"""

from tkinter import *
from random import randint
from formes import *

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur, background='#ec4062')

        self.rectangle=[]
        #pieds
        self.rectangle.append(Rectangle(self, 100, 300, 100, 5, 'yellow'))
        self.rectangle.append(Rectangle(self, 120, 250, 5, 50, 'black'))
        self.rectangle.append(Rectangle(self, 120, 200, 5, 50, 'black'))
        self.rectangle.append(Rectangle(self, 120, 150, 5, 50, 'black'))
        self.rectangle.append(Rectangle(self, 120, 100, 5, 50, 'black'))
        #barre horizontale
        self.rectangle.append(Rectangle(self, 120, 100, 60, 5, 'black'))
        self.rectangle.append(Rectangle(self, 170, 100, 60, 5, 'black'))
        #barre pendu
        self.rectangle.append(Rectangle(self, 230, 100, 5, 50, 'black'))
        #accroche et boule de pendu
        self.rectangle.append(Rectangle(self, 222, 150, 20, 5, 'black'))
        self.rectangle.append(Ellipse(self, 230, 170, 25, 25, 'yellow'))
        
        #initial state
        for i in range(len(self.rectangle)):
            self.rectangle[i].setState("hidden")
            
    #getter        
    def getForme(self):
        return self.rectangle
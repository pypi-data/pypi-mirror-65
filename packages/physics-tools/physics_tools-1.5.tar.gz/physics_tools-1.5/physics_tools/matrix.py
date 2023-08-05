import numpy as np
import sympy as sp
import scipy as cp

# Set sympy matrix display
sp.init_printing(use_latex='mathjax') 
from IPython.display import display

# Define 3d Vector function
def identiteit():
    return np.matrix([[1,0,0],[0,1,0],[0,0,1]])

def schalen(x,y):
    return np.matrix([[x,o,0],[0,y,0],[0,0,1]])

def roteren(theta):
    theta = theta/180*np.pi
    return np.matrix([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])

def verplaatsen(x,y):
    return np.matrix([[1, 0, x], [0, 1, y], [0, 0, 1]])

def horizontaal_uitrekken(x):
    return np.matrix([[1,x,0],[0,1,0],[0,0,1]])

def verticaal_uitrekken(y):
    return np.matrix([[1,0,0],[y,1,0],[0,0,1]])

def spiegelx():
    return np.matrix([[-1,0,0],[0,1,0],[0,0,1]])

def spiegely():
    return np.matrix([[1,0,0],[0,-1,0],[0,0,1]])

def projecterenx():
    return np.matrix([[1,0,0],[0,0,0],[0,0,1]])

def projectereny():
    return np.matrix([[0,0,0],[0,1,0],[0,0,1]])

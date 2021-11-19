# biblioteca padrão
import math
import sys
import time
import argparse
import itertools
import random

# biblioteca de terceiros
import numpy
import pygame
import PPlay
from PPlay.sprite import *
from PPlay.window import *

# utilidades
from utils import *

class Pad:

    def __init__( self , **kwargs ) -> None:
        
        self.pos = kwargs.get('pos', numpy.array( [ 2 , 3 ] ) )
        self.basepos = self.pos.copy() #depois de ponto marcado, retornar à posição original
        self.height = kwargs.get( 'height' , 1.5 )
        self.speed = numpy.zeros( 2 )
        
        #------------------------------------------------------------
        # O pad pode ser rotacionado, e norm é o vetor unitŕaio perpendicular
        # à barra, indicando a inclinação
        self.norm = kwargs.get( 'norm' , numpy.array( [1. , 0 ] ) )
        self.basenorm = self.norm.copy()
        self.rot_speed = kwargs.get( 'rot_speed' , 1. )
        self.max_theta = kwargs.get( 'max_theta' , numpy.pi/3 )

        self.mass = kwargs.get( 'mass' , 1. )

        #------------------------------------------------------------
        # Se for nescessário retornar à posição original. Por exemplo
        # em caso de colisão
        self.previous_pos  = None
        self.previous_norm = None

        #-------------------------------------------------------------
        # Area em que o pad fica restrito
        #                                         x1  y1  dx  dy
        self.outerbox = kwargs.get("outerbox" , [ 0 , 0 , 4 , 6] )

    def get_edges( self ):

        v = self.norm*self.height/2
        rot_mat = numpy.array([ [ 0 , -1. ] , [ 1 , 0 ] ])
        
        x1 = self.center + v@rot_mat
        x2 = self.center + v@(-rot_mat )

        return x1 , x2
        
    def reset_vars( self , point = False ):

        p0 = self.basepos if point else self.previous_pos
        self.pos = p0.copy()

        n0 = self.basenorm if point else self.previous_norm
        self.norm = n0

    def move( self , dt ):

        self.previous_pos = self.pos.copy()
        self.pos += self.speed*dt
    
    def rotate( self , dt , clockwise = True):

        self.previous_norm = self.norm.copy()

        k = -1 if clockwise else 1
        d_theta = k*self.rot_speed*dt
        dx = numpy.cos( d_theta )
        dy = numpy.sin( d_theta )
        self.norm += numpy.array( [ dx , dy ] ) 

        
        
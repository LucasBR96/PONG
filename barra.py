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
from constantes import *

class barra:

    @classmethod
    def right( cls ):
        return cls()
    
    @classmethod
    def left( cls ):
        return cls(
            pos      = LEFT_PAD,
            outerbox = LEFT_BOX
        )

    def __init__( self , **kwargs ) -> None:
        
        self.pos = kwargs.get('pos', numpy.array( RIGHT_PAD ) )
        self.basepos = self.pos.copy() #depois de ponto marcado, retornar à posição original
        self.height = kwargs.get( 'height' , PAD_TAM )
        self.speed = numpy.zeros( 2 )
        
        self.mass = kwargs.get( 'mass' , PAD_MASS )

        #------------------------------------------------------------
        # Se for nescessário retornar à posição original. Por exemplo
        # em caso de colisão
        x , y  = self.pos
        self.previous_pos  = ( x , y )

        #-------------------------------------------------------------
        # Area em que o pad fica restrito
        self.outerbox = kwargs.get("outerbox" , RIGHT_BOX )

        self.score = 0

    def get_edges( self ):

        L = self.height/2
        x1 = self.pos + numpy.array( [ 0 , L ] )
        x2 = self.pos - numpy.array( [ 0 , L ] )

        return x1 , x2
        
    def reset_vars( self , point = False ):

        p0 = self.basepos if point else self.previous_pos
        self.pos = numpy.array( p0 )

    def move( self , dt ):

        if ( self.speed**2 ).sum() == 0.: return 

        x , y = self.pos
        self.previous_pos = ( x , y )
        self.pos += self.speed*dt
    
    def out_of_thebox( self ):

        pos1 , pos2 = self.get_edges()
        y1 = pos1[ 1 ]
        y2 = pos2[ 1 ]
        x  = self.pos[ 0 ]

        xmin , ymin , dx , dy = self.outerbox
        xmax , ymax = xmin + dx , ymin + dy

        a = ( x > xmax ) or ( x < xmin )
        b = ( y1 > ymax )
        c = ( y2 < ymin )

        return any( [ a , b , c ] )

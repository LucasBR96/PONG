
# biblioteca de terceiros
import numpy
import pygame
import PPlay
from PPlay.sprite import *
from PPlay.window import *

# utilidades
from utils import coord_conv, set_bolinha_vel
from constantes import *

class bolinha:

    def __init__( self , **kwargs ):

        self.mass  = kwargs.get( "mass" , BOLA_MASS )
        self.pos   = kwargs.get( "pos" , BOLA_START )
        self.speed = kwargs.get( "speed" , set_bolinha_vel() )

        self.base_pos     = ( BOLA_START[ 0 ] , BOLA_START[ 1 ] )
        self.previous_pos = self.pos.copy()
    
    def move( self , dt , g = G ):

        x , y = self.pos
        self.previous_pos = ( x , y )

        self.pos += self.speed*dt
        self.speed[ 1 ] -= g*dt

    def reset_pos( self , point = False ):

        old = self.base_pos if point else self.previous_pos
        self.pos = numpy.array( old )

        if point: self.speed = set_bolinha_vel()
    

        


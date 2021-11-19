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
from utils import coord_conv
from constantes import *


def coord_convert( cart , screen_dim, R = 25 ):

    '''
    converte as coordenadas do sistema cartesiano ( Centro da tela = ( 0 , 0 ) )
    para o sistema do PPlay
    '''

    # R é a razão entre numero de pixels e um metro
    
    dx = int( R*cart[ 0 ] )
    sx = screen_dim[ 0 ]//2 + dx

    dy = int( R*cart[ 1 ] )
    sy = screen_dim[ 1 ]//2 - dy
    
    return sx , sy

class bolinha:

    def __init__( self , **kwargs ):

        self.mass  = kwargs.get( "mass" , BOLA_MASS )
        self.pos   = kwargs.get( "pos" , BOLA_START )
        self.speed = kwargs.get( "speed" , BOLA_VEL )

        self.base_pos     = self.pos.copy()
        self.previous_pos = self.pos.copy()
    
    def move( self , dt , g = G ):

        self.previous_pos
        self.pos += self.speed*dt
        self.speed[ 1 ] -= g*dt

    def reset_pos( self , ponto = False ):

        old = self.base_pos if ponto else self.old_pos
        self.pos = old

class bolinha_spr( Sprite ):

    def __init__( self , **kwargs ):
        
        image_file = kwargs.get( 'image_file' , BOLA_IMG)
        super().__init__( "assets/images/" + image_file )

        self.bola = bolinha( **kwargs )
        self.conv = coord_conv( **kwargs )
    
    def convert_pos( self ):

        x , y = self.bola.pos
        true_x , true_y = self.conv.v2r( x , y )
        self.x = true_x
        self.y = true_y
        
if __name__ == "__main__":
    test_1()


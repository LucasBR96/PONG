import itertools
import sys
import time

import numpy

from constantes import * 

class coord_conv:

    def __init__(
        self , center = numpy.array( ( 0 , SCREEN_DIM[ 1 ] ) ),
        mat = numpy.array([ [ R , 0 ] , [ 0 , -R ] ])
    ):

        self.center = center
        self.mat = mat
    
    def from_virtual( self , x , y ):
        return numpy.array( [ x , y ] )@self.mat + self.center 
    
    def to_virtual( self , x , y ):

        '''
        não vou escrever nada ainda, pois não tenho nenhuma utilidade
        para essa função por enquanto
        '''
        pass


class clock:

    def __init__( self ):
        pass

def check_bw( bola_sprite , screen = SCREEN_DIM ):

    '''
    Checa se a bola colidiu com alguma parede, retornando
    uma flag pra ver qual foi atingida. Essa função opera no sistema de coor
    denada do PPlay.
    '''

    width , height = screen

    if bola_sprite.y + bola_sprite.height > height:
        return FLOOR
    
    if bola_sprite.y < 0:
        return CEIL
    
    if bola_sprite.x + bola_sprite.width > width:
        return FRONT_WALL
    
    if bola_sprite.x < 0:
        return BACK_WALL
    
    return NO_WALL

def handle_bw( bola , col_type , k = K ):

    '''
    Muda a direção da bola de acordo com a colisão obtida. 
    '''

    if col_type == NO_WALL:
        return
    
    dv = k*numpy.array( [ -1 , 1 ] )
    if col_type == FLOOR or col_type == CEIL:
        dv *= -1
    
    bola.speed *= dv 
    bola.reset_pos()
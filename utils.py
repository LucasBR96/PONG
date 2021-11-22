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
        self.inv = numpy.linalg.inv( mat )
    
    def from_virtual( self , x , y ):
        return numpy.array( [ x , y ] )@self.mat + self.center 
    
    def to_virtual( self , x , y ):
        return ( numpy.array( [ x , y ] ) - self.center )@self.inv
        
class clock:

    def __init__( self ):
        pass

def set_bolinha_vel( ):

    theta = BOLA_THETA*( numpy.random.random() -.5 )
    vec   = BOLA_VEL*numpy.array([
        numpy.cos( theta ), 
        numpy.sin( theta )
    ])

    if numpy.random.random() > .5:
        vec *= -1
    return vec

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

def handle_bw( bola_sprite , bola , col_type ):

    '''
    Muda a direção da bola de acordo com a colisão obtida com o teto ou chão
    '''

    if col_type == CEIL:
        bola_sprite.y = 0
    else:
        bola_sprite.y = SCREEN_DIM[ 1 ] - bola_sprite.height
    
    bola.speed[ 1 ] *= -1
    bola_sprite.set_virt_pos()
    


def update_score( pad_win , pad_lose , bola ):

    pad_win.score += 1 
    pad_lose.reset_vars( point = True)
    pad_lose.reset_vars( point = True)
    bola.reset_pos( point = True )


def check_bp( bola_sprite , pad_sprite ):

    if not bola_sprite.collided( pad_sprite ):
        return NO_PAD
    
    vbola = bola_sprite.bola.speed
    vpad  = pad_sprite.barra.norm
    if vbola.dot( vpad ) < 0:
        return FRONT_PAD
    return BACK_PAD

def handle_bp( bola_sprite, barra , k = K ):

    # bola_sprite.bola.speed *= -1
    
    # t = .001
    # while bola_sprite.collided( barra ):
    #     bola_sprite.bola.move( t )
    #     bola_sprite.convert_pos()
    
    # bola_sprite.bola.speed[1] *= -1

    new_x = barra.x - bola_sprite.width
    if bola_sprite.x > barra.x:
        new_x = barra.x + barra.width
    
    bola_sprite.x = new_x
    bola_sprite.set_virt_pos()
    bola_sprite.bola.speed[0] *= -1
import itertools
import sys
import time

import numpy

from constantes import * 

class coord_conv:

    def __init__(
        self , center = numpy.array( ( 0 , SCREEN_H ) ),
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

    def __init__( self , num_ticks = TICKS ):
        
        self.last_t    = time.time()
        self.max_ticks = num_ticks
        self.curr_tick = 0
        self.tps       = None
    
    def tick( self ):

        self.curr_tick += 1
        if self.curr_tick < self.max_ticks:
            return False
        
        self.curr_tick = 0

        aux = self.last_t
        self.last_t = time.time()
        dt = self.last_t - aux

        tps = dt/self.max_ticks #ticks per second
        self.tps = "{:2f}".format( tps )
        return True

def set_bolinha_vel( ):

    theta = BOLA_THETA*( numpy.random.random() -.5 )
    vec   = BOLA_VEL*numpy.array([
        numpy.cos( theta ), 
        numpy.sin( theta )
    ])

    if numpy.random.random() > .5:
        vec[ 0 ] *= -1
    return vec

def check_bw( bola_sprite ):

    '''
    Checa se a bola colidiu com alguma parede, retornando
    uma flag pra ver qual foi atingida. Essa função opera no sistema de coor
    denada do PPlay.
    '''


    if bola_sprite.y + bola_sprite.height > SCREEN_H:
        return FLOOR
    
    if bola_sprite.y < 0:
        return CEIL
    
    if bola_sprite.x + bola_sprite.width > SCREEN_W:
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
        bola_sprite.y = SCREEN_H - bola_sprite.height
    
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
    
    x_center = pad_sprite.x + pad_sprite.width/2
    a = ( bola_sprite.x < x_center < bola_sprite.x + bola_sprite.width )
    b = bola_sprite.y < pad_sprite.y
    c = bola_sprite.y + bola_sprite.height > pad_sprite.y + pad_sprite.height

    if a and ( b or c ):
        return OVR_PAD
    return SIDE_PAD


def handle_bp( bola_sprite, barra_sprite, col_type ):

    a = ( col_type == SIDE_PAD )
    b = ( bola_sprite.x < barra_sprite.x)
    c = ( bola_sprite.y < barra_sprite.y )

    if   a and b: bola_sprite.x = barra_sprite.x - bola_sprite.width #  pela esquerda
    elif a: bola_sprite.x = barra_sprite.x + barra_sprite.width      #  pela direita
    elif c: bola_sprite.y = barra_sprite.y - bola_sprite.height      #  por cima
    else  : bola_sprite.y = barra_sprite.y + barra_sprite.height     #  por baixo
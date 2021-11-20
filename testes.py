import pygame
from pygame.locals import *
pygame.init()

import PPlay
from PPlay.sprite import *
from PPlay.window import *
from PPlay.keyboard import *
from barra import barra_spr

from bolinha import *
from utils import *
from constantes import *

def teste1():

    W = Window( *SCREEN_DIM )
    W.set_title( "bolinha" )
    W.delta_time()

    b = bolinha_spr()
    b.convert_pos()
    
    while True:

        W.update()
        W.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()

        dt = W.delta_time()        
        b.bola.move( dt )
        b.convert_pos()
        
        hit = check_bw( b , ( W.width , W.height ) )
        handle_bw( b.bola , hit )


def teste2():

    W = Window( *SCREEN_DIM )
    W.set_title( "bolinha" )
    W.delta_time()

    b = bolinha_spr()
    b.convert_pos()

    pad = barra_spr()
    pad.convert_pos()

    kb = Keyboard()
    foo = lambda x: kb.key_pressed( x )

    def manage_keys():
        
        v = numpy.zeros( 2 )

        if   foo( 'w' ): v = numpy.array( [ 0 , PAD_SPEED ] )
        elif foo( 's' ): v = numpy.array( [ 0 , -PAD_SPEED ] )
        elif foo( 'a' ): v = numpy.array( [ -PAD_SPEED, 0  ] )
        elif foo( 'd' ): v = numpy.array( [ PAD_SPEED , 0 ] )

        pad.barra.speed = v

    def manage_pad_pos():

        barra = pad.barra
        if barra.out_of_thebox():
            barra.reset_vars()

    def manage_ball_hits():

        hit1 = check_bw( b , ( W.width , W.height ) )
        hit2 = check_bp( b , pad )
        if not( hit1 or hit2 ):
            return
        
        # x , y = b.bola.pos
        # vx , vy = b.bola.speed
        # wall = ( hit1 != 0 )
        # print( "{:2f} {:2f} {:2f} {:2f} {}".format( x , y , vx , vy, wall ) )

        if hit1: 
            handle_bw( b.bola , hit1 )
            return
        
        handle_bp( b.bola , pad.barra , hit2 )
    
    while True:

        W.update()
        W.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()
        pad.draw()

        dt = W.delta_time()        
        b.bola.move( dt )
        b.convert_pos()
        pad.barra.move( dt )
        pad.convert_pos()

        manage_ball_hits()
        manage_pad_pos()
        manage_keys()
        

if __name__ == "__main__":

    teste2()
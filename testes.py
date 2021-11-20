import pygame
import PPlay
from PPlay.sprite import *
from PPlay.window import *
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

    def manage_hits():

        hit1 = check_bw( b , ( W.width , W.height ) )
        hit2 = check_bp( b , pad )
        if not( hit1 or hit2 ):
            return
        
        x , y = b.bola.pos
        vx , vy = b.bola.speed
        wall = ( hit1 != 0 )
        print( "{:2f} {:2f} {:2f} {:2f} {}".format( x , y , vx , vy, wall ) )

        if hit1: 
            handle_bw( b.bola , hit1 )
            return
        
        handle_bp( b.bola , pad , hit2 )
    
    while True:

        W.update()
        W.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()
        pad.draw()

        dt = W.delta_time()        
        b.bola.move( dt )
        b.convert_pos()

        manage_hits()
        



if __name__ == "__main__":

    teste2()
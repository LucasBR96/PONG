import pygame
import PPlay
from PPlay.sprite import *
from PPlay.window import *

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


        



if __name__ == "__main__":

    teste1()
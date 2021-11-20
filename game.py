import pygame
from pygame.locals import *
pygame.init()

import PPlay
from PPlay.sprite import *
from PPlay.window import *
from PPlay.keyboard import *
from barra import barra_spr , barra

from bolinha import *
from utils import *
from constantes import *

def main():

    W = Window( *SCREEN_DIM )
    W.set_title( "bolinha" )
    W.delta_time()

    b = bolinha_spr()
    b.convert_pos()

    rpad = barra_spr( )
    rpad.barra = barra.right()
    rpad.convert_pos()
    print( *rpad.barra.pos , rpad.x , rpad.y )

    lpad = barra_spr( )
    lpad.barra = barra.left()
    lpad.convert_pos()
    print( *lpad.barra.pos , lpad.x , lpad.y )


    kb = Keyboard()
    foo = lambda x: kb.key_pressed( x )

    def set_screen():

        W.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()
        rpad.draw()
        lpad.draw()

    def manage_keys():
        
        v = numpy.zeros( 2 )

        a = any( map( foo , RPAD_KEYS ) )
        b = any( map( foo , LPAD_KEYS ) )
        c = foo( PAUSE )

        if not ( a or b or c ):
            return
        
        up , down , left , right = RPAD_KEYS
        pad = rpad
        if b:
            up , down , left , right = LPAD_KEYS
            pad = lpad

        if   foo( up    ): v = numpy.array( [ 0 , PAD_SPEED ] )
        elif foo( down  ): v = numpy.array( [ 0 , -PAD_SPEED ] )
        elif foo( left  ): v = numpy.array( [ -PAD_SPEED, 0  ] )
        elif foo( right ): v = numpy.array( [ PAD_SPEED , 0 ] )
        pad.barra.speed = v

    def manage_pad_pos():

        for pad in [ rpad , lpad ]:
            barra = pad.barra
            if barra.out_of_thebox():
                barra.reset_vars()

    def manage_ball_hits():

        hit1 = check_bw( b , ( W.width , W.height ) )
        hit2 = check_bp( b , rpad )
        hit3 = check_bp( b , lpad )

        if not( hit1 or hit2 or hit3 ):
            return

        if hit1: 
            handle_bw( b.bola , hit1 )
            return

        pad = rpad if hit2 else lpad
        handle_bp( b.bola , pad.barra , hit2 )
    
    while True:

        W.update()
        set_screen()

        dt = W.delta_time()
        # dt = .1        
        b.bola.move( dt )
        b.convert_pos()
        rpad.barra.move( dt )
        rpad.convert_pos()
        lpad.convert_pos()

        manage_ball_hits()
        manage_pad_pos()
        manage_keys()

if __name__ == "__main__":
    main()
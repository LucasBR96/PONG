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
    # print( *lpad.barra.pos , lpad.x , lpad.y )

    kb = Keyboard()
    foo = lambda x: kb.key_pressed( x )

    global paused
    paused = False

    def set_screen():

        W.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()
        rpad.draw()
        lpad.draw()

        #renderizando placar
        W.draw_text( str( rpad.barra.score ) , PLACAR1_X , PLACAR_Y , size = FONT_SIZE )
        W.draw_text( str( lpad.barra.score ) , PLACAR2_X , PLACAR_Y , size = FONT_SIZE )

        #indicando pausa 
        if paused:
            W.draw_text( "PAUSADO" , PAUSE_X , PAUSE_Y , size = FONT_SIZE  )

    def manage_keys():
        
        if foo( PAUSE ):
            global paused
            paused = not paused
            # se o frame estiver muito rapido, o jogo vai pausar e despausar enquanto o 
            # a barra pressionada.
            time.sleep( PAUSE_T )

        if paused:
            return

        a = any( map( foo , RPAD_KEYS ) )
        b = any( map( foo , LPAD_KEYS ) )
        
        v = numpy.zeros( 2 )
        if not ( a or b ):
            lpad.barra.speed = v.copy()
            rpad.barra.speed = v.copy()
            return
        
        up , down , left , right = RPAD_KEYS
        pad = rpad
        if b:
            up , down , left , right = LPAD_KEYS
            pad = lpad
        
        if   foo( up    ): v = numpy.array( [ 0 , PAD_SPEED ] )
        elif foo( down  ): v = numpy.array( [ 0 , -PAD_SPEED ] )
        # elif foo( left  ): v = numpy.array( [ -PAD_SPEED, 0  ] )
        # elif foo( right ): v = numpy.array( [ PAD_SPEED , 0 ] )
        pad.barra.speed = v
    
    def move_sprites():

        b.convert_pos()
        rpad.convert_pos()
        lpad.convert_pos()

        dt = W.delta_time()
        b.bola.move( dt )
        rpad.barra.move( dt )
        lpad.barra.move( dt )

    def manage_pad_pos():

        for pad in [ rpad , lpad ]:
            barra = pad.barra
            if barra.out_of_thebox():
                barra.out_of_thebox()
                print( barra.pos , pad.x , pad.y , pad.x + pad.width , pad.y + pad.height )
                barra.reset_vars()

    def manage_ball_wall():

        # print( *b.bola.pos , *b.bola.speed )
        hit = check_bw( b , ( W.width , W.height ) )
        if not hit:
            return
        
        if hit == CEIL or hit == FLOOR:
            handle_bw( b , b.bola , hit )
            return

        # acertou as paredes verticais, o que significa ponto
        pad_win  = rpad.barra
        pad_lose = lpad.barra
        if hit == BACK_WALL:
            pad_win , pad_lose = pad_lose , pad_win
        bola = b.bola

        update_score( pad_win , pad_lose , bola )
    
    def manage_ball_pad( ):

        hit1 = check_bp( b , rpad )
        hit2 = check_bp( b , lpad )

        if not( hit1 or hit2 ):
            return

        pad = rpad if hit1 else lpad
        handle_bp( b , pad )
    
    while True:

        W.update()
        set_screen()

        # dt = .1        
        manage_keys()
        if paused:
            continue

        manage_ball_wall()
        manage_ball_pad()
        manage_pad_pos()
        move_sprites()

if __name__ == "__main__":
    main()
import pygame
from pygame.locals import *
pygame.init()

import PPlay
from PPlay.sprite import *
from PPlay.window import *
from PPlay.keyboard import *

from barra import barra
from bolinha import bolinha
from utils import *
from constantes import *

def init_globals():

    global W
    W = Window( SCREEN_W , SCREEN_H )
    W.set_title( "gravity pong" )
    W.delta_time()

    global kb , foo
    kb = Keyboard()
    foo = lambda x: kb.key_pressed( x )

    global paused
    paused = False
    
    global conv
    conv = coord_conv()

    global bola , bola_sprite
    bola = bolinha()
    bola_sprite = Sprite( BOLA_IMG )

    global padr  , padr_sprite
    padr = barra.right()
    padr_sprite = Sprite( PAD_IMG )

    global padl  , padl_sprite
    padl = barra.left()
    padl_sprite = Sprite( PAD_IMG )

def align_ball( to_virtual = False ):
    
    global conv , bola_sprite , bola

    if to_virtual:
        true_x , true_y = bola_sprite.x, bola_sprite.y
        x , y = conv.to_virtual( true_x , true_y )
        bola.pos = numpy.array( [ x , y ] )
    
    else:
        virtual_x , virtual_y = bola.pos
        x , y = conv.from_virtual( virtual_x , virtual_y )
        bola_sprite.x , bola_sprite.y = x , y

def align_pad( left = False ):

    global padr , padr_sprite , padl , padl_sprite
    global conv

    pad , pad_sprite = padr , padr_sprite
    if left:
        pad , pad_sprite = padl , padl_sprite
    
    ( virtual_x , virtual_y ) , _ = pad.get_edges()
    x , y = conv.from_virtual( virtual_x , virtual_y )
    pad_sprite.x , pad_sprite.y = x , y

def set_screen():

    W.set_background_color( ( 255 , 255 , 255 ) )
    bola_sprite.draw()
    padr_sprite.draw()
    padl_sprite.draw()

    #renderizando placar
    W.draw_text( str( padr.score ) , PLACAR1_X , PLACAR_Y , size = FONT_SIZE )
    W.draw_text( str( padl.score ) , PLACAR2_X , PLACAR_Y , size = FONT_SIZE )

    #indicando pausa 
    if paused:
        W.draw_text( "PAUSADO" , PAUSE_X , PAUSE_Y , size = FONT_SIZE  )

def manage_keys():
    
    global paused
    if foo( PAUSE ):
        paused = not paused

        #----------------------------------------------------------------------
        # se o frame estiver muito rapido, o jogo vai pausar e despausar 
        # enquanto o jogador soltar a barra
        time.sleep( PAUSE_T )

    if paused:
        return

    a = any( map( foo , RPAD_KEYS ) )
    b = any( map( foo , LPAD_KEYS ) )
    
    v = numpy.zeros( 2 )
    if not ( a or b ):
        padr.barra.speed = v.copy()
        padr.barra.speed = v.copy()
        return
    
    up , down , left , right = RPAD_KEYS
    pad = padr
    if b:
        up , down , left , right = LPAD_KEYS
        pad = padl
    
    if   foo( up    ): v = numpy.array( [ 0 , PAD_SPEED ] )
    elif foo( down  ): v = numpy.array( [ 0 , -PAD_SPEED ] )
    elif foo( left  ): v = numpy.array( [ -PAD_SPEED, 0  ] )
    elif foo( right ): v = numpy.array( [ PAD_SPEED , 0 ] )
    pad.barra.speed = v

def move_sprites():

    dt = W.delta_time()
    bola.move( dt )
    padr.move( dt )
    padl.move( dt )

    #caso os pads saiam de seus limites
    for pad in [ padr , padl ]:
        if pad.out_of_thebox():
            pad.reset_vars()
    
    # fazendo os sprites seguirem seus respectivos objetos
    align_ball()
    align_pad()
    align_pad( True )


def manage_ball_wall():

    global bola_sprite , bola
    hit = check_bw( bola_sprite )
    if not hit:
        return
    
    if hit == CEIL or hit == FLOOR:
        handle_bw( bola_sprite )
        align_ball( True )
        bola.speed[ 1 ] *= -1
        return

    # acertou as paredes verticais, o que significa ponto
    pad_win  = padr
    pad_lose = padl
    if hit == BACK_WALL:
        pad_win , pad_lose = pad_lose , pad_win
    update_score( pad_win , pad_lose , bola )

def manage_ball_pad( ):

    hit1 = check_bp( bola_sprite , padr_sprite )
    hit2 = check_bp( bola_sprite , padl_sprite )

    if not( hit1 or hit2 ):
        return

    pad = padr_sprite if hit1 else padl_sprite
    handle_bp( bola_sprite , pad )
    align_ball( True )

    v = numpy.array( [ -1 , 1 ] )
    hit = max( hit1 , hit2 )
    if hit == OVR_PAD:
        v *= -1
    bola.speed *= v


def main():

    
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
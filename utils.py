import itertools
import sys
import time

import numpy
# --------------------------------------------------------
# Colisões

def space_partition( bolas ):
    
    '''
    particiona os objetos na tela em conjuntos disjuntos cujos
    elementos talvez colidam. Se dois objetos não estão no mesmo
    grupo é certo que eles não vão colidir no mesmo frame
    '''

    bolas.sort( key = lambda bola : bola.fx )
    
    ball_seqs = []
    current_seq = None
    for bola in bolas:

        if current_seq is None:
            current_seq = [ bola ]
            continue
        
        anterior = current_seq[ -1 ]
        if anterior.x + anterior.width < bola.x:
            current_seq.append( bola )
            continue

        ball_seqs.append( current_seq )
    return ball_seqs

def check_collisions( ball_seqs ):

    '''
    Procura colisões perfeitas dentro de cada grupo.
    '''

    col_cand = set()
    for seq in ball_seqs:
        for b1 , b2 in itertools.combinations( seq , 2 ):
            if b1.collided_perfect( b2 ):
                col_cand |= { ( b1 , b2 ) }
    return col_cand

def colisao_bw( bola , dims, k = .9 ):

    '''
    tratamento de colisão da bola com alguma das paredes
    do jogo.
    '''

    m = bola.mass
    vx = bola.vx
    vy = bola.vy
    ix , iy = 0 , 0 

    a = ( 0 < bola.x )
    c = ( bola.x + bola.width < dims[ 0 ] )
    if not( a and c ):
        ix = -2*vx*m

    b = ( 0 < bola.y )
    d = ( bola.y + bola.height < dims[ 1 ] )
    if not( b and d ):
        iy = -2*vy*m

    return k*ix , k*iy
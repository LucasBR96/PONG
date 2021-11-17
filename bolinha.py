# biblioteca padrão
import math
import sys
import time
import argparse
import itertools
import random

# biblioteca de terceiros
import numpy
import pygame
import PPlay
from PPlay.sprite import *
from PPlay.window import *

def space_partition( bolas ):
    
    bolas.sort( key = lambda bola : bola.fx )
    
    ball_seqs = []
    current_seq = None
    for bola in bolas:

        if current_seq is None:
            current_seq = [ bola ]
            continue
        
        anterior = current_seq[ -1 ]
        if anterior.collided( bola ):
            current_seq.append( bola )
            continue

        ball_seqs.append( current_seq )
    return ball_seqs

def check_collisions( ball_seqs ):

    col_cand = set()
    for seq in ball_seqs:
        for b1 , b2 in itertools.combinations( seq , 2 ):
            if b1.collided_perfect( b2 ):
                if b1 in col_cand or b2 in col_cand:
                    continue
                yield b1 , b2
                col_cand |= { b1 , b2 }
    return col_cand


def handle_collision( b1 , b2, k = 1 ):

    x1 = numpy.array( [ b1.fx , b1.fy ] )
    v1 = numpy.array( [ b1.vx , b1.vy ] )

    x2 = numpy.array( [ b2.fx , b2.fy ] )
    v2 = numpy.array( [ b2.vx , b2.vy ] )

    mass_ratio = 2*( b2.mass )/( b1.mass + b2.mass )

    dx = x1 - x2 
    dv = v1 - v2 

    v1 = v1 - dx*mass_ratio*( numpy.dot( dx , dv )/( dx**2 ).sum() )
    b1.vx = v1[0]*k
    b1.vy = v1[1]
    b1.reset_position()

def coord_convert( cart , screen_dim, R = 25 ):

    '''
    converte as coordenadas do sistema cartesiano ( Centro da tela = ( 0 , 0 ) )
    para o sistema do PPlay
    '''

    # R é a razão entre numero de pixels e um metro
    
    dx = int( R*cart[ 0 ] )
    sx = screen_dim[ 0 ]//2 + dx

    dy = int( R*cart[ 1 ] )
    sy = screen_dim[ 1 ]//2 - dy
    
    return sx , sy

class Bolinha( Sprite ):

    def __init__( self , image_file, center = ( 0 , 0 ) , **kwargs ):

        super().__init__( "assets/images/" + image_file )
        
        #--------------------------------------------------
        # posição, em metros da bolinha. A fisica vai considerar
        # a bolinha num plano cartesiano clássico. Sua posição vai ser
        # convertida para o sistema de coordenadas do PPlay quando a 
        # bola for renderizada
        x , y = center
        self.fx = x
        self.fy = y

        # para a colisão
        self.old = None

        # metros por segundo
        self.vx = kwargs.get( "vx" , 10 )
        self.vy = kwargs.get( "vy" , 0 )
         
        # quilogramas
        self.mass  = kwargs.get( "mass" , 1 )

    def set_screen_pos( self, screen_dim , R = 25 ):

        cart = ( self.fx , self.fy )
        x , y = coord_convert( cart , screen_dim , R = 25 )
        # self.set_postion( x , y )
        self.x = x
        self.y = y
    
    def move( self, dt, g = 9.81 ):
        
        self.old = ( self.fx , self.fy )

        self.fy += self.vy*dt 
        self.fx += self.vx*dt 
 
        self.vy = self.vy - g*dt
    
    def reset_position( self ):

        ox , oy = self.old
        self.fx = ox
        self.fy = oy

    def simple_bounce( self, k = .8 , vertical = False ):

        '''
        versão mais simplificada. Paredes sempre retas
        '''

        self.reset_position()

        k = numpy.clip( k, 0 , 1. )
        if vertical: 
            self.vy *= -k
            return
        self.vx *= -k


    def bounce( self , **kwargs ):
        
        '''
        alteração do movimento da bola quando quando bate
        na superficie. No caso geral a barra, teto ou chão.
        Essa função tem como efeito colateral a mudança 
        nos valores de vx e vy da bola, e retorna a quantida
        de de energia dissipada na colisão, para computar o
        quão alto será o som do impacto. Quando nenhum argumento
        for passado. Considera-se o chão a superfície.
        '''

        #--------------------------------------------------
        # a massa do objeto que colide. Para fins práticos o chão e 
        # teto tem massa infinita
        mass = kwargs.get( 'mass' , sys.maxsize )

        #--------------------------------------------------
        # o angulo que o vetor normal a superfície faz com o eixo
        # x. Relevante pois planejo fazer a barra dos jogadores
        # inclinável.
        norm = kwargs.get( 'norm' , numpy.pi/2 )

        # velocidade da superfície, caso se mova.
        ux = kwargs.get( 'ux' , 0 )
        uy = kwargs.get( 'uy' , 0 )
        
        #--------------------------------------------------
        # coeficiente de restituição. Varia de 0 ( Colisão perfeita
        # mente inelástica ) a 1. ( perfeitamente elástica ). É usada
        # para calcular a dissipação de energia. 
        k = kwargs.get( 'k' , .8 )


def test_1():

    width , height = 800 , 800
    w = Window( width , height )
    w.set_title( 'bolinha' )

    b = Bolinha( 'basquete.png' , vx = -15 , vy = -25)
    
    w.delta_time()
    while True:
        w.set_background_color( ( 255 , 255 , 255 ) )
        b.draw()

        dt = w.delta_time()
        b.move( dt )
        b.set_screen_pos( ( width , height ) )

        #--------------------------------------------------
        # checando colisões. Só temos paredes, então sem os
        # métodos da classe Colided, por enquanto
        print( b.fx , b.x )
        if b.x + b.width > width or b.x < 0:
            b.simple_bounce( )
        elif b.y < 0 or b.y + b.height > height:
            b.simple_bounce( vertical = True )

        w.update()


def test_2():

    width , height, R = 800 , 800, 25
    w = Window( width , height )
    w.set_title( 'bolinha' )

    seq = []
    num_bolas = 15
    for i in range( num_bolas ):

        vx , vy = -10 + 20*numpy.random.rand(2)
        x = numpy.random.randint( low = -width//( 2*R ) , high = width//( 2*R ) )
        y = numpy.random.randint( low = -height//( 2*R ) , high = height//( 2*R ) )
        b = Bolinha( 'basquete.png' , vx = vx , vy = vy , center = ( x , y ) )
        seq.append( b )
    
    w.delta_time()
    while True:
        w.set_background_color( ( 255 , 255 , 255 ) )

        dt = w.delta_time()
        for b in seq:

            b.move( dt )
            b.draw()
            b.set_screen_pos( ( width , height ) )

            if b.x + b.width > width or b.x < 0:
                b.simple_bounce( k = 1 )
            elif b.y < 0 or b.y + b.height > height:
                b.simple_bounce( k = 1 , vertical = True )

        ball_seqs = space_partition( seq )
        pos_col   = check_collisions( ball_seqs )
        for b1 , b2 in pos_col:
            handle_collision( b1 , b2 )
            handle_collision( b2 , b1 )   

        w.update()
        
        
if __name__ == "__main__":
    # test_1()
    test_2()
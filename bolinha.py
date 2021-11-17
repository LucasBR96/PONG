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

# utilidades
from utils import colisao_bw


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

    def impulso( self , ix , iy ):

        '''
        o impulso é a variação da quantidade de movimento
        '''

        m = self.mass
        vx = self.vx
        vy = self.vy

        self.vx = ( ix + vx*m )/m
        self.vy = ( iy + vy*m )/m

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
        norm = kwargs.get( 'norm' , numpy.array( [ 0 , 1 ] ) )

        # velocidade da superfície, caso se mova.
        ux = kwargs.get( 'ux' , 0 )
        uy = kwargs.get( 'uy' , 0 )
        
        #--------------------------------------------------
        # coeficiente de restituição. Varia de 0 ( Colisão perfeita
        # mente inelástica ) a 1. ( perfeitamente elástica ). É usada
        # para calcular a dissipação de energia. 
        k = kwargs.get( 'k' , .8 )

        
        #projetando 

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
        ix , iy = colisao_bw( b , ( width , height ) )
        if not( ix == 0 and ix == iy ):
            b.impulso( ix , iy )
            b.reset_position()
        
        w.update()




        
if __name__ == "__main__":
    test_1()


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
        self.vx = kwargs.get( "vx" , 15 )
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


def test_1():

    width , height = 800 , 800
    w = Window( width , height )
    w.set_title( 'bolinha' )

    b = Bolinha( 'basquete.png' )
    
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


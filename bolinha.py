# biblioteca padrão
import math
import sys
import time
import argparse

# biblioteca de terceiros
import numpy
import pygame
import PPlay
from PPlay.sprite import *

class Bolinha( PPlay ):

    def __init__( self , image_file, center, **kwargs ):

        super().__init__( "assets/imagens/" + image_file )
        
        x , y = center/2
        self.set_position( x , y )
        
        # metros por segundo
        self.vx = kwargs.get( "vx" , 10 )
        self.vy = kwargs.get( "vy" , 0 )
         
        # quilogramas
        self.mass  = kwargs.get( "mass" , 1 ) 
    
    def move( self, dt, g = 9.81 ):

        self.move_y( self.vy*dt )
        self.move_x( self.vx*dt )
 
        self.vy = self.vy - g*dt
    
    def simple_bounce( self, k = .8 , vertical = False ):

        '''
        versão mais simplificada. Paredes sempre retas
        '''

        k = numpy.clip( k, 0. , 1. )
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
        mass = kwargs.get( 'mass' , sys.maxint )

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


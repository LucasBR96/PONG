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
        self.speed = kwargs.get( "speed" , 10 )
        
        # angulo com o eixo x, em radianos
        self.theta = kwargs.get( "theta" , 0 )  
        
        # quilogramas
        self.mass  = kwargs.get( "mass" , 1 ) 
    
    def to_vectorial( self ):

        vy = numpy.sin( self.theta )*self.speed
        vx = numpy.cos( self.theta )*self.speed

        return vx , vy

    def move( self, dt ):

        vx , vy = self.to_vectorial()
        self.move_y( vy*dt )
        self.move_x( vx*dt )

    def update_speed( vx , vy ):

        self.speed = numpy.sqrt( vx**2 + vy**2 )
        self.theta = numpy.arctan( vy/vx )

    def fall( self , dt , g = 9.81 ):

        #g é o coeficiente de acc da gravidade
 
        vx , vy = self.to_vectorial()
        vy = vy - g*dt
        self.update_speed( vx , vy )
    
    def bounce( self , **kwargs ):

        #--------------------------------------------------
        # é a bola sendo rebatida, reage a uma colisão com
        # o chão, o teto, o chão ou uma das barras. A função recebe
        # massa, o vetor velocidade do objeto que colidiu, além do 
        # coeficiente de restituição. Retorna a quantidade de energia
        # dissipada.



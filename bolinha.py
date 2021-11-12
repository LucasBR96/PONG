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


    def move( self, dt ):

        vy = numpy.sin( self.theta )*self.speed
        self.move_y( vy*dt )

        vx = numpy.cos( self.theta )*self.speed
        self.move_x( vx*dt )

    def fall( self , dt , g = 9.81 ):

        #g é o coeficiente de acc da gravidade



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
from utils import *
from constantes import *

class barra:

    @classmethod
    def right( cls ):
        return cls()
    
    @classmethod
    def left( cls ):
        return cls(
            pos      = LEFT_PAD,
            norm     = LEFT_NORM,
            outerbox = LEFT_BOX
        )

    def __init__( self , **kwargs ) -> None:
        
        self.pos = kwargs.get('pos', numpy.array( RIGHT_PAD ) )
        self.basepos = self.pos.copy() #depois de ponto marcado, retornar à posição original
        self.height = kwargs.get( 'height' , PAD_TAM )
        self.speed = numpy.zeros( 2 )
        
        #------------------------------------------------------------
        # O pad pode ser rotacionado, e norm é o vetor unitŕaio perpendicular
        # à barra, indicando a inclinação
        self.norm = kwargs.get( 'norm' , RIGHT_NORM  )
        self.basenorm = self.norm.copy()
        self.rot_speed = kwargs.get( 'rot_speed' , ROT_SPEED )
        self.max_theta = kwargs.get( 'max_theta' , MAX_THETA )

        self.mass = kwargs.get( 'mass' , 1. )

        #------------------------------------------------------------
        # Se for nescessário retornar à posição original. Por exemplo
        # em caso de colisão
        x , y  = self.pos
        self.previous_pos  = ( x , y )

        nx , ny = self.norm
        self.previous_norm = ( nx , ny ) 

        #-------------------------------------------------------------
        # Area em que o pad fica restrito
        self.outerbox = kwargs.get("outerbox" , RIGHT_BOX )

        self.score = 0

    def get_edges( self ):

        v = self.norm*self.height/2
        rot_mat = numpy.array([ [ 0 , -1. ] , [ 1 , 0 ] ])
        
        x1 = self.pos + v@( -rot_mat )
        x2 = self.pos + v@( rot_mat )

        return x1 , x2
        
    def reset_vars( self , point = False ):

        
        p0 = self.basepos if point else self.previous_pos
        self.pos = numpy.array( p0 )

        n0 = self.basenorm if point else self.previous_norm
        self.norm = numpy.array( n0 )

    def move( self , dt ):

        if ( self.speed**2 ).sum() == 0.: return 

        x , y = self.pos
        self.previous_pos = ( x , y )
        self.pos += self.speed*dt
    
    def out_of_thebox( self ):

        pos1 , pos2 = self.get_edges()
        x1 = min( pos1[0] ,pos2[ 0 ] )
        x2 = max( pos1[0] ,pos2[ 0 ] )
        y1 = min( pos1[1] ,pos2[ 1 ] )
        y2 = max( pos1[1] ,pos2[ 1 ] )

        x , y , w , h = self.outerbox
        xmin , xmax , ymin , ymax = x , x + w , y , y + h

        a = ( xmin <= x1 ) and ( x2 <= xmax )
        b = ( ymin <= y1 ) and ( y2 <= ymax )
        return not( a and b )

    def rotate( self , dt , clockwise = True):

        self.previous_norm = self.norm.copy()

        k = -1 if clockwise else 1
        d_theta = k*self.rot_speed*dt
        dx = numpy.cos( d_theta )
        dy = numpy.sin( d_theta )
        self.norm += numpy.array( [ dx , dy ] )

    def over_tilt( self ): 

        # o pad está inclinado mais do que o máximo permitido
        return ( self.norm.dot( self.basenorm ) ) > numpy.cos( self.max_theta )

        
class barra_spr( Sprite ):

    def __init__( self , **kwargs ):
        
        image_file = kwargs.get( 'image_file' , PAD_IMG)
        super().__init__( "assets/images/" + image_file )

        self.barra = barra( **kwargs )
        self.conv = coord_conv( **kwargs )
        
    
    def convert_pos( self ):

        x1 , x2 = self.barra.get_edges()
        x , y = x1 if x1[1] > x2[1] else x2 
        true_x , true_y = self.conv.from_virtual( x , y )
        self.set_position( true_x , true_y )
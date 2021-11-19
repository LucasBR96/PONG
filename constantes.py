import numpy

# Dimensões virtuais e reais
QUADRA_DIM = ( 12 , 6 )
SCREEN_DIM = ( 960 , 480 )
R = SCREEN_DIM[ 0 ]/QUADRA_DIM[ 0 ]

# Bola
BOLA_VEL   = numpy.array( [ 10 , 0. ] )
BOLA_START = numpy.array( 6 , 3 )
BOLA_MASS  = .3

# Pad
PAD_TAM    = 2.
PAD_SPEED  = 5.

# Física
G =  9.81   # Acc da Gravidade
K = .8      # Coef de restituição

# Imagens
BOLA_IMG = 'basquete.png'

# Paredes
NO_WALL    = 0
FRONT_WALL = 1
CEIL       = 2
BACK_WALL  = 3
FLOOR      = 4
import numpy

# dimensões virtuais e reais
QUADRA_DIM = ( 12 , 6 )
SCREEN_DIM = ( 960 , 480)
R = SCREEN_DIM[ 0 ]/QUADRA_DIM[ 0 ]

# bola
BOLA_VEL   = numpy.array( [ 10 , 0. ] )
BOLA_START = numpy.array( 6 , 3 )
BOLA_MASS  = .3


PAD_TAM    = 2.

# Física
G =  9.81   # Acc da Gravidade
K = .8      # Coef de restituição

# Imagens
BOLA_IMG = 'basquete.png'
import numpy

# Dimensões virtuais e reais
QUADRA_DIM = ( 13 , 6 )
SCREEN_DIM = ( 1040 , 480 )
R = SCREEN_DIM[ 0 ]/QUADRA_DIM[ 0 ]

# Bola
BOLA_VEL   = 5.
BOLA_THETA = numpy.pi/3
BOLA_START = numpy.array( [ 6. , 3. ] )
BOLA_MASS  = .3

# Pad
PAD_TAM    = 1.5
PAD_SPEED  = 4.
ROT_SPEED  = 1.
MAX_THETA  = numpy.pi/3
RIGHT_NORM = numpy.array( [1. , 0 ] )
RIGHT_PAD  = numpy.array( [ QUADRA_DIM[0]/4 , QUADRA_DIM[1]/2 ] )
RIGHT_BOX  = [ 0 , 0 , QUADRA_DIM[0]/3 , QUADRA_DIM[1] ]
LEFT_NORM  = numpy.array( [-1. , 0 ] )
LEFT_PAD   = numpy.array( [ 3*QUADRA_DIM[0]/4 , QUADRA_DIM[1]/2 ] )
LEFT_BOX   = [ 2*QUADRA_DIM[0]/3 , 0 , QUADRA_DIM[0]/3 , QUADRA_DIM[1] ]

# Física
G = 2.81   # Acc da Gravidade
K = 1.   # Coef de restituição

# Imagens
BOLA_IMG = 'basquete.png'
PAD_IMG  = 'Pad.png'

# Paredes
NO_WALL    = 0
FRONT_WALL = 1
CEIL       = 2
BACK_WALL  = 3
FLOOR      = 4

#Colisoes com o Pad
FRONT_PAD = 1
BACK_PAD  = -1
NO_PAD    = 0

#Teclado
RPAD_KEYS = ['w' , 's' , 'a' , 'd' ]
LPAD_KEYS = ['i' , 'k' , 'j' , 'l' ]
PAUSE     = 'space'
# GAME_KEYS = RPAD_KEYS | { LPAD_KEYS } | { PAUSE }
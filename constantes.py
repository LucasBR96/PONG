import numpy

# Dimensões virtuais e reais
R = 80
QUADRA_W = 13
QUADRA_H = 6
SCREEN_W = QUADRA_W*R
SCREEN_H = QUADRA_H*R
# QUADRA_DIM = ( 13 , 6 )
# SCREEN_DIM = ( 1040 , 480 )
# R = SCREEN_W/QUADRA_W

# Bola
BOLA_VEL   = 5.              # Modulo da velocidade inicial
BOLA_THETA = numpy.pi/3
BOLA_START = numpy.array( [ QUADRA_W , QUADRA_H ] )/2
BOLA_MASS  = .3

# Placares
FONT_SIZE = 28
PLACAR_Y  = SCREEN_H/2
PLACAR1_X = SCREEN_W/8
PLACAR2_X = 7*SCREEN_W/8

# Pausa
PAUSE_X = ( SCREEN_W/2 ) - 3*FONT_SIZE
PAUSE_Y = ( SCREEN_H/2 ) - .5*FONT_SIZE

# Tempos Padrão
PAUSE_T = .1
BACK_DT = .01
TICKS   = 100

# Pad
PAD_TAM    = 1.5
PAD_SPEED  = 4.
PAD_MASS   = 1.
RIGHT_PAD  = numpy.array( [ QUADRA_W/4 , QUADRA_H/2 ] )
RIGHT_BOX  = [ 0 , 0 , QUADRA_W/3 , QUADRA_H ]
LEFT_PAD   = numpy.array( [ 3*QUADRA_W/4 , QUADRA_H/2 ] )
LEFT_BOX   = [ 2*QUADRA_W/3 , 0 , QUADRA_W/3 , QUADRA_H ]

# Física
G = 9.81   # Acc da Gravidade
K = 1.     # Coef de restituição

# Imagens
BOLA_IMG = 'basquete.png'
PAD_IMG  = 'Pad.png'

# colisoes com paredes
NO_WALL    = 0
FRONT_WALL = 1
CEIL       = 2
BACK_WALL  = 3
FLOOR      = 4

#Colisoes com o Pad
NO_PAD    = 0
SIDE_PAD  = 1
OVR_PAD   = 2 # Tanto em cima como abaixo

#Teclado
RPAD_KEYS = ['w' , 's' , 'a' , 'd' ]
LPAD_KEYS = ['i' , 'k' , 'j' , 'l' ]
PAUSE     = 'space'
# GAME_KEYS = RPAD_KEYS | { LPAD_KEYS } | { PAUSE }
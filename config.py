WIN_WIDTH = 640  #640
WIN_HEIGHT = 480 #480
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 4 #top
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

#RGB(red,green,blue)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B.....E............B',     
    'B..........BBB..E..B',        
    'B...BBB......B.....B', 
    'B..................B', 
    'B........P.........B', 
    'B.BB...............B', 
    'B..E..B............B', 
    'B.....BBB..........B', 
    'B.......B..........B', 
    'B.......B....B.....B', 
    'B.............E....B',  
    'B.........E.....B..B', 
    'B..................B', 
    'BBBBBBBBBBBBBBBBBBBB',
    ]

SERVER_HOST = '10.107.25.172'
SERVER_PORT = 54323
score = ''

#constantes que utilizamos en todo el proyecto
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

TITLE = "PY TANK"

FONT_TYPE = "Inter"

BULLETS = []

#coordenadas de balas
PICKUP_SPOTS = [
    (220, 140),
    (400, 300),
    (700, 500)
]

#lista de pickups en pantalla
PICKUP_ITEMS = []

last_pickup_time = 0

PICKUP_INTERVAL = 10000

ENEMIES = []
ENEMIES_RECTS = []

#definimos tamaño de botones
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 50
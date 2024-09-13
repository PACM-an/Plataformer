import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#Cargar Math
import math
# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from O_Wall import Walls
from O_Floor import Floors
from O_Fake_Floor import Fake_Floors
from O_Lava import Lavas
from O_Proyectile import Balls
from objloader import *

"""CHOOSE YOUR LEVEL!!!

    By changing the value of actLevel, you can see other examples of how to use the materials.
    1 = Basic level
    2 = Maze like level
    3 = Hard plataformer level
    
    
"""
actLevel = 1  #<----- CHOOSE YOUR LEVEL!!!

#Configuracion de pantalla
screen_width = 1280 #800
screen_height = 720 #800
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = -80.0
EYE_Y = 5.0
EYE_Z = 50.0
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 50.0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-100
X_MAX=100
Y_MIN=-100
Y_MAX=100
Z_MIN=-100
Z_MAX=100
#Dimension del plano
DimBoard = 200
sky = 2000
#Variable de control observador
dir = [1.0, 0.0, 0.0]
#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 20
#Variables para el control del observador
theta = 1.0
radius = 300

#Configuración de la cámara (Mpuse)
#   + En esta parte se optiene la uibación del mouse
camera_x, camera_y = 0, 0
CAMERA_SPEED = 5
MOUSE_BORDER = 630
#   + En cada cuanto se actualiza el cursor para volver a 0
timer = 0

#Gravedad y suelo
gravity = 0
eye_up = 5
#   + actLevel del suelo: donde la camara se encuentra realmente
Ground_level = 5

# Uso de shift:
oldDir = [1.0, 0.0, 0.0]
#   + Estamina
fuel = 1000
fuel_text = "AAAAAAAAAAAAAAAAAAAAAAAAA" # 25 A
n = 0

# Pared
#   + Wall = [inicio xz, final xz, jump true/false]
Wall = []
Wall_Obj = []
End = []
End_Obj = []
# Suelo
#   + Floor = [x1, z1, x2, z2, x3, z3, x4, z4, Y]
Floor = []
Floor_Obj = []
Fake_Floor_Obj = []

# Lava
#   + Lava = [x1, z1, x2, z2, x3, z3, x4, z4]
Lava = []
Lava_Obj = []

#Arreglo para el manejo de texturas
textures = []
filename1 = "./textures/grass.bmp"
filename2 = "./textures/stone.bmp"
filename3 = "./textures/wood.bmp"
filename4 = "./textures/floss.bmp"
filename5 = "./textures/lava.bmp"
filename6 = "./textures/Win.bmp"

#Enemigos
objetos = []
Enemy = []
#   + Tiempo de tiro (y eliminar ls otras balas igual)
Shoottime = 150
time = 0
#   + bullet = (x1, z1, y1, m)
bullet_obj = []

#INICIO DEL JUEGO
pygame.init()

# Texto en pantalla
# Pd: saqué a pygame del Init, necesito screen
screen = pygame.display.set_mode(
    (screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL: cubos")
    
# Configuración de la fuente
#   + Texto clasico: font = pygame.font.SysFont("Arial", 18)
font_path = "./GG.ttf"
font_size = 30
font = pygame.font.Font(font_path, font_size)

# Inicializar el mixer de pygame
pygame.mixer.init()
# Cargar el archivo de audio
if(actLevel == 1):
    pygame.mixer.music.load("./music/Gdash.mp3")
elif (actLevel == 2):
    pygame.mixer.music.load("./music/CDave.mp3")
else:
    EYE_Y = 105.0
    pygame.mixer.music.load("./music/Gzilla.mp3")

# Crear esferas:
sphere = gluNewQuadric()

# Activar axis en caso de ver punto de origen y referencias:
def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    """
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    """
    #Axis TUTORIAL
    #Axis que crea una flecha que indica que puedes saltar
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(19.0,0.0,30.0)
    glVertex3f(19.0,19.0,30.0)
    glEnd()
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(19.0,10.0,21.0)
    glVertex3f(19.0,19.0,30.0)
    glEnd()
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(19.0,19.0,30.0)
    glVertex3f(19.0,10.0,39.0)
    glEnd()
    
    glLineWidth(1.0)
    
#Codigo para la carga de texturas
def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)       # Uso de las imagenes
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size                                     # Obtiene sus dimensiones
    image_data = pygame.image.tostring(image,"RGBA")                 # Da las dimensiones de las imagenes
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 

#Funcion Init
def Init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Carga de texturas
    Texturas(filename1)
    Texturas(filename2)
    Texturas(filename3)
    Texturas(filename4)
    Texturas(filename5)
    Texturas(filename6)
    
    """
   TUTORIAL FOR CREATING OBJECTS:
    
    WALL:
    #           x1  z1  x2   z2   jump
    Wall.append([20, 20, 20, 40, True])
    
    END TROPHY WALL:
    #           x1  z1  x2   z2   TRUE always
    End.append([20, 20, 20, 40, True])
    
    FLOOR:
    #           x1   z1   x2  z2  Length  height
    Floor.append([20, 20, 20, 40,   40,     20])
    - x1 and x2 are always the same.
    - Length and height are other coordinates in x or y, respectively.
    
    
    LAVA:
    #           x1   z1   x2  z2  Length
    Lava.append([160, 10, 160, 90, 240])
    
    - x1 and x2 are always the same.
    - Length is another coordinate in x. It does not refer to how long it is, but rather to the point where it is.
    
    
    FAKE FLOOR:
    #           x1   z1     x2    z2  longitud  altura
    Fake_Floors(-400, -80, -400, 200,   300,      0)
    - The same as floor, but with a stone texture and no collision.
    - Its only purpose is to create text on the ground; you can see 
    that there are several of these created in the line with the comment: #Only texture (FAKE FLOORS)
    
    
    ENEMY:
    #            x   z   y  (Todas coordenadas)
    Enemy.append([0, 10, 0])
    
    
    RULES:
    1. When creating a wall, x1 == x2 or z1 == z2; at least one of these conditions must be met.
    2. When creating a wall, floor, or lava, x1 and z1 MUST always be less than or equal to x2 and z2.
        If this is not the case, it is a pass-through object (without a hitbox).
    
    """
    
    if (actLevel == 2):
        #PAREDES:
        # Adelante
        Wall.append([-20, 20, -20, 160, False])
        
        # Atrás
        Wall.append([-100, 20, -100, 80, False])
        
        # Izquierda
        Wall.append([-100, 20, -20, 20, False])
        
        # Derecha
        Wall.append([-40, 80, -100, 80, False])
        # Vuelta
        Wall.append([-40, 80, -40, 140, False])
        # Vueta derecha
        Wall.append([-60, 160, -20, 160, False])
        # Vueta vuelta derecha
        Wall.append([-60, 110, -60, 160, False])
        # Vueta vuelta vuelta derecha (Paralela a derecha)
        Wall.append([-110, 90, -40, 90, False])
        Wall.append([-130, 110, -60, 110, False])
        # Paralelea a adelante y atrás
        Wall.append([-130, -20, -130, 110, False])
        Wall.append([-110, 10, -110, 90, False])
        # Paralelea izquierda
        Wall.append([-110, 10, 40, 10, False])
        Wall.append([-130, -20, 80, -20, False])
        Wall.append([-90, -5, -90, 10, True])
        Wall.append([-50, -20, -50, -5, True])
        # Paralela adelante (Pasillo gordo)
        Wall.append([80, -20, 80, 200, False])
        Wall.append([40, 10, 40, 170, False])
        # Vuelta derecha Pasillo gordo (paralela derecha) Pasillo vert
        Wall.append([-40, 200, 80, 200, False])
        Wall.append([-80, 170, 40, 170, False])
        # Vuelta Pasillo vert
        Wall.append([-80, 170, -80, 240, False])
        Wall.append([-40, 200, -40, 210, False])
        # Paralelo pasillo vert
        Wall.append([-40, 210, 140, 210, False])
        Wall.append([-80, 240, 180, 240, False])
        # Paralelo pasillo gordo (vuelta izq pasillo vert)
        Wall.append([180, -40, 180, 240, False])
        Wall.append([140, -80, 140, 210, False])
        Wall.append([160, 150, 180, 150, True])
        Wall.append([140, 40, 160, 40, True])
        # Vuelta derecha (pasillo final)
        Wall.append([140, -80, 220, -80, False])
        Wall.append([180, -40, 220, -40, False])
        # Pared final
        Wall.append([220, -80, 220, -40, False])
        End.append([210, -80, 210, -40, True]) #Cuando ves esta pared, listo

        
        #SUELOS:  
        #Floor.append([20, 20, 20, 40, 40, 20])
        Floor.append([-40, 20, -40, 80, 10, 20])
        # Vuelta derecha
        Floor.append([-60, 140, -60, 160, 10, 40])
        # Paralelea izquierda
        Floor.append([0, -20, 0, -10, 80, 20])
        # Paralela adelante pasillo gordo
        Floor.append([60, 170, 60, 200, 80, 30])
        # Paralela pasillo vert
        Floor.append([50, 220, 50, 240, 80, 20])
        
        
        #LAVA:
        #Lava.append([-20, 20, -20, 80, -60])
        Lava.append([-60, 20, -60, 80, 40])
        Lava.append([-100, 20, -100, 30, 40])
        Lava.append([-100, 70, -100, 80, 40])
        # Vuelta derecha
        Lava.append([-40, 80, -40, 160, 40])
        Lava.append([-60, 110, -60, 160, 40])
        # Pasillo paralelo a adelante y atrás
        Lava.append([-130, 70, -130, 80, 40])
        Lava.append([-130, 20, -130, 30, 40])
        # Paralelea izquierda
        Lava.append([-20, -20, -20, 10, 100])
        # Paralela adelante (Pasillo gordo)
        Lava.append([40, 10, 40, 70, 80])
        Lava.append([40, 150, 40, 200, 80])
        Lava.append([-20, 150, -20, 200, 80]) #Paralelo derecha (Pasillo vert)
        # Paralela pasillo vert
        Lava.append([-10, 210, -10, 240, 140])
        # Paralela pasillo gordo
        Lava.append([180, 110, 180, 150, 20])
        Lava.append([180, -20, 180, 40, 20])    
        # Lanzaguisantes
        Enemy.append([-60, 70, 0])
        Enemy.append([-30, 30, 21])
        Enemy.append([-120, -20, 0])
        Enemy.append([50, 120, 0])
        Enemy.append([-70, 230, 0])
        Enemy.append([150, -70, 0])
    elif (actLevel == 3):
        # EJEMPLO
        #BARRERA 1
        #SUELOS:
            #plataforma del inicio:
        Floor.append([-350, -100, -350, 100, -20, 100])

        #paredes laterales a la plataforma del inicio:
        Wall.append([-350, -100, -20, -100, False])
        Wall.append([-350, 100, -20, 100, False])
        Wall.append([-350, -100, -350, 100, False])
        Wall.append([-20, -100, 210, -100, False])

        Floor.append([20, 20, 20, 40, 40, 20])
        #suelo falso buggeando el suelo para plataformas
        Floor.append([100, 0, 100, -20, 120, 20])
        Floor.append([140, 40, 140, 20, 160, 20])

        #BARRERA 1
        Wall.append([210, -100, 210, 100, True])
        
        # -------------------------plataformas detras de la barrera 1--------------------------------------------
        Floor.append([225, -60, 225, -30, 270, 10])

        Floor.append([280, 80, 280, 100, 300, 5])
        Floor.append([390, 20, 390, 40, 410, 30])
        Floor.append([340, -100, 340, -80, 360, 50])
        Floor.append([260, -1, 260, 19, 280, 80])
        Floor.append([310, 100, 310, 80, 330, 90])
        Floor.append([390, -10, 390, 10, 410, 100])


        Floor.append([305, -10, 305, -30, 325, 130])
        #Floor.append([250, -30, 250, -10, 270, 130])


        Floor.append([305, -100, 305, -80, 325, 130])
        Floor.append([250, -100, 250, -80, 270, 130])


        Floor.append([305, -150, 305, -170, 325, 130])
        Floor.append([250, -170, 250, -150, 270, 130])



        Floor.append([305, -240, 305, -220, 325, 130])
        Floor.append([250, -220, 250, -240, 270, 130])

        Floor.append([305, -290, 305, -310, 325, 130])
        Floor.append([250, -290, 250, -310, 270, 130])

        Floor.append([305, -370, 305, -390, 325, 130])
        Floor.append([250, -390, 250, -370, 270, 130])
        #Floor.append([280, -350, 280, -330, 300, 130])
        #Floor.append([305, 40, 305, 60, 325, 130])
        Lava.append([-20, -100, -20, 100, 271])
        Lava.append([271, -100, 271, 100, 410])

        #paredes laterales a la lava
        Wall.append([-20, 100, 210, 100, False])
        Wall.append([210, 100, 410, 100, False])
        Wall.append([410, -100, 410, 100, False])
        Wall.append([410, -520, 410, -100, False])
        Wall.append([210, -480, 210, -100, False])
        #Wall.append([210, -450, 410, -450, False])

        Lava.append([200, -520, 200, -100, 410])
        Wall.append([150, -520, 410, -520, False])
        Wall.append([150, -520, 150, -480, False])
        Wall.append([150, -480, 210, -480, False])
        Floor.append([150, -520, 150, -480, 250, 10])

        #ENEMIGO:
        #enemigos de la plataforma de incio
        Enemy.append([-300, 20, 100])
        Enemy.append([-300, 20, 110])
        Enemy.append([-300, 20, 120])
        Enemy.append([-300, 20, 130])
        
        End.append([151, -480, 151, -520, True])
        
        enemy_pos_y = 0
        for i in range(15):
            Enemy.append([210, 90, enemy_pos_y])
            enemy_pos_y = enemy_pos_y + 15

        enemy_pos_y = 0
        for i in range(15):
            Enemy.append([210, -90, enemy_pos_y])
            enemy_pos_y = enemy_pos_y + 15

        enemy_pos_y = 90
        for i in range(8):
            Enemy.append([310, -300, enemy_pos_y])
            enemy_pos_y = enemy_pos_y + 10

        #Enemy.append([210, 20, 0])
        #Enemy.append([0, 0, 0])
        #Enemy.append([400, 0, 0])
        #Enemy.append([200, 30, 40])

    else:
        # EJEMPLO
        #BARRERA 1
        Wall.append([20, 20, 20, 40, True])
        Wall.append([20, 40, 20, 60, True])
        Wall.append([20, 60, 20, 80, True])
        #BARRERA 2  
        Wall.append([160, 20, 160, 40, True])
        Wall.append([160, 40, 160, 60, True])
        Wall.append([160, 60, 160, 80, True])
        #PARED INICIAL (Paredes del lobby, 2 por pared)
        Wall.append([20, 80, 20, 200, False])
        Wall.append([20, -80, 20, 20, False])
        Wall.append([-80, -70, 20, -70, False])
        Wall.append([-200, -70, -80, -70, False])
        Wall.append([-80, 200, 20, 200, False])
        Wall.append([-200, 200, -80, 200, False])
        Wall.append([-200, -70, -200, 45, False])
        Wall.append([-200, 45, -200, 200, False])
        #PARED FONDO LATERALES
        Wall.append([20, 80, 240, 80, False])
        Wall.append([20, 20, 240, 20, False])
        Wall.append([20, 90, 240, 90, False])
        Wall.append([20, 10, 240, 10, False])
        Wall.append([240, 80, 240, 90, False])
        Wall.append([240, 10, 240, 20, False])
        #Pared que no se ve
        Wall.append([200, 90, 200, 200, False])
        Wall.append([200, -200, 200, 10, False])
        
        
        #LOBBY 2 (PARED FONDO LITERAL)
        Wall.append([700, -80, 700, 30, False])
        Wall.append([700, 70, 700, 200, False])
        Wall.append([700, 30, 1100, 30, False])
        Wall.append([700, 70, 1100, 70, False])
        Wall.append([1100, 0, 1100, 100, False])
        End.append([1099, 30, 1099, 70, True])
        
        
        # LOBBY 2 LATERALES
        Wall.append([400, -80, 700, -80, False])
        Wall.append([400, 200, 700, 200, False])
        Wall.append([100, -80, 400, -80, False])
        Wall.append([100, 200, 400, 200, False])
        #Paredes que van lateral a lava 1
        Wall.append([240, 10, 320, 10, True])
        Wall.append([240, 90, 320, 90, True])
        Wall.append([320, 10, 400, 10, True])
        Wall.append([320, 90, 400, 90, True])
        Wall.append([400, 10, 400, 45, True])
        Wall.append([400, 45, 400, 90, True])
        
        #SUELOS:
        Floor.append([20, 20, 20, 40, 40, 20])
        Floor.append([40, 20, 40, 40, 80, 20])
        Floor.append([80, 20, 80, 40, 120, 20])
        #Piso más alto
        Floor.append([180, 20, 180, 40, 220, 40])
        #Piso aun más alto
        Floor.append([80, 60, 80, 100, 180, 100])
        
        #LAVA:
        Lava.append([160, 10, 160, 90, 240])
        Lava.append([240, 10, 240, 90, 320])
        Lava.append([320, 10, 320, 90, 400])
        
        #LAVA PARTE 2:
        Lava.append([450, -100, 450, 10, 650])
        Lava.append([450, 90, 450, 200, 650])
        
        #LAVA FINAL:
        Lava.append([800, 0, 800, 100, 900])
        
        
        #ENEMIGO:
        Enemy.append([0, 10, 0])
        Enemy.append([0, 0, 0])
        Enemy.append([0, 80, 0])
        Enemy.append([0, 90, 0])
        Enemy.append([700-10, 0, 0])
        Enemy.append([700-10, 100, 0])
        Enemy.append([200, 30, 40])
    
    #CREACION DE LOS OBJETOS INDICADOS
    for i in Wall:
        [x11, z11, x22, z22, jump] = i
        Wall_Obj.append(Walls(x11, z11, x22, z22, jump))
        
    for i in End:
        [x11, z11, x22, z22, jump] = i
        End_Obj.append(Walls(x11, z11, x22, z22, True))
        
    for i in Floor:       
        [x1, z1, x2, z2, la_Z, la_Y] = i
        Floor_Obj.append(Floors(x1, z1, x2, z2, la_Z, la_Y))
    
    for i in Lava:
        [x1, z1, x2, z2, la_Z] = i
        Lava_Obj.append(Lavas(x1, z1, x2, z2, la_Z))
        
    #Solo textura (FAKE FLOORS)
    if (actLevel == 3):
        Fake_Floor_Obj.append(Fake_Floors(-800, -100, -800, 450, -400, 0))
        Fake_Floor_Obj.append(Fake_Floors(-400, -100, -400, 450, -200, 0))
        Fake_Floor_Obj.append(Fake_Floors(-200, -200, -200, -80, 200, 0))
    nLenght = 10
    v = 0
    for i in range(nLenght):
        v = v + 200  
        #Fake_Floor_Obj.append(Fake_Floors(-400 + v, -80, -400 + v, 200, v, 0))
        Fake_Floor_Obj.append(Fake_Floors(-400 + v, -80, -400 + v, 450, v, 0))
    
    #DISEÑOS OPCIONALES (Para otra iluminacion en caso de querrer)    
    #glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    #glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glEnable(GL_COLOR_MATERIAL)
    #glShadeModel(GL_SMOOTH)
    
    #Creando a los enemigos (con o sin detalles de arriba)
    num = 0
    for i in Enemy:       
        objetos.append(OBJ(".\Enemy\scene.obj", swapyz=True))
        objetos[num].generate()
        num = num + 1
    

#Funcion para rotar la camara aplicando matriz de giro
def rota_obs():
    global theta
    global dir
    angulo = math.radians(theta)
    new_x = math.cos(angulo)*dir[0] + math.sin(angulo)*dir[2]
    new_z = - math.sin(angulo)*dir[0] + math.cos(angulo)*dir[2]
    dir[0] = new_x
    dir[2] = new_z

#Funcion para mostrar el objeto enemigo  
def displayobj(n, x4, y4, z4, arconte_g):
    glPushMatrix()  
    #Correcciones para dibujar el objeto en plano XZ
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(x4, -y4, z4)
    #Correcciones al girar y mirar al objetivo jugador
    if (EYE_X > x4):
        glRotatef(-arconte_g + 90, 0.0, 0.0, 1.0)
    else:
        glRotatef(-arconte_g - 90, 0.0, 0.0, 1.0)
    glScale(7.0,7.0,7.0)
    objetos[n].render()  
    glPopMatrix()
    
#Funcion para mover el mouse al centro    
def teleport_mouse_to_center():
    center_x = screen.get_width() // 2 #Mitad de la pantalla
    center_y = screen.get_height() // 2 #Mitad de la pantalla
    pygame.mouse.set_pos(center_x, center_y) #Teleport a mitad mitad pantalla
    
#Funcion para direcciones A, B del jugador
def get_right_vector(direction, up):
    #Calcula el vector derecho usando el producto cruzado.
    right = [
        direction[1] * up[2] - direction[2] * up[1],
        direction[2] * up[0] - direction[0] * up[2],
        direction[0] * up[1] - direction[1] * up[0]
    ]
    return right

#Funcion graficadora de los objetos
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.1, 0.4, 1)
    glBegin(GL_QUADS)
    glVertex3d(-sky, 300, -sky)
    glVertex3d(-sky, 300, sky)
    glVertex3d(sky, 300, sky)
    glVertex3d(sky, 300, -sky)
    glEnd()
        
    for obj in Wall_Obj:
        obj.drawCube(textures, 0)
        
    for obj in End_Obj:
        obj.drawCube(textures, 5)
        
    for obj in Floor_Obj:
        obj.drawCube(textures, 2)
        
    for obj in Fake_Floor_Obj:
        obj.drawCube(textures, 3)
        
    for obj in Lava_Obj:
        obj.drawCube(textures, 4)
        
    num = 0
    for i in Enemy:
        [x4, y4, z4] = i
        if (EYE_X - x4) != 0:
            m = (EYE_Z - y4)/(EYE_X - x4)
        else:
            m = 0
        arcotangente_radianes = math.atan(m)
        arconte_g = math.degrees(arcotangente_radianes)
        displayobj(num, x4, y4, z4, arconte_g)
        num = num + 1
        
    for obj in bullet_obj:
        obj.drawCube(sphere)
        
#Iniciando la musica
pygame.mixer.music.play()
#Iniciando el programa
done = False
Init()
while not done:
    #PARTE 1: MOVIMIENTO
    #Guardar la ubicacion actual    
    Old_EYE_X = EYE_X
    Old_EYE_Z = EYE_Z
    #Ver teclas presionadas
    keys = pygame.key.get_pressed()
    
    #Amplificar velocidad
    if keys[pygame.K_LSHIFT] and fuel >= 1:
        oldDir[0] = dir[0]
        oldDir[2] = dir[2]
        dir[0] = dir[0] *4
        dir[2] = dir[2] *4
        fuel -= 40
    
    #Mover hacia adelante    
    if keys[pygame.K_w]:
            EYE_X = EYE_X + dir[0]
            EYE_Z = EYE_Z + dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
    
    #Mover hacia atras        
    if keys[pygame.K_s]:
            EYE_X = EYE_X - dir[0]
            EYE_Z = EYE_Z - dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
     
    #Calcular el vector derecho
    right = get_right_vector(dir, [UP_X, UP_Y, UP_Z])
    
    #Mover hacia la izquierda
    if keys[pygame.K_a]:
        EYE_X -= right[0]
        EYE_Z -= right[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
    
    #Mover hacia la derecha
    if keys[pygame.K_d]:
        EYE_X += right[0]
        EYE_Z += right[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        
    #Definir rango para ver si esta su hitbox pegando algo
    rango = 0
    if Old_EYE_X < EYE_X:
        rango = 10
    else:
        rango = -10    
    if Old_EYE_Z < EYE_Z:
        rangoZ = 10
    else:
        rangoZ = -10
    
    #Verificar choque con Wall (Pared)   
    for i in Wall:
        [x1, z1, x2, z2, jump] = i
            
        if x1 == x2 and ((Old_EYE_X + rango >= x1 and EYE_X + rango < x1) or (Old_EYE_X + rango < x1 and EYE_X + rango >= x1)) and EYE_Z > z1 and EYE_Z < z2:
            if (jump and EYE_Y >= 25):
                nada = EYE_X
            else:
                if keys[pygame.K_w]:
                    EYE_X = EYE_X - dir[0]
                    CENTER_X = EYE_X + dir[0]
                if keys[pygame.K_s]:
                    EYE_X = EYE_X + dir[0]
                    CENTER_X = EYE_X + dir[0]
                if keys[pygame.K_a]:
                    EYE_X += right[0]
                    CENTER_X = EYE_X + dir[0]
                if keys[pygame.K_d]:
                    EYE_X -= right[0]
                    CENTER_X = EYE_X + dir[0]
                
                
        if z1 == z2 and ((Old_EYE_Z + rangoZ >= z1 and EYE_Z + rangoZ < z1) or (Old_EYE_Z + rangoZ < z1 and EYE_Z + rangoZ >= z1)) and EYE_X > x1 and EYE_X < x2:
            if (jump and EYE_Y >= 25):
                nada = EYE_Z
            else:
                if keys[pygame.K_w]:
                    EYE_Z = EYE_Z - dir[2]
                    CENTER_Z = EYE_Z + dir[2]
                if keys[pygame.K_s]:
                    EYE_Z = EYE_Z + dir[2]
                    CENTER_Z = EYE_Z + dir[2]
                if keys[pygame.K_a]:
                    EYE_Z += right[2]
                    CENTER_Z = EYE_Z + dir[2]
                if keys[pygame.K_d]:
                    EYE_Z -= right[2]
                    CENTER_Z = EYE_Z + dir[2]
        
    #Regresar la velocidad al estado original
    if keys[pygame.K_LSHIFT]:        
        dir[0] = oldDir[0]
        dir[2] = oldDir[2]
    elif fuel < 2500: #En caso de no usarse recuperar energia
        fuel += 5
        
    n = 25-(fuel//100)
    fT = fuel_text[n:]   # Representar la energia gastada
    
    
             
    #PARTE 2: VISTA
    #Vista derecha
    if keys[pygame.K_RIGHT]:
            theta = -4.0
            rota_obs()
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
    
    #Vista izquierda        
    if keys[pygame.K_LEFT]:
            theta = 4.0
            rota_obs()
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
      
    #Vista con Mouse            
    #Obtiene la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #Mueve la cámara según la posición del mouse
    if mouse_x < MOUSE_BORDER:
        theta = 10.0
        rota_obs()
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]  
    elif mouse_x > screen_width - MOUSE_BORDER: 
        theta = -10.0
        rota_obs()
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]

    #PARTE 3: FISICAS
    #Gravedad
    ground = True
    #Deteccion de suelo
    for i in Floor:
        if ground:
            [x1, z1, x2, z2, la_X, la_Y] = i
            if (x1 <= EYE_X + 10) and (EYE_X - 10 <= la_X) and (z1 <= EYE_Z + 10) and (EYE_Z - 10 <= z2):
                Ground_level = la_Y + 5
                ground = False
            else:
                Ground_level = 5
                
    #Aplicando gravedad en el aire
    if EYE_Y > Ground_level:
        gravity = gravity - 9.81*0.01
    elif EYE_Y < Ground_level:
        if EYE_Y < 5:
            EYE_Y = 5
            CENTER_Y = 5
            gravity = 0
        else:
            if gravity == 0:
                suma = 1+1
                gravity = 0
            elif (abs(EYE_Y - Ground_level) <= 5) and gravity < 0:
                EYE_Y = Ground_level
                CENTER_Y = Ground_level
                gravity = 0
            else:
                gravity = gravity - 9.81*0.01    
    else:
        gravity = 0
        
    #Aplicar salto   
    if keys[pygame.K_SPACE] and gravity == 0:
        if (actLevel == 3):
            gravity = 3
        else:
            gravity = 4    
    
    #Siempre actualizar y a donde salta    
    EYE_Y = EYE_Y + gravity
    CENTER_Y = EYE_Y
    
    #Camara vista + gravedad de arriba y ahacia abajo
    if keys[pygame.K_DOWN]:
            CENTER_Y = EYE_Y - 0.5     
    if keys[pygame.K_UP]:
            CENTER_Y = EYE_Y + 0.5
    
    #PARTE 4: HITBOXES Y ENEMIGOS        
    #Lava
    for i in Lava:
        if EYE_Y == 5:
            [x1, z1, x2, z2, la_X] = i
            if (x1 <= EYE_X) and (EYE_X <= la_X) and (z1 <= EYE_Z) and (EYE_Z <= z2):
                dir = [1.0, 0.0, 0.0]
                EYE_X = -80
                EYE_Z = 50
                EYE_Y = 7 
                CENTER_X = EYE_X + 1
                CENTER_Z = EYE_Z
                CENTER_Y = EYE_Y
    
    #Proyectiles (Ball):            
    for obj in bullet_obj:
        [x1, y1, z1] = obj.doxxeo()
        if (abs(x1 - EYE_X) <= 5) and (abs(z1 - EYE_Z) <= 5) and (abs(EYE_Y - y1) <= 6):
            dir = [1.0, 0.0, 0.0]
            EYE_X = -80
            EYE_Z = 50
            EYE_Y = 7 
            CENTER_X = EYE_X + 1
            CENTER_Z = EYE_Z
            CENTER_Y = EYE_Y
            
    #PARTE 6: Otros
    #Actualizar la mirada
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    
    # Teletransporta el mouse al centro cara 3 ticks
    if timer == 3:
        timer = 0
        teleport_mouse_to_center()
    timer += 1

    # Terminar el juego  
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    
    # Creacion de las Balas
    # Todas las balas se eliminan el mismo tiempo que se crean otras
    time = time + 1
    if Shoottime <= time:
        bullet_obj.clear()
        for i in Enemy:
            [x4, y4, z4] = i
            if (EYE_X - x4) != 0:
                m = (EYE_Z - y4)/(EYE_X - x4)
            else:
                m = 0
            arcotangente_radianes = math.atan(m)
            arconte_g = math.degrees(arcotangente_radianes)
            if (EYE_X > x4):
                bullet_obj.append(Balls(x4, z4+5.5, y4, -arconte_g))
            else:
                bullet_obj.append(Balls(x4, z4+5.5, y4, -arconte_g + 180))
        time = 0
    
    #Mostrar todo         
    display()
    
    # Renderizar el texto
    text_surface = font.render(
        fT, True, (255, 200, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(10, 10)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # Renderizar el texto (Barra Estamina)
    text_surface2 = font.render(
        fuel_text, True, (0, 255, 255)) # 20
    text_data2 = pygame.image.tostring(text_surface2, "RGBA", True)
    glWindowPos2d(10, 10)
    glDrawPixels(text_surface2.get_width(), text_surface2.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data2)
    
    """
    # Renderizar el texto (Vida?)
    text_surface2 = font.render(
        "AAAAAAAAAAAAAAAAAAAA", True, (255, 0, 0)) # 20
    text_data2 = pygame.image.tostring(text_surface2, "RGBA", True)
    glWindowPos2d(10, 70)
    glDrawPixels(text_surface2.get_width(), text_surface2.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data2)
    """

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
#Fin :)
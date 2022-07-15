import pygame
import math

#Tamaño de la Pantalla
wScreen = 1200
hScreen = 500

#Info del Nivel
nivel=1
gravedad=9.8
power_act=0
forze_act=0

#Inicializa
win = pygame.display.set_mode((wScreen,hScreen))
pygame.display.set_caption('Projectile Motion')
pygame.font.init()

font_coordenadas = pygame.font.SysFont('Comic Sans MS', 23)
font_info = pygame.font.SysFont('Comic Sans MS', 20)

#Objeto Pelota
class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)


    #Recorrido de La Pelota
    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        
        angle = ang         #Angulo
        #Velocidad
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        #Movimiento
        distX = velx * time
        distY = (vely * time) + ((-gravedad * (time ** 2)) / 2)  #Gravedad

        newx = round(distX + startx)
        newy = round(starty - distY)
        trajectoryLaunch.append(newx)
        trajectoryLaunch.append(newy)
        return (newx, newy)

#Mostrar Posicion

#Iniciar
trajectoryLaunch=[]

def redrawWindow(shooted):

    win.fill((64,64,64))
    golfBall.draw(win)
    pygame.draw.line(win, (0,0,0),line[0], line[1])
    drawInformation()
    drawParabol()
    pygame.display.update()

def drawInformation():

    text_info=font_info.render('Nivel: '+str(nivel),False,(0,255,0))
    win.blit(text_info, (20,20))
    text_info=font_info.render('Gravedad: '+str(gravedad),False,(0,255,0))
    win.blit(text_info, (20,50))
    text_info=font_info.render('Angulo: '+str(angle_act),False,(0,255,0))
    win.blit(text_info, (20,80))
    text_info=font_info.render('Fuerza: '+str(power_act),False,(0,255,0))
    win.blit(text_info, (20,110))

    text_surface = font_coordenadas.render('X:'+str(line[0][0])+'  Y: '+str(line[0][1]), False, (0, 0, 0))
    win.blit(text_surface, (line[0][0],line[0][1]-50))

def drawParabol():
    for i in range(int(len(trajectoryLaunch)/4)):
        x1=trajectoryLaunch[(i*4)]
        y1=trajectoryLaunch[(i*4)+1]
        x2=trajectoryLaunch[(i*4)+2]
        y2=trajectoryLaunch[(i*4)+3]
        pygame.draw.line(win, (255,0,0),(x1,y1), (x2,y2),width=2)

#Encontrar El angulo
def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y

    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle
    return angle


#Inicializar Pelota, Posicion, Color
golfBall = ball(300,494,5,(255,255,255))

run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
while run:
    clock.tick(200)
    angle_act=findAngle(pygame.mouse.get_pos())
    line_act = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    power_act=math.sqrt((line_act[1][1]-line_act[0][1])**2 +(line_act[1][0]-line_act[0][1])**2)/5
    if shoot:
        if golfBall.y < 500 - golfBall.radius:
            trajectoryLaunch.append(golfBall.x)
            trajectoryLaunch.append(golfBall.y)
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]
            trajectoryLaunch.append(golfBall.x)
            trajectoryLaunch.append(golfBall.y)
        else:
            shoot = False
            time = 0
            golfBall.y = 494

    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    redrawWindow(shoot)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = golfBall.x
                y = golfBall.y
                pos =pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/5
                angle = findAngle(pos)

pygame.quit()
quit()
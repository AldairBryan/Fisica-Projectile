import pygame, math, random

path='Resources/'

#Tamaño de la Pantalla
wScreen = 1200
hScreen = 500

#Info del Nivel
nivel=3
if nivel==1:
    gravedad=9.8
    rangoGanar=300
    bg=pygame.image.load(path+"fondo1.jpg")
    maximaFuerza=93.1
    controlarFuerza=2.1
elif nivel==2:
    gravedad=5.4
    rangoGanar=200
    bg=pygame.image.load(path+"fondo2.jpg")
    maximaFuerza=69.2
    controlarFuerza=3
elif nivel==3:
    gravedad=24.3
    rangoGanar=100
    bg=pygame.image.load(path+"fondo3.jpg")
    maximaFuerza=147
    controlarFuerza=1.33

#Posicion donde se puede generar el lugar donde deba aterrizar para ganar
posicionGanar=random.randint(600,wScreen-rangoGanar)

#Inicializa
win = pygame.display.set_mode((wScreen,hScreen))
pygame.display.set_caption('Projectile Motion')
pygame.font.init()

#Fuentes Para los Textos
font_coordenadas = pygame.font.SysFont('Comic Sans MS', 23)
font_info = pygame.font.SysFont('Comic Sans MS', 20)

#Objeto Pelota
class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    #Pelota
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

        #Nuevas Posiciones
        newx = round(distX + startx)
        newy = round(starty - distY)
        return (newx, newy)

#Guarda los puntos del recorrdio
trajectoryLaunch=[]

#Iniciar
def redrawWindow(shooted):
    win.fill((64,64,64))
    win.blit(bg, (0, 0))
    golfBall.draw(win)
    if not shooted:
        pygame.draw.line(win, (255,255,255),line[0], line[1])     #Linea del mouse
    drawInformation()   #Mostrar Informacion del Nivel
    drawLineGame()      #Linea del Juego - Ganar/Perder
    drawParabol()       #Mostrar El movimiento Parabolico
    pygame.display.update()

def drawInformation():
    #Informacion del NIvel
    text_info=font_info.render('Nivel: '+str(nivel),False,(0,255,0))
    win.blit(text_info, (20,20))
    text_info=font_info.render('Gravedad: '+str(gravedad),False,(0,255,0))
    win.blit(text_info, (20,50))
    text_info=font_info.render('Angulo: '+str(round((angle_act)*(180/math.pi),3))+' °',False,(0,255,0))
    win.blit(text_info, (20,80))
    text_info=font_info.render('Fuerza: '+str(round(power_act,3)),False,(0,255,0))
    win.blit(text_info, (20,110))
    #Informacion de la posicion
    text_surface = font_coordenadas.render('X:'+str(line[0][0])+'  Y: '+str(line[0][1]), False, (255, 255, 255))
    win.blit(text_surface, (line[0][0],line[0][1]-50))

def showWinLose(estado):
    if estado=='win':
        bg=pygame.image.load(path+"winner.png")
    elif estado=='lose':
        bg=pygame.image.load(path+"loser.png")
    win.blit(bg, (440, 100))
    pygame.display.update()
    
#Linea donde se indica si gano o perdio
def drawLineGame():
    pygame.draw.line(win, (255,0,0), (0,494), (posicionGanar,494))
    pygame.draw.line(win, (0,255,0), (posicionGanar,494), (posicionGanar+rangoGanar,494))
    pygame.draw.line(win, (255,0,0), (posicionGanar+rangoGanar,494), (1200, 494))

#Muestra la Parabola
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

def ajustarLimitePoder(x,y,pos):
    powerTemp= (math.hypot(pos[0]-x,pos[1]-y))/controlarFuerza
    if powerTemp > maximaFuerza:
        powerTemp=maximaFuerza
    return powerTemp

#Inicializar Pelota, Posicion, Color
golfBall = ball(300,494,5,(255,255,255))

run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
status='playing'

def clearAll():
    trajectoryLaunch.clear()
    win.fill((64,64,64))

while run:
    clock.tick(200)     #Reloj

    #Informacion actual
    if status =='playing' and shoot==False:
        angle_act=findAngle(pygame.mouse.get_pos())
        power_act=ajustarLimitePoder(golfBall.x,golfBall.y,pygame.mouse.get_pos())

    #Cuando la pelota haya sido disparada y este en el recorrido
    if shoot:
        if golfBall.y < 500 - golfBall.radius:
            trajectoryLaunch.append(golfBall.x)     #Agregamos posicion actual
            trajectoryLaunch.append(golfBall.y)
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)    #Recorrido
            golfBall.x = po[0]
            golfBall.y = po[1]
            trajectoryLaunch.append(golfBall.x)     #Agregamos posicion nueva
            trajectoryLaunch.append(golfBall.y)
        else:       #Aterrizo
            shoot = False
            time = 0
            golfBall.y = 494
            status='landed'

    #Linea al mouse
    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    if status=='playing':
        redrawWindow(shoot)
    elif status=='win' or status=='lose':
        showWinLose(status)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #Lanza
        if event.type == pygame.MOUSEBUTTONDOWN:
            if status =='landed':
                if golfBall.x > posicionGanar and golfBall.x < posicionGanar+rangoGanar:
                    status='win'
                    posicionGanar=random.randint(750,1200-rangoGanar)
                    #Mostrar mensaje de Gano
                else:
                    status='lose'
                    #Mostrar mensaje de Perdio
            elif not shoot and status =='playing':
                x = golfBall.x
                y = golfBall.y
                pos =pygame.mouse.get_pos()
                shoot = True
                angle = findAngle(pos)
                power = ajustarLimitePoder(x,y,pos)

        if event.type == pygame.KEYDOWN and (status=='win' or status=='lose'):
            if event.key == pygame.K_r:
                status='playing'
                clearAll()
                golfBall = ball(300,494,5,(255,255,255))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

pygame.quit()
quit()
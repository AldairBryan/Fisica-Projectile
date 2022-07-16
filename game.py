import pygame, math, random
from menu import *
from ball import ball

path='Resources/'

class Game():
    def __init__(self):
        #---------#
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1200, 500  #Tamaño de la Pantalla
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        #self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        #---------#
        #Info del Nivel
        self.nivel=1
        if self.nivel==1:
            self.gravedad=9.8
            self.rangoGanar=300
            self.bg=pygame.image.load(path+"fondo1.jpg")
            self.maximaFuerza=93.1
            self.controlarFuerza=2.1
        elif self.nivel==2:
            self.gravedad=5.4
            self.rangoGanar=200
            self.bg=pygame.image.load(path+"fondo2.jpg")
            self.maximaFuerza=69.2
            self.controlarFuerza=3
        elif self.nivel==3:
            self.gravedad=24.3
            self.rangoGanar=100
            self.bg=pygame.image.load(path+"fondo3.jpg")
            self.maximaFuerza=147
            self.controlarFuerza=1.33
        #Posicion donde se puede generar el lugar donde deba aterrizar para ganar
        self.posicionGanar=random.randint(600,self.DISPLAY_W-self.rangoGanar)
        #Inicializa
        self.win = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        pygame.display.set_caption('Projectile Motion')
        pygame.font.init()
        #Fuentes Para los Textos
        self.font_coordenadas = pygame.font.SysFont('Comic Sans MS', 23)
        self.font_info = pygame.font.SysFont('Comic Sans MS', 20)
        #Guarda los puntos del recorrdio
        self.trajectoryLaunch=[]
        #Inicializar Pelota, Posicion, Color
        self.golfBall = ball(300,494,5,(255,255,255))
        self.run = True
        self.time = 0
        self.power = 0
        self.angle = 0
        self.shoot = False
        self.clock = pygame.time.Clock()
        self.status='playing'

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.run_game()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    #Iniciar
    def redrawWindow(self, shooted):
        self.win.fill((64,64,64))
        self.win.blit(self.bg, (0, 0))
        self.golfBall.draw(self.win)
        if not shooted:
            pygame.draw.line(self.win, (255,255,255),self.line[0], self.line[1])
        self.drawInformation()   #Mostrar Informacion del Nivel
        self.drawLineGame()      #Linea del Juego - Ganar/Perder
        self.drawParabol()       #Mostrar El movimiento Parabolico
        pygame.display.update()

    def drawInformation(self):
        #Informacion del NIvel
        text_info=self.font_info.render('Nivel: '+str(self.nivel),False,(0,255,0))
        self.win.blit(text_info, (20,20))
        text_info=self.font_info.render('Gravedad: '+str(self.gravedad)+'  m/s^2',False,(0,255,0))
        self.win.blit(text_info, (20,50))
        text_info=self.font_info.render('Angulo: '+str(round((self.angle_act)*(180/math.pi),3))+'  °',False,(0,255,0))
        self.win.blit(text_info, (20,80))
        text_info=self.font_info.render('Velocidad: '+str(round(self.power_act,3))+'  m/s',False,(0,255,0))
        self.win.blit(text_info, (20,110))
        text_info=self.font_info.render('Tiempo: '+str(round(self.time,3))+'  s',False,(0,255,0))
        self.win.blit(text_info, (20,140))
        #Posicion del Rango para Ganar
        text_surface = self.font_coordenadas.render(str(self.posicionGanar-300), False, (255, 255, 255))
        self.win.blit(text_surface, (self.posicionGanar-40,454))
        text_surface = self.font_coordenadas.render(str(self.posicionGanar+self.rangoGanar-300), False, (255, 255, 255))
        self.win.blit(text_surface, (self.posicionGanar+self.rangoGanar-50,454))
        #Informacion de la posicion
        if(self.golfBall.y>=494):
            self.text_surface = self.font_coordenadas.render('X:'+str(self.golfBall.x-300)+'  Y: '+str(0), False, (255, 255, 255))
            self.win.blit(self.text_surface, (self.line[0][0],self.line[0][1]-50))
        else:
            self.text_surface = self.font_coordenadas.render('X:'+str(self.golfBall.x-300)+'  Y: '+str((self.golfBall.y*-1)+494), False, (255, 255, 255))
            self.win.blit(self.text_surface, (self.line[0][0],self.line[0][1]-50))

    def showWinLose(self, estado):
        if estado=='win':
            bg=pygame.image.load(path + "winner.png")
        elif estado=='lose':
            bg=pygame.image.load(path + "loser.png")
        self.win.blit(bg, (440, 100))
        pygame.display.update()
        
    #Linea donde se indica si gano o perdio
    def drawLineGame(self):
        pygame.draw.line(self.win, (255,0,0), (0,494), (self.posicionGanar,494))
        pygame.draw.line(self.win, (0,255,0), (self.posicionGanar,494), (self.posicionGanar+self.rangoGanar,494))
        pygame.draw.line(self.win, (255,0,0), (self.posicionGanar+self.rangoGanar,494), (1200, 494))

    #Muestra la Parabola
    def drawParabol(self):
        for i in range(int(len(self.trajectoryLaunch)/4)):
            x1=self.trajectoryLaunch[(i*4)]
            y1=self.trajectoryLaunch[(i*4)+1]
            x2=self.trajectoryLaunch[(i*4)+2]
            y2=self.trajectoryLaunch[(i*4)+3]
            pygame.draw.line(self.win, (255,0,0),(x1,y1), (x2,y2),width=2)

    #Encontrar El angulo
    def findAngle(self, pos):
        sX = self.golfBall.x
        sY = self.golfBall.y

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

    def ajustarLimitePoder(self, x, y, pos):
        powerTemp= (math.hypot(pos[0]-x,pos[1]-y))/self.controlarFuerza
        if powerTemp > self.maximaFuerza:
            powerTemp = self.maximaFuerza
        return powerTemp

    def clearAll(self):
        self.trajectoryLaunch.clear()
        self.win.fill((64,64,64))

    def run_game(self):
        self.clock.tick(200)     #Reloj

        #Informacion actual
        if self.status =='playing' and self.shoot==False:
            self.angle_act=self.findAngle(pygame.mouse.get_pos())
            self.power_act=self.ajustarLimitePoder(self.golfBall.x,self.golfBall.y,pygame.mouse.get_pos())

        #Cuando la pelota haya sido disparada y este en el recorrido
        if self.shoot:
            if self.golfBall.y < 500 - self.golfBall.radius:
                self.trajectoryLaunch.append(self.golfBall.x)     #Agregamos posicion actual
                self.trajectoryLaunch.append(self.golfBall.y)
                self.time += 0.05
                self.po = ball.ballPath(self.x, self.y, self.power, self.angle, self.time, self.gravedad)    #Recorrido
                self.golfBall.x = self.po[0]
                self.golfBall.y = self.po[1]
                self.trajectoryLaunch.append(self.golfBall.x)     #Agregamos posicion nueva
                self.trajectoryLaunch.append(self.golfBall.y)
            else:       #Aterrizo
                self.shoot = False
                self.time = 0
                self.golfBall.y = 494
                self.status='landed'
                print(str(self.golfBall.x-300))

        #Linea al mouse
        self.line = [(self.golfBall.x, self.golfBall.y), pygame.mouse.get_pos()]
        if self.status=='playing':
            self.redrawWindow(self.shoot)
        elif self.status=='win' or self.status=='lose':
            self.showWinLose(self.status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            #Lanza
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.status =='landed':
                    if self.golfBall.x > self.posicionGanar and self.golfBall.x < self.posicionGanar+self.rangoGanar:
                        self.status='win'
                        self.posicionGanar=random.randint(750,1200-self.rangoGanar)
                        #Mostrar mensaje de Gano
                    else:
                        self.status='lose'
                        #Mostrar mensaje de Perdio
                elif not self.shoot and self.status =='playing':
                    self.x = self.golfBall.x
                    self.y = self.golfBall.y
                    self.pos = pygame.mouse.get_pos()
                    self.shoot = True
                    self.angle = self.findAngle(self.pos)
                    self.power = self.ajustarLimitePoder(self.x,self.y,self.pos)

            if event.type == pygame.KEYDOWN and (self.status=='win' or self.status=='lose'):
                if event.key == pygame.K_r:
                    self.status='playing'
                    self.clearAll()
                    self.golfBall = ball(300,494,5,(255,255,255))
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
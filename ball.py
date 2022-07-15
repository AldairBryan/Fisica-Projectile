import pygame, math
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
    def ballPath(startx, starty, power, ang, time, gravedad):
        
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
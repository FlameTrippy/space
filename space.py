import pygame as pg
import random 
import math


vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH,HEIGHT =1600,900        #Разрешение экрана
NUM_STARS = 5000
CENTER = vec2(WIDTH//2,HEIGHT//2)
COLORS = "red green blue orange purple cyan".split()
Z_DISTANCE = 100     #Начало движения звёзд
ALPHA = 120
Ch = False
class Star:             #Создаёт один воксель(звезду типа))0))
    def __init__(self,app):
        self.screen = app.screen    #поверхность отрисовки(что бы не запутаться)
        self.pos3d = self.get_pos3d()           #Позиция вокселя в 3д
        self.vel = random.uniform(0.05, 0.25)   #Случайная скорость звезды
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0,0)             #Позиция звезды на экране
        self.size = 10                          # Величина размера

    def get_pos3d(self,scale_pos = 35):                        #Рандомная точка на окружности
        angle = random.uniform(0, 2 * math.pi)  #Угол (случайный)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) *scale_pos      #расстояние от центра до случайной точки(звезды)
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x,y,Z_DISTANCE)

    def update(self):           #обновление состояния(двигаем звезду)
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z<1 else self.pos3d #Когда звезда близко то заного даём ей рандомное состояние

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER     #Расчёт координат звезды на экране
        self.size = (Z_DISTANCE - self.pos3d.z)/(0.2*self.pos3d.z)                                         #пропорциональный размер
        self.pos3d.xy =self.pos3d.xy.rotate(1)    #Управление и угол поворота
        mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        self.screen_pos += mouse_pos
    def draw(self):             #Метод отрисовки
            pg.draw.ellipse(self.screen, self.color, (*self.screen_pos,self.size,self.size ))


class Starfield:            #Здесь создание и управление звёздами
    def __init__(self,app):
        self.stars = [Star(app) for i in range(NUM_STARS)]
    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z,reverse = True)                    #Сортировка звёзд до момента их отрисовки                                                        
        [star.draw() for star in self.stars]

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)  #Экран(поверхность отрисовки)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.clock = pg.time.Clock()            #Кадры в секунду
        self.starfield = Starfield(self)

    def run(self):
        while True:                             
            #self.screen.fill('black')
            self.screen.blit(self.alpha_surface,(0,0))
            self.starfield.run()

            pg.display.flip()   #Обновление экрана(отоброжение отрисовки)
            [exit() for i in pg.event.get() if i.type == pg.QUIT]       
            self.clock.tick(60)

if __name__=='__main__' :
    app = App()
    app.run()
import pygame
import math
import random
"""

DESCRIPTION : HERE THE ENVIRONMENT IS REDEFINED TO USE IT FOR THE PURPOSE OF TRAINING

"""
class environment :
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    #################################################
    x_position = 100
    y_position = 100
    ball_x_position = 250
    ball_y_position = 250
    t1 = 10
    v = 10
    a = 0.5
    t = t1 + v / a
    pi = math.pi
    loop = False
    face_angle = 0
    rotate_angle = 0
    last_x_position = 0
    last_y_position = 0
    last_ball_x_position = 250
    last_ball_y_position = 250
    v_angle = 0
    raw_x_position = 100.
    raw_y_position = 100.
    raw_ball_x_position = 250
    raw_ball_y_position = 250
    ball_angle = 0
    ball_velocity = 0
    constant = 2 ### CASE SENSITIVE
    ball_acc = 0.25
    add_velocity = 0
    norm_angle = 0
    left_distance = 65.2703644666
    right_distance = 65.2703644666
    front_distance = 50
    dist_ball = -1
    angle_ball = -1
    inpt = 0
    x_pos = 0
    y_pos = 0
    time = 1
    mark_velocity = 0
    s = 0
    ball_distance = 0
    angle_between = 0
    steady_retract_angle = 0
    norm_ball_v = 0
    ball_crossed_distance = 0
    new_angle = 0
    c = 0
    new_y = 0
    new_x = 0
    angle_between_ball = 0
    distance_ball = 0
    control = False
    reward = 0
    clock = pygame.time.Clock()


    def __init__(self):
        pygame.init()
        self.img = pygame.image.load("mark2.png")
        self.img_1 = pygame.image.load("background.png")
        self.img_2 = pygame.image.load("ball.png")
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Mark playing")
        self.render()

    def normalize(self , x , y):
        if x > 408 or x < 92 or y > 408 or y < 92:
            if x > 408:
                x = 408 - (x - 408)
            if x < 92:
                x = 92 + (92 - x)
            if y > 408:
                y = 408 - (y - 408)
            if y < 92:
                y = 92 + (92 - y)
        return (x, y)

    def normalize2(self , x , y, b_angle):
        if x > 428 or x < 72 or y > 428 or y < 72:
            if x > 428:
                x = 428 - (x - 428)
                b_angle = - b_angle
            if x < 72:
                x = 72 + (72 - x)
                b_angle = - b_angle
            if y > 428:
                y = 428 - (y - 428)
                b_angle = - (b_angle + 180)
            if y < 72:
                y = 72 + (72 - y)
                b_angle = - (b_angle + 180)
        b_angle = b_angle % 360
        return (x, y, b_angle)

    def fps(self):
        self.clock.tick(30)


    def action(self , act):
        self.reward = 0
        self.inpt = act

    def state(self):
        return([self.left_distance , self.front_distance , self.right_distance , self.dist_ball , self.angle_ball] )


    def render(self):
        image = pygame.transform.rotate(self.img , self.face_angle)
        rect = image.get_rect()
        rect.center =(self.x_position , self.y_position)
        ball_rect = self.img_2.get_rect()
        ball_rect.center = (self.ball_x_position , self.ball_y_position)
        self.gameDisplay.fill(self.white)
        self.gameDisplay.blit(self.img_1 , (50 , 50))
        self.gameDisplay.blit(self.img_2 , ball_rect)
        self.gameDisplay.blit(image , rect)
        pygame.display.update()

    def core_loop(self):
        pygame.event.get()
        if self.inpt == 0 and not self.loop :
            self.rotate_angle = 10
        if self.inpt == 2 and not self.loop :
            self.rotate_angle = -10
        if self.inpt == 1 and not self.loop :
            self.loop = True
            self.x_pos = self.x_position
            self.y_pos = self.y_position
            self.time = 1

        if self.loop :
            if self.time <= self.t1 :
                self.s = self.v * self.time
                self.mark_velocity = self.v
            if self.time > self.t1 and self.time <= self.t :
                self.s = self.v * self.t1 + self.v * (self.time - self.t1) - self.a * ((self.time - self.t1) ** 2) * 0.5
                self.mark_velocity = self.v - self.a * (self.time - self.t1)

            self.raw_x_position = self.x_pos - self.s * math.sin(self.pi / 180 * self.face_angle)
            self.raw_y_position = self.y_pos - self.s * math.cos(self.pi / 180 * self.face_angle)
            self.time = self.time + 1
            if self.time == self.t :
                self.loop = False
                self.control = False
        self.raw_x_position , self.raw_y_position = self.normalize(self.raw_x_position , self.raw_y_position)
        self.x_position = round(self.raw_x_position)
        self.y_position = round(self.raw_y_position)
        self.v_angle = - (math.atan2((self.raw_y_position - self.last_y_position) , (self.raw_x_position - self.last_x_position)) * 180 / self.pi + 90)
        self.ball_distance = math.sqrt((self.last_ball_y_position - self.raw_y_position) ** 2 + (self.last_ball_x_position - self.raw_x_position) ** 2)

        if self.ball_distance < 64 and self.angle_ball != -1 :
            self.raw_ball_x_position = random.randint(73 , 427)
            self.ball_x_position = round(self.raw_ball_x_position)
            self.last_ball_x_position = self.ball_x_position
            self.raw_ball_y_position = random.randint(73 , 427)
            self.ball_y_position = round(self.raw_ball_y_position)
            self.last_ball_y_position = self.ball_y_position
            self.ball_angle = 0
            self.ball_velocity = 0
            self.reward = 1
            return

        if self.ball_distance < 64 :
            self.angle_between = - (math.atan2((self.last_ball_y_position - self.raw_y_position) , (self.last_ball_x_position - self.raw_x_position))* 180 / self.pi + 90)
            if self.ball_velocity > 0 :
                self.steady_retract_angle = 2 * self.angle_between - (180 + self.ball_angle)
            else :
                self.steady_retract_angle = self.angle_between
            if math.cos((self.v_angle - self.angle_between) * self.pi / 180) > 0 :
                self.add_velocity = self.constant * self.mark_velocity * math.cos((self.v_angle - self.angle_between) * self.pi / 180)
            else :
                self.add_velocity = 0
            self.norm_ball_v = math.sqrt(self.add_velocity ** 2 + self.ball_velocity ** 2 + 2 * self.add_velocity * self.ball_velocity * math.cos(self.pi / 180 * (self.steady_retract_angle - self.angle_between)))
            self.norm_angle = math.atan2((self.add_velocity * math.sin(self.pi / 180 * self.angle_between) + self.ball_velocity * math.sin(self.pi / 180 * self.steady_retract_angle)) , ((self.add_velocity * math.cos(self.pi / 180 * self.angle_between) + self.ball_velocity * math.cos(self.pi / 180 * self.steady_retract_angle)))) * 180 / self.pi
            self.ball_velocity = self.norm_ball_v
            self.ball_angle = self.norm_angle
        self.ball_crossed_distance = self.ball_velocity
        self.raw_ball_x_position = self.last_ball_x_position - self.ball_crossed_distance * math.sin(self.pi / 180 * self.ball_angle)
        self.raw_ball_y_position = self.last_ball_y_position - self.ball_crossed_distance * math.cos(self.pi / 180 * self.ball_angle)
        self.raw_ball_x_position , self.raw_ball_y_position , self.ball_angle = self.normalize2(self.raw_ball_x_position , self.raw_ball_y_position , self.ball_angle)
        self.ball_y_position = round(self.raw_ball_y_position)
        self.ball_x_position = round(self.raw_ball_x_position)
        if self.ball_velocity > 0 :
            self.ball_velocity = self.ball_velocity - self.ball_acc
        if self.ball_velocity <= 0 :
            self.ball_velocity = 0
            self.ball_angle = 0

        self.face_angle = ((self.face_angle + self.rotate_angle) + 360) % 360
    ##############          calculation for left distance
        if self.face_angle > 5 and self.face_angle <= 95 :
            self.new_angle = 270 - (self.face_angle + 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y <= 450 and self.new_y >= 50 :
                self.left_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.left_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.left_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 95 and self.face_angle <= 185 :
            self.new_angle = 270 - (self.face_angle + 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x <= 450 and self.new_x >= 50:
                self.left_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.left_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_x < 50 :
                new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.left_distance = math.sqrt((self.raw_y_position - new_y) ** 2 + (self.raw_x_position - 50) ** 2)

        elif self.face_angle > 185 and self.face_angle <= 275 :
            self.new_angle = 270 - (self.face_angle + 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y >= 50 and self.new_y <= 450 :
                self.left_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.left_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif  self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.left_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 275 or self.face_angle <= 5 :
            self.new_angle = 270 - (self.face_angle + 40)
            self.c = self.raw_y_position - math.tan(self.new_angle * self.pi / 180) * self.raw_x_position
            self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x >= 50 and self.new_x <= 450 :
                self.left_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x < 50 :
                self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.left_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.left_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)

    ################ calculation of right distance
        if self.face_angle > 85 and self.face_angle <= 175 :
            self.new_angle = 270 - (self.face_angle - 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y >= 50 and self.new_y <= 450:
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.right_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.right_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 175 and self.face_angle <= 265 :
            self.new_angle = 270 - (self.face_angle - 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x >= 50 and self.new_x <= 450 :
                self.right_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x < 50:
                self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
        elif self.face_angle > 265 and self.face_angle <= 355 :
            self.new_angle = 270 - (self.face_angle - 40)
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y <= 450 and self.new_y >= 50 :
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.right_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.right_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 355 or self.face_angle <= 85 :
            self.new_angle = 270 - (self.face_angle - 40)
            self.c = self.raw_y_position - math.tan(self.new_angle * self.pi / 180) * self.raw_x_position
            self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x <= 450 and self.new_x >= 50 :
                self.right_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_x < 50 :
                self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.right_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)

    ########################       calculation of front distance

        if self.face_angle > 45 and self.face_angle <= 135 :
            self.new_angle = 270 - self.face_angle
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y <= 450 and self.new_y >= 50 :
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.front_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.front_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 135 and self.face_angle <= 225 :
            self.new_angle = 270 - self.face_angle
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x <= 450 and self.new_x >= 50:
                self.front_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_x < 50 :
                self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)

        elif self.face_angle > 225 and self.face_angle <= 315 :
            self.new_angle = 270 - self.face_angle
            self.c = self.raw_y_position - self.raw_x_position * math.tan(self.new_angle * self.pi / 180)
            self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
            if self.new_y >= 50 and self.new_y <= 450 :
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)
            elif self.new_y < 50 :
                self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.front_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif  self.new_y > 450 :
                self.new_x = (450 - self.c) / math.tan(self.new_angle * self.pi / 180)
                self.front_distance = math.sqrt((self.raw_y_position - 450) ** 2 + (self.raw_x_position - self.new_x) ** 2)
        elif self.face_angle > 315 or self.face_angle <= 45 :
            self.new_angle = 270 - self.face_angle
            self.c = self.raw_y_position - math.tan(self.new_angle * self.pi / 180) * self.raw_x_position
            self.new_x = (50 - self.c) / math.tan(self.new_angle * self.pi / 180)
            if self.new_x >= 50 and self.new_x <= 450 :
                self.front_distance = math.sqrt((self.raw_y_position - 50) ** 2 + (self.raw_x_position - self.new_x) ** 2)
            elif self.new_x < 50 :
                self.new_y = 50 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 50) ** 2)
            elif self.new_x > 450 :
                self.new_y = 450 * math.tan(self.new_angle * self.pi / 180) + self.c
                self.front_distance = math.sqrt((self.raw_y_position - self.new_y) ** 2 + (self.raw_x_position - 450) ** 2)


        self.angle_between_ball = round( - (math.atan2((self.raw_ball_y_position - self.raw_y_position) , (self.raw_ball_x_position - self.raw_x_position))* 180 / self.pi + 90) + 360 ) % 360
        self.distance_ball = math.sqrt((self.raw_y_position - self.raw_ball_y_position) ** 2 + (self.raw_x_position - self.raw_ball_x_position) ** 2)
        if self.angle_between_ball >= self.face_angle - 40 and self.angle_between_ball <= self.face_angle + 40 :
            self.dist_ball = self.distance_ball
            self.angle_ball = self.angle_between_ball - (self.face_angle - 40)
        else :
            self.dist_ball = -1
            self.angle_ball = -1


        self.rotate_angle = 0
        self.last_x_position = self.raw_x_position
        self.last_y_position = self.raw_y_position
        self.last_ball_x_position = self.raw_ball_x_position
        self.last_ball_y_position = self.raw_ball_y_position
        if not self.loop :
            self.control = False
        return






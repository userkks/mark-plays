import pygame
import math
"""

DESCRIPTION : IN THIS ENVIRONMENT WHENEVER THE ROBOT HITS THE BALL, THE BALL GETS DEFLECTED
RUNNING THIS SCRIPT THE GAME CAN BE PLAYED USING ARROW KEYS FROM KEYBOARD

"""
def normalize(x , y) :
    if x > 408 or x < 92 or y > 408 or y < 92 :
        if x > 408 :
            x = 408 - (x - 408)
        if x < 92 :
            x = 92 + (92 - x)
        if y > 408 :
            y = 408 - (y - 408)
        if y < 92 :
            y = 92 + (92 - y)
    return(x , y)

def normalize2(x , y , b_angle) :
    if x > 428 or x < 72 or y > 428 or y < 72 :
        if x > 428 :
            x = 428 - ( x - 428)
            b_angle = - b_angle
        if x < 72 :
            x = 72 + (72 - x)
            b_angle = - b_angle
        if y > 428 :
            y = 428 - (y - 428)
            b_angle = - (b_angle + 180)
        if y < 72 :
            y = 72 + (72 - y)
            b_angle = - (b_angle + 180)
    b_angle = b_angle % 360
    return(x , y , b_angle)

pygame.init()
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
gameDisplay = pygame.display.set_mode((500 , 500))
pygame.display.set_caption("Slither")
pygame.display.update()

gameExit = False
img = pygame.image.load("mark2.png")
img_1 = pygame.image.load("background.png")
img_2 = pygame.image.load("ball.png")

clock = pygame.time.Clock()
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
raw_x_position = 100
raw_y_position = 100
raw_ball_x_position = 250
raw_ball_y_position = 250
ball_angle = 0
ball_velocity = 0
constant = 2 ### CASE SENSITIVE
ball_acc = 0.25
add_velocity = 0
norm_angle = 0
left_distance = 0
right_distance = 0
front_distance = 0

while not gameExit :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True
        if event.type == pygame.KEYDOWN and not loop :
            if event.key == pygame.K_LEFT:
                rotate_angle = 10
            if event.key == pygame.K_RIGHT :
                rotate_angle = -10
            if event.key == pygame.K_UP :
                loop = True
                x_pos = x_position
                y_pos = y_position
                time = 1

    if loop :
        if time <= t1 :
            s = v * time
            mark_velocity = v
        if time > t1 and time <= t :
            s = v * t1 + v * (time - t1) - a * ((time - t1) ** 2) * 0.5
            mark_velocity = v - a * (time - t1)

        raw_x_position = x_pos - s * math.sin(pi / 180 * face_angle)
        raw_y_position = y_pos - s * math.cos(pi / 180 * face_angle)
        time = time + 1
        if time == t :
            loop = False
    raw_x_position , raw_y_position = normalize(raw_x_position , raw_y_position)
    x_position = round(raw_x_position)
    y_position = round(raw_y_position)
    v_angle = - (math.atan2((raw_y_position - last_y_position) , (raw_x_position - last_x_position)) * 180 / pi + 90)
    ball_distance = math.sqrt((last_ball_y_position - raw_y_position) ** 2 + (last_ball_x_position - raw_x_position) ** 2)
    if ball_distance < 64 :
        angle_between = - (math.atan2((last_ball_y_position - raw_y_position) , (last_ball_x_position - raw_x_position))* 180 / pi + 90)
        if ball_velocity > 0 :
            steady_retract_angle = 2 * angle_between - (180 + ball_angle)
        else :
            steady_retract_angle = angle_between
        if math.cos((v_angle - angle_between) * pi / 180) > 0 :
            add_velocity = constant * mark_velocity * math.cos((v_angle - angle_between) * pi / 180)
        else :
            add_velocity = 0
        norm_ball_v = math.sqrt(add_velocity ** 2 + ball_velocity ** 2 + 2 * add_velocity * ball_velocity * math.cos(pi / 180 * (steady_retract_angle - angle_between)))
        norm_angle = math.atan2((add_velocity * math.sin(pi / 180 * angle_between) + ball_velocity * math.sin(pi / 180 * steady_retract_angle)) , ((add_velocity * math.cos(pi / 180 * angle_between) + ball_velocity * math.cos(pi / 180 * steady_retract_angle)))) * 180 / pi
        ball_velocity = norm_ball_v
        ball_angle = norm_angle
    ball_crossed_distance = ball_velocity
    raw_ball_x_position = last_ball_x_position - ball_crossed_distance * math.sin(pi / 180 * ball_angle)
    raw_ball_y_position = last_ball_y_position - ball_crossed_distance * math.cos(pi / 180 * ball_angle)
    raw_ball_x_position , raw_ball_y_position , ball_angle = normalize2(raw_ball_x_position , raw_ball_y_position , ball_angle)
    ball_y_position = round(raw_ball_y_position)
    ball_x_position = round(raw_ball_x_position)
    if ball_velocity > 0 :
        ball_velocity = ball_velocity - ball_acc
    if ball_velocity <= 0 :
        ball_velocity = 0
        ball_angle = 0

    face_angle = ((face_angle + rotate_angle) + 360) % 360
##############          calculation for left distance
    if face_angle > 30 and face_angle <= 120 :
        new_angle = 270 - (face_angle + 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 50 * math.tan(new_angle * pi / 180) + c
        if new_y <= 450 and new_y >= 50 :
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            left_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            left_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 120 and face_angle <= 210 :
        new_angle = 270 - (face_angle + 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_x = (450 - c) / math.tan(new_angle * pi / 180)
        if new_x <= 450 and new_x >= 50:
            left_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_x < 50 :
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)

    elif face_angle > 210 and face_angle <= 300 :
        new_angle = 270 - (face_angle + 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 450 * math.tan(new_angle * pi / 180) + c
        if new_y >= 50 and new_y <= 450 :
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            left_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif  new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            left_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 300 or face_angle <= 30 :
        new_angle = 270 - (face_angle + 15)
        c = raw_y_position - math.tan(new_angle * pi / 180) * raw_x_position
        new_x = (50 - c) / math.tan(new_angle * pi / 180)
        if new_x >= 50 and new_x <= 450 :
            left_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x < 50 :
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            left_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)

################ calculation of right distance
    if face_angle > 60 and face_angle <= 150 :
        new_angle = 270 - (face_angle - 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 50 * math.tan(new_angle * pi / 180) + c
        if new_y >= 50 and new_y <= 450:
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            right_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            right_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 150 and face_angle <= 240 :
        new_angle = 270 - (face_angle - 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_x = (450 - c) / math.tan(new_angle * pi / 180)
        if new_x >= 50 and new_x <= 450 :
            right_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x < 50:
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
    elif face_angle > 240 and face_angle <= 330 :
        new_angle = 270 - (face_angle - 15)
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 450 * math.tan(new_angle * pi / 180) + c
        if new_y <= 450 and new_y >= 50 :
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            right_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            right_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 330 or face_angle <= 60 :
        new_angle = 270 - (face_angle - 15)
        c = raw_y_position - math.tan(new_angle * pi / 180) * raw_x_position
        new_x = (50 - c) / math.tan(new_angle * pi / 180)
        if new_x <= 450 and new_x >= 50 :
            right_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_x < 50 :
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            right_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)

########################       calculation of front distance

    if face_angle > 45 and face_angle <= 135 :
        new_angle = 270 - face_angle
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 50 * math.tan(new_angle * pi / 180) + c
        if new_y <= 450 and new_y >= 50 :
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            front_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            front_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 135 and face_angle <= 225 :
        new_angle = 270 - face_angle
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_x = (450 - c) / math.tan(new_angle * pi / 180)
        if new_x <= 450 and new_x >= 50:
            front_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_x < 50 :
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)

    elif face_angle > 225 and face_angle <= 315 :
        new_angle = 270 - face_angle
        c = raw_y_position - raw_x_position * math.tan(new_angle * pi / 180)
        new_y = 450 * math.tan(new_angle * pi / 180) + c
        if new_y >= 50 and new_y <= 450 :
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)
        elif new_y < 50 :
            new_x = (50 - c) / math.tan(new_angle * pi / 180)
            front_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif  new_y > 450 :
            new_x = (450 - c) / math.tan(new_angle * pi / 180)
            front_distance = math.sqrt((raw_y_position - 450) ** 2 + (raw_x_position - new_x) ** 2)
    elif face_angle > 315 or face_angle <= 45 :
        new_angle = 270 - face_angle
        c = raw_y_position - math.tan(new_angle * pi / 180) * raw_x_position
        new_x = (50 - c) / math.tan(new_angle * pi / 180)
        if new_x >= 50 and new_x <= 450 :
            front_distance = math.sqrt((raw_y_position - 50) ** 2 + (raw_x_position - new_x) ** 2)
        elif new_x < 50 :
            new_y = 50 * math.tan(new_angle * pi / 180) + c
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 50) ** 2)
        elif new_x > 450 :
            new_y = 450 * math.tan(new_angle * pi / 180) + c
            front_distance = math.sqrt((raw_y_position - new_y) ** 2 + (raw_x_position - 450) ** 2)




    #print(front_distance)
    image = pygame.transform.rotate(img , face_angle)
    rect = image.get_rect()
    rect.center =(x_position , y_position)
    ball_rect = img_2.get_rect()
    ball_rect.center = (ball_x_position , ball_y_position)

    gameDisplay.blit(img_1 , (50 , 50))
    gameDisplay.blit(img_2 , ball_rect)
    gameDisplay.blit(image , rect)
    pygame.display.update()
    gameDisplay.fill(white)
    rotate_angle = 0
    last_x_position = raw_x_position
    last_y_position = raw_y_position
    last_ball_x_position = raw_ball_x_position
    last_ball_y_position = raw_ball_y_position
    clock.tick(30)

pygame.quit()
quit()

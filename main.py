import os.path
import pygame
from pygame.locals import *
from threading import Thread
import serial
import serial.tools.list_ports
import random

supportedBoardsModel = ("Arduino Uno", "Arduino Nano", "Silicon Labs CP210x")


def start_connection():
    global links, boardConnected, MCU
    ports = list(serial.tools.list_ports.comports())
    attached = 0
    port = None
    for p in ports:
        if any(one in p.description for one in supportedBoardsModel):
            attached += 1
            port = p.description
    if attached == 1:
        for o in supportedBoardsModel:
            if o in port:
                com = port.split("(")[-1][:-1]
                MCU = serial.Serial(port=com, baudrate=9600)
                MCU.close()
                MCU.open()
                boardConnected = True
                return "Connected"
    elif attached > 1:
        return "Attach one MCU only!"
    else:
        return "No MCU board attached!"


start_connection()

# main attributes definition
cups_levels = ['1.png', '2.png', '3.png']
general_value = 0
round = 0
cup_number = 0
reach = 0
running = True
isReady = True
rest = False
stillPressed = False
grabbed = False
half_cup = False
full_cup = False
bypass = False
next_flag = False
size = width, height = (700, 700)
pygame.init()
pygame.mixer.init()
bg_sound = pygame.mixer.Sound('bg_music.mp3')
bg_sound.set_volume(min(1.0, bg_sound.get_volume() / 20))
squeeze_sound = pygame.mixer.Sound('squezee.mp3')
nice_sound = pygame.mixer.Sound('احسنت.mp3')
press_sound = pygame.mixer.Sound('اضغط.mp3')
continue_sound = pygame.mixer.Sound('اكمل.mp3')
press_again_sound = pygame.mixer.Sound('قم بالضغط مرة اخري.mp3')
more_sound = pygame.mixer.Sound('اكثر.mp3')
try_again_sound = pygame.mixer.Sound('حاول تانيا.mp3')
for s in [press_sound, continue_sound, press_again_sound, more_sound, try_again_sound]:
    s.set_volume(min(1.0, s.get_volume() / 3))

# set window size
screen = pygame.display.set_mode(size)

# set game window name
if os.path.exists('gn.txt'):
    pygame.display.set_caption(open('gn.txt', 'r').read())
else:
    open('gn.txt', 'w').write('grip strength game')

# set game window icon
icon = pygame.image.load('orange.png')
pygame.display.set_icon(icon)

# background image init
background = pygame.image.load('bg.jpg')
background_loc = background.get_rect()
background_loc.center = 350, 300

# main object init (Orange)
main_object = pygame.image.load('orange.png')
main_object_loc = main_object.get_rect()
main_object_loc.center = width - 170, height / 2
res_main_object = pygame.transform.scale(main_object, (300, 200))

# cup image init
cup_loc = main_object.get_rect()
cup_loc.center = width - 170, height - 150
res_cup = pygame.transform.scale(pygame.image.load(cups_levels[0]), (300, 360))

# table image
table = pygame.image.load('table.png')
table_loc = table.get_rect()
table_loc.center = width / 18, height - 150
res_table = pygame.transform.scale(table, (1200, 400))

# rounds counter init
font = pygame.font.Font(None, 60)
text_surface = font.render(f"      {round}", True, (255, 255, 255))
text_surface_loc = text_surface.get_rect()
text_surface_loc.center = 5, 40

# round counter image
round_image = pygame.image.load('rounds.png')
round_image_loc = round_image.get_rect()
round_image_loc.center = 250, 100
res_round_image = pygame.transform.scale(round_image, (150, 80))

# cups counter init
cups_text_surface = pygame.font.Font(None, 60).render(f"     {cup_number}", True, (255, 255, 255))
cups_text_surface_loc = cups_text_surface.get_rect()
cups_text_surface_loc.center = 500, 40

# cups counter image
cups_image = pygame.image.load('cups.png')
cups_image_loc = cups_image.get_rect()
cups_image_loc.center = 740, 100
res_cups_image = pygame.transform.scale(cups_image, (150, 80))

# controller navigate
controller_nav = pygame.font.Font(None, 35).render(f"Controller connecting..", True, (255, 140, 0))
controller_nav_loc = controller_nav.get_rect()
controller_nav_loc.center = width / 4 - 10, 680

# finish a cup
finish_cup = pygame.image.load('check.png')
finish_cup_loc = finish_cup.get_rect()
finish_cup_loc.center = width / 2 + 50, height - 300
res_finish_cup = pygame.transform.scale(finish_cup, (400, 400))

# break init (Rest)
rest_text = pygame.font.Font(None, 150).render(f"Take a rest.", True, (0, 0, 255))
rest_text_loc = rest_text.get_rect()
rest_text_loc.center = 350, 350

# endgame init (Win)
end_text = pygame.font.Font(None, 150).render("Good job", True, (0, 255, 0))
end_text_loc = end_text.get_rect()
end_text_loc.center = 350, 350


# update all objects on screen
def update_all_objects():
    global rest, next_flag
    if not rest and not next_flag:
        screen.blit(background, background_loc)
        screen.blit(res_main_object, main_object_loc)
        screen.blit(res_table, table_loc)
        screen.blit(res_cups_image, cups_image_loc)
        screen.blit(res_cup, cup_loc)
        screen.blit(text_surface, text_surface_loc)
        screen.blit(res_round_image, round_image_loc)
        screen.blit(cups_text_surface, cups_text_surface_loc)
        screen.blit(controller_nav, controller_nav_loc)
        pygame.display.update()


# move full cup animation and get new empty cup
def next_cup():
    global cup_loc, main_object_loc, res_cup, cup, isReady, next_flag, nice_sound, continue_sound, press_sound
    isReady = False
    next_flag = True
    press_sound.stop()
    continue_sound.stop()
    screen.blit(res_finish_cup, finish_cup_loc)
    pygame.display.update()
    nice_sound.play()
    pygame.time.delay(3000)
    next_flag = False
    while cup_loc[0] < width + 100 and main_object_loc[0] < width + 100:
        cup_loc = cup_loc.move(100, 0)
        main_object_loc = main_object_loc.move(100, 0)
        pygame.display.update()
        pygame.time.delay(50)
    cup = pygame.image.load(cups_levels[0])
    res_cup = pygame.transform.scale(cup, (300, 360))
    cup_loc.center = 0, height - 150
    main_object_loc.center = 0, height / 2
    orange()
    while cup_loc.center <= (width - 170, height - 150):
        cup_loc = cup_loc.move(50, 0)
        main_object_loc = main_object_loc.move(50, 0)
        pygame.display.update()
        pygame.time.delay(50)
    isReady = True


# view orange on screen
def orange():
    global main_object, res_main_object
    main_object = pygame.image.load('orange.png')
    res_main_object = pygame.transform.scale(main_object, (300, 200))


# view squeezed orange on screen
def squezeed_orange():
    global main_object, res_main_object
    main_object = pygame.image.load('squezeed.png')
    res_main_object = pygame.transform.scale(main_object, (320, 600))


# view ended orange on screen
def ended_orange():
    global main_object, res_main_object
    main_object = pygame.image.load('ended_orange.png')
    res_main_object = pygame.transform.scale(main_object, (320, 600))


# take rest function
def take_rest():
    global isReady, rest_text, rest_text_loc, rest
    isReady = False
    rest = True
    screen.blit(rest_text, rest_text_loc)
    pygame.display.update()
    pygame.time.delay(1000 * 60)
    isReady = True
    rest = False


# check live sensor value
def active_press():
    global stillPressed, MCU, general_value, controller_nav
    while 1:
        pygame.time.delay(200)
        try:
            general_value = int(MCU.read().decode().strip())
            if str(general_value).isnumeric():
                controller_nav = pygame.font.Font(None, 36).render(f"Controller connected", True, (00, 255, 0))
        except:
            controller_nav = pygame.font.Font(None, 36).render(f"Controller offline!", True, (255, 0, 0))


Thread(target=active_press, daemon=True).start()


# check if still pressed
def still_pressed():
    global stillPressed, general_value
    while 1:
        pygame.time.delay(100)
        if general_value >= 1:
            stillPressed = True
        else:
            stillPressed = False


Thread(target=still_pressed, daemon=True).start()


# 3 secs holder
def holder():
    global bypass, press_sound, continue_sound, press_sound, more_sound, try_again_sound, rest, say
    if reach == 0:
        sw = 80
    else:
        sw = 120
    for x in range(sw):
        pygame.time.delay(50)
        if not stillPressed:
            bypass = False
            return
    bypass = True
    return


def guid_sound():
    global press_sound, press_again_sound, reach, general_value
    say_of_cup = 0
    tries = 4

    while 1:
        if cup_number == say_of_cup:
            for i in range(tries):
                if isReady and not rest:
                    while pygame.mixer.Channel(0).get_busy():
                        pygame.time.delay(3000)
                    if reach == 0 and tries > 2 and general_value != 1:
                        tries -= 1
                        press_sound.play()
                    elif reach == 1 and general_value != 2:
                        tries -= 1
                        press_again_sound.play()

        if reach == 2:
            tries = 4
            say_of_cup += 1

        if cup_number == 5:
            say_of_cup = 0

        pygame.time.delay(200)


Thread(target=guid_sound, daemon=True).start()

# game core
while running:
    if not pygame.mixer.get_busy():
        pygame.mixer.Channel(1).play(bg_sound)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    if not grabbed and isReady and not rest:
        Thread(target=holder, daemon=True).start()
        if bypass:
            grabbed = True
            if general_value == 1 and not half_cup:
                reach = 1
                half_cup = True
                squezeed_orange()
                cup = pygame.image.load(cups_levels[1])
                res_cup = pygame.transform.scale(cup, (300, 360))
                squeeze_sound.play()
            elif general_value == 2 and half_cup:
                reach = 2
                full_cup = True
                squezeed_orange()
                cup = pygame.image.load(cups_levels[2])
                res_cup = pygame.transform.scale(cup, (300, 360))
                cup_number += 1
                cups_text_surface = font.render(f"     {cup_number}", True, (255, 255, 255))
                squeeze_sound.play()

    if not stillPressed and isReady and not rest and reach >= 1:
        grabbed = False
        squeeze_sound.stop()
        orange()
        if full_cup:
            ended_orange()
            half_cup = False
            full_cup = False
            reach = 0
            if isReady:
                Thread(target=next_cup, daemon=True).start()
            if cup_number == 5:
                cup_number = 0
                round += 1
                text_surface = font.render(f"      {round}", True, (255, 255, 255))
                cups_text_surface = font.render(f"     {cup_number}", True, (255, 255, 255))
                if round < 3:
                    Thread(target=take_rest, daemon=True).start()

    update_all_objects()

    if round == 3:
        screen.blit(end_text, end_text_loc)
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

pygame.quit()

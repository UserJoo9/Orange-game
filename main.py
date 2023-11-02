import pygame
from pygame.locals import *

cups_levels = ['1.png', '2.png', '3.png']
round = 1
cup_number = 0
reach = 0
running = True
size = width, height = (700, 700)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
icon = pygame.image.load('orange.png')
pygame.display.set_icon(icon)

background = pygame.image.load('bg.jpg')
background_loc = background.get_rect()
background_loc.center = 350, 300

main_object = pygame.image.load('orange.png')
main_object_loc = main_object.get_rect()
main_object_loc.center = width-210, height/2
res_main_object = pygame.transform.scale(main_object, (320, 220))

cup_loc = main_object.get_rect()
cup_loc.center = width-200, height-150
res_cup = pygame.transform.scale(pygame.image.load(cups_levels[0]), (300, 360))

font = pygame.font.Font(None, 36)
text_surface = font.render(f"Round {round}", True, (255, 255, 255))
text_surface_loc = text_surface.get_rect()
text_surface_loc.center = 60, 30

cups_text_surface = pygame.font.Font(None, 36).render(f"Cups {cup_number}", True, (255, 255, 255))
cups_text_surface_loc = cups_text_surface.get_rect()
cups_text_surface_loc.center = 650, 30

end_text = pygame.font.Font(None, 140).render("Good job.", True, (0, 255, 0))
end_text_loc = end_text.get_rect()
end_text_loc.center = 350, 350

def sound(sound):
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                reach += 1
                main_object = pygame.image.load('squezeed.png')
                res_main_object = pygame.transform.scale(main_object, (320, 600))
                if reach == 1:
                    cup = pygame.image.load(cups_levels[reach])
                    res_cup = pygame.transform.scale(cup, (300, 360))
                    sound('squezee.mp3')
                elif reach == 2:
                    cup = pygame.image.load(cups_levels[reach])
                    res_cup = pygame.transform.scale(cup, (300, 360))
                    cup_number += 1
                    cups_text_surface = font.render(f"Cups {cup_number}", True, (255, 255, 255))
                    sound('squezee.mp3')

        if event.type == KEYUP:
            main_object = pygame.image.load('orange.png')
            res_main_object = pygame.transform.scale(main_object, (320, 220))
            if reach == 2:
                if cup_number < 5:
                    reach = 0
                cup = pygame.image.load(cups_levels[0])
                res_cup = pygame.transform.scale(cup, (300, 360))
                if cup_number == 5:
                    main_object = pygame.image.load('orange.png')
                    res_main_object = pygame.transform.scale(main_object, (320, 220))
                    cup_number = 0
                    reach = 0
                    round += 1
                    text_surface = font.render(f"Round {round}", True, (255, 255, 255))
                    if round == 3:
                        sound('win.mp3')

    screen.blit(background, background_loc)
    screen.blit(res_main_object, main_object_loc)
    screen.blit(res_cup, cup_loc)
    screen.blit(text_surface, text_surface_loc)
    screen.blit(cups_text_surface, cups_text_surface_loc)
    if round == 3:
        screen.blit(end_text, end_text_loc)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
    pygame.display.update()

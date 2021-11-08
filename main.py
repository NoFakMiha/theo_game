import random


import pygame
from sys import exit  # this will close the any of the code
import math

def display_score(level):
    current_time = pygame.time.get_ticks() - start_time
    sec = 0
    min = 0
    score_surf = main_font.render(f"{math.floor(current_time/1000)} sec | {level} Level", False, 'Black')
    score_rect = score_surf.get_rect(center=(575,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obsticle_movment(obstice_rect_list):
    if obstice_rect_list:
        for obsitlce_rect in obstice_rect_list:
            obsitlce_rect.x-=5
            if obsitlce_rect.bottom == 315  :
                screen.blit(snail_surf ,obsitlce_rect)
            else:
                screen.blit(fly_surf, obsitlce_rect)
        obstice_rect_list = [obstacle for obstacle in obstice_rect_list if obstacle.x > -50]
        return obstice_rect_list
    else: return []

def collisions(player_rect, obstacles):
    if obstacles:
        for obsticle_rect in obstacles:
            if player_rect.colliderect(obsticle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index, user_squat
    if player_rect.bottom < 315:
        player_surf = player_jump
    if user_squat:
        player_surf=player_squad

    else:
        #walk
        player_index +=0.1
        if player_index >= (len(player_run)): player_index = 0
        player_surf = player_run[int(player_index)]



pygame.init() # this to start the py game to initialize it

screen = pygame.display.set_mode((1150,385)) # setting the screen and its size, we have to give him tuple
pygame.display.set_caption("Pixel Runner | GAME MADE FOR THEO") # setting caption of the main window
clock = pygame.time.Clock() # clock object which will tel the game that it should not run faster as 60 frame/s
main_font = pygame.font.Font('fonts/VT323-Regular.ttf', 50) #Font

tittle_text = main_font.render("Pixel runner | Game made for my son Theo", False,"White")
tittle_text_rect = tittle_text.get_rect(center=(575,30))
score = 1 # for Level | Score 

instructions_text = main_font.render("Press space to start the game", False, "White")
instructions_text_rect = instructions_text.get_rect(center=(575,340))

start_time = 0

sky_surface = pygame.image.load('sprites/sky/sky.png').convert() # convert it to pygame easier png are very slow!
ground_surface = pygame.image.load('sprites/ground/ground.png').convert()
finish_line = pygame.image.load('sprites/finish_line/fin_linet.png')

# -- obstacles -- #

# snail
snail_frame_1 = pygame.image.load("sprites/enemy/snail/snail_1.png").convert_alpha()
snail_frame_2 = pygame.image.load("sprites/enemy/snail/snail_2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]
snail_speed = 1

# fly
fly_frame_1 = pygame.image.load("sprites/enemy/fly/fly_1l.png").convert_alpha()
fly_frame_2 = pygame.image.load('sprites/enemy/fly/fly_2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstice_rect_list = [] # list of enemy`s



# player running
player_stand_surf = pygame.image.load('sprites/user/user_standing.png').convert_alpha()
player_run1_surf = pygame.image.load("sprites/user/user_running_1.png")
player_run2_surf = pygame.image.load('sprites/user/user_running_2.png')
player_run = [player_run1_surf, player_run2_surf]
player_index = 0
player_jump = pygame.image.load("sprites/user/user_jump.png")
player_squad = pygame.image.load("sprites/user/user_squad.png")

player_surf = player_run[player_index]
player_rect = player_surf.get_rect(midbottom=(80,315))

player_stand_rect = player_stand_surf.get_rect(midbottom=(100, 315))
player_stand_scaled = pygame.transform.scale2x(player_stand_surf)
player_stand_scaled_rect = player_stand_scaled.get_rect(midbottom=(575, 300))

player_gravity = 0
user_squat = False
player_speed = 2
last_player_speed = 0

# sound
intro_music = pygame.mixer.Sound('music/Juhani Junkala [Retro Game Music Pack] Ending.wav')
running_music = pygame.mixer.Sound('music/Juhani Junkala [Retro Game Music Pack] Level 1.wav')

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,3000)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)

# Game logic 
game_running = False

while True:

    for event in pygame.event.get(): # to get all of the events
        if event.type == pygame.QUIT: # to check if the event was quit to close the window
            pygame.quit()
            exit() # to use exit which will close and and any code you have to import sys and give initialize it as exit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 315:
                    player_gravity = -25
            if event.key == pygame.K_DOWN:
                user_squat = True
                last_player_speed = player_speed
                player_speed = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                user_squat = False
                player_speed = last_player_speed


            if event.key == pygame.K_SPACE:

                if game_running == False:
                    game_running = True
                    player_rect.centerx = 0
                    snail_speed = 1
                    score = 1
                    start_time = pygame.time.get_ticks()
                    intro_music.stop()
                    running_music.play()
                    running_music.set_volume(0.5)


        if event.type == obstacle_timer:
            if random.randint(0,2):
                obstice_rect_list.append(snail_surf.get_rect(midbottom=(random.randint(1200,1300),315)))
            else:
                obstice_rect_list.append(fly_surf.get_rect(midbottom=(random.randint(1200,1300),200 )))
        if event.type == snail_animation_timer:
            if snail_index == 0: snail_index = 1
            else: snail_index = 0
            snail_surf = snail_frames[snail_index]

        if event.type == fly_animation_timer:
            if fly_index == 0: fly_index = 1
            else: fly_index = 0
            fly_surf = fly_frames[fly_index]
    if game_running:
        game_running = collisions(player_rect, obstice_rect_list)
        screen.blit(sky_surface,(0,0))
        screen.blit(finish_line,(900,215))
        # creating ground
        x_loc = 0
        for i in range(16):
            screen.blit(ground_surface, (x_loc, 315))
            x_loc+=73

        display_score(level=score)


        player_rect.left +=player_speed # to move the player to the left

        player_gravity +=1
        player_rect.y += player_gravity
        player_animation()
        if player_rect.bottom >=315 and user_squat == False:
            player_rect.bottom = 315

        if player_rect.bottom >=315 and user_squat == True:
            player_rect.bottom = 360
        screen.blit(player_surf, player_rect)
        
# Obsticle movement
        obstice_rect_list = obsticle_movment(obstice_rect_list)

        if player_rect.left > 900:
            player_rect.left = -30
            snail_speed +=1
            score +=1
            player_speed += 1

# Collisions
    else:
        obstice_rect_list.clear()
        player_gravity = 0
        screen.fill("Black")
        running_music.stop()
        intro_music.play()
        intro_music.set_volume(0.1)
        player_speed = 2
        last_player_speed = 0
        if score == 1:screen.blit(tittle_text, tittle_text_rect)

        else:
            score_end_txt = main_font.render(f'Your last score {score} Level', False,"White")
            score_end_txt_rect = score_end_txt.get_rect(center=(575,30))
            screen.blit(score_end_txt, score_end_txt_rect)
        screen.blit(player_stand_scaled, player_stand_scaled_rect)
        screen.blit(instructions_text,instructions_text_rect)

    pygame.display.update()
    clock.tick(60)

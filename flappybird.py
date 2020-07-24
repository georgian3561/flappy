import pygame, sys, time, random
from pygame import mixer

def animation_floor():
    screen.blit(floor, (floorX, 500))
    screen.blit(floor, (floorX + 300, 500))

def randoms_pipes():
    top_pipe = pipe_surface.get_rect(midtop = (300, random.randint(250,400)))
    bottom_pipe = pipe_surface.get_rect(midbottom = (300, (random.randint(100,120))))
    return bottom_pipe,top_pipe

def moving_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def check_collision (pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.set_volume(1)
            death_sound.play()


            return False
        if bird_rect.top<=10 or bird_rect.bottom>=570:
            return False
    return True

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=550:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def rotate_bird(bird):

    new_bird = pygame.transform.rotozoom(bird_surface,bird_movement*5,1)

    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def text_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,0))
        score_surface_rect = score_surface.get_rect(center = (180,100))
        screen.blit(score_surface,score_surface_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f"SCORE : {int(score)}", True, (255, 255, 0))
        score_surface_rect = score_surface.get_rect(center=(180, 90))
        screen.blit(score_surface, score_surface_rect)

        highscore_surface = game_font1.render(f"HIGH SCORE : {int(high_score)}", True, (0, 255, 255))
        highscore_surface_rect = score_surface.get_rect(center=(110, 480))
        screen.blit(highscore_surface, highscore_surface_rect)

def update_score(score,high_score):
    if score>high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency= 44100, size= 16, channels= 2, buffer = 512)
pygame.init()
flap_sound = pygame.mixer.Sound('Everything/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Everything/sfx_hit.wav')
die_sound = pygame.mixer.Sound('Everything/sfx_die.wav')
score_sound = pygame.mixer.Sound('Everything/sfx_point.wav')
score_sound_countdown = 100
screen_width = 350
screen_height = 600

game_font = pygame.font.SysFont("FlappyBirdy.ttf",40)

game_font1 = pygame.font.SysFont("freesansbold.ttf",50)

game_active = True
# displaying the screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
score = 0
high_score = 0
# game variables
gravity = 0.09
bird_movement = 0
bird_downflap = pygame.image.load('New folder/yellowbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('New folder/yellowbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('New folder/yellowbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
background = pygame.image.load('New folder/bg.png').convert()
bird_rect = bird_surface.get_rect(center=(100, 300))
# bird_surface = pygame.image.load('New folder/yellowbird-midflap.png').convert_alpha()
#bird_rect = bird_surface.get_rect(center=(100, 300))

floor = pygame.image.load('New folder/ground1.png').convert()
floorX = 0

pipe_surface = pygame.image.load('New folder/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
game_over_surface = pygame.image.load('New folder/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (170, 290))

# main loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement -= 10
                flap_sound.set_volume(1)
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:

                game_active = True

                pipe_list.clear()

                bird_rect.center = (100,  300)
                bird_movement = 0
                score=0

        if event.type == SPAWNPIPE:
            pipe_list.extend(randoms_pipes())
        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index+=1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    screen.blit(background, (0, 0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement

        pipe_list = moving_pipes(pipe_list)
        draw_pipes(pipe_list)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        score +=0.01
        text_display('main_game')
        score_sound_countdown-=1
        if score_sound_countdown<=0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score=score
        text_display('game_over')

    floorX -= 1
    animation_floor()

    if floorX <= -300:
        floorX = 0

    pygame.display.update()
    clock.tick(110)

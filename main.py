# arabeasy - learn to read arabic in various contexts

### SETUP ###

# libraries and modules and stuff
import sys, pygame
import random
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import time
pygame.init()

# load images
main_image = pygame.image.load("images/mainscreen.png")
info_image = pygame.image.load("images/info.png")
countdown_images = [
    pygame.image.load("images/go.png"),
    pygame.image.load("images/1.png"),
    pygame.image.load("images/2.png"),
    pygame.image.load("images/3.png"),
]

# load fonts
lexend_bold = pygame.font.Font("fonts/Lexend/static/Lexend-Bold.ttf", 26)

# universal variables
width, height = 900, 600
color_pallete = {
    "red": (238, 42, 53),
    "green": (0, 151, 54),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "button": (245, 238, 230),
    "buttonHover": (150, 150, 150),
    "buttonText": (35, 35, 40)
}


# create the window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("arabeasy!")

### FUNCTIONS ###

# create a button
def createButton(screen, text, rect, color, hover_color, text_color):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    
    buttonText = lexend_bold.render(text, True, text_color)
    buttonTextRect = buttonText.get_rect(center=(rect.centerx, rect.centery))
    screen.blit(buttonText, buttonTextRect)

# fade in an image
def fadeInImage(image):
    global alpha, fade_in
    alpha += 10
    if alpha >= 255:
        alpha = 255
        fade_in = False
    image.set_alpha(alpha)

# fade out an image
def fadeOutImage(image):
    global alpha, fade_out, countdown_index
    alpha -= 10
    if alpha <= 0:
        alpha = 0
        fade_out = False
        countdown_index -= 1
    image.set_alpha(alpha)

# display the countdown
def displayCountdown():
    global countdown_index, fade_in, fade_out, countdown_screen
    screen.blit(countdown_images[countdown_index], (0, 0))
    time.sleep(0.5)
    countdown_index -= 1
    if countdown_index < 0:
        countdown_index = 3
        countdown_screen = False
    else:
        fade_in = True


### MAIN LOOP ###

# default states
running = True
fade_in = True
main_screen = True
fade_out = False
info_screen = False
countdown_screen = False
game_screen = False
end_screen = False
alpha = 0
countdown_index = 3
begin_switch = False

while running:

    # main screen

    if main_screen:
        if fade_in:
            fadeInImage(main_image)
        screen.fill(color_pallete["black"])
        screen.blit(main_image, (0, 0))
        start_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 10 - 15, 300, 50)
        createButton(screen, "start!", start_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["red"])
        quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 10 + 60, 300, 50)
        createButton(screen, "quit", quit_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["black"])
        if begin_switch:
            if fade_out:
                fadeOutImage(main_image)
                screen.fill(color_pallete["black"])
                screen.blit(main_image, (0, 0))
            else:
                main_screen = False
                info_screen = True
                begin_switch = False
    
    # info screen
    if info_screen:
        fadeInImage(info_image)
        screen.fill(color_pallete["black"])
        screen.blit(info_image, (0, 0))
        ready_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 10 + 100, 300, 50)
        createButton(screen, "ready!", ready_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["red"])
        if begin_switch:
            info_screen = False
            countdown_screen = True
            begin_switch = False
            countdown_index = 3
    
    # countdown screen
    if countdown_screen:
        displayCountdown()
        



    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # main screen
        if main_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    begin_switch = True
                    fade_out = True
        
        # info screen
        if info_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button_rect.collidepoint(event.pos):
                    begin_switch = True
                    fade_out = True
                    
    # update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
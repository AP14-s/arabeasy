# arabeasy - learn to read arabic in various contexts

### SETUP ###

# libraries and modules and stuff
import sys, pygame
import random
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import time
import csv
pygame.init()

# load images
main_image = pygame.image.load("images/mainscreen.png")
info_image = pygame.image.load("images/info.png")
game_bg = pygame.image.load("images/gamebg.png")
countdown_images = [
    pygame.image.load("images/go.png"),
    pygame.image.load("images/1.png"),
    pygame.image.load("images/2.png"),
    pygame.image.load("images/3.png"),
]

# load fonts
lexend_bold = pygame.font.Font("fonts/Lexend/static/Lexend-Bold.ttf", 26)
arabic_fonts = [
    pygame.font.Font("fonts/Alkalami-Regular.ttf", 90),
    pygame.font.Font("fonts/ArefRuqaa-Regular.ttf", 90),
    pygame.font.Font("fonts/Blaka-Regular.ttf", 90),
    pygame.font.Font("fonts/Far_Vosta.ttf", 90),
    pygame.font.Font("fonts/Handjet-Medium.ttf", 90),
    pygame.font.Font("fonts/jb-funland.ttf", 90),
    pygame.font.Font("fonts/Rakkas-Regular.ttf", 90),
    pygame.font.Font("fonts/ReemKufi-Bold.ttf", 90),
]

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
question_number = 1
correct_answers = 0
selected_word = False
in_arabic = ""
timer_start = 60
timer_value = timer_start
timer_running = False
last_update_time = 0
options = []
answered = False
correct = "Correct Answer"
wrong1 = "Wrong Answer 1"
wrong2 = "Wrong Answer 2"
wrong3 = "Wrong Answer 3"
answer_time = 0
game_over = False


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

def resetGame():
    global correct_answers, question_number, timer_value, timer_running, game_screen, main_screen, game_over, answered, selected_word

    correct_answers = 0
    question_number = 1
    timer_value = 60 
    timer_running = False
    game_screen = False
    main_screen = True
    game_over = False
    answered = False
    selected_word = False

def updateTimer():
    global timer_value, timer_running, last_update_time, game_over
    if timer_running:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - last_update_time) / 1000  # milliseconds to seconds
        if elapsed_time >= 1:
            timer_value -= int(elapsed_time)
            last_update_time = current_time
        if timer_value <= 0:
            timer_value = 0
            timer_running = False
            game_over = True  # set game over flag

# display the countdown
def displayCountdown():
    global countdown_index, fade_in, fade_out, countdown_screen, game_screen, timer_running, last_update_time
    screen.blit(countdown_images[countdown_index], (0, 0))
    pygame.time.delay(500)
    countdown_index -= 1
    if countdown_index < -1:
        countdown_index = 3
        countdown_screen = False
        game_screen = True
        timer_running = True  # Start the timer
        last_update_time = pygame.time.get_ticks()  # Initialize last update time
    else:
        fade_in = True

def gameLogic():
    global in_arabic, options, selected_word, selected_font, correct
    if selected_word == False: 
        # open and read the CSV file
        with open('words.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
        # select a random line
        random_line = random.choice(lines)
        in_arabic, correct, wrong1, wrong2, wrong3 = random_line
        selected_font = random.choice(arabic_fonts)
        selected_font.set_script("Arab")
        selected_font.set_direction(pygame.DIRECTION_RTL)
        positions = [
            pygame.Rect(110, height // 2 + 50, 300, 60),
            pygame.Rect(width - 410, height // 2 + 50, 300, 60),
            pygame.Rect(110, height // 2 + 150, 300, 60),
            pygame.Rect(width - 410, height // 2 + 150, 300, 60)
        ]
        random.shuffle(positions)
        options = [
            (correct, positions[0]),
            (wrong1, positions[1]),
            (wrong2, positions[2]),
            (wrong3, positions[3])
        ]
        selected_word = True
        return in_arabic, options, selected_font
    else:
        return in_arabic, options, selected_font

def displayGameOverPopup():
    global correct_answers, question_number, game_screen, main_screen, game_over

    total_questions = question_number - 1
    if total_questions > 0:
        correct_percentage = (correct_answers / total_questions) * 100
    else:
        correct_percentage = 0

    popup_surface = pygame.Surface((400, 300))
    popup_surface.fill(color_pallete["white"])
    popup_rect = popup_surface.get_rect(center=(width // 2, height // 2))

    correct_text = lexend_bold.render(f"{correct_answers} correct answers!", True, color_pallete["black"])
    percentage_text = lexend_bold.render(f"{correct_percentage:.2f}% accuracy!", True, color_pallete["black"])
    correct_rect = correct_text.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50))
    percentage_rect = percentage_text.get_rect(center=(popup_rect.centerx, popup_rect.centery))

    screen.blit(popup_surface, popup_rect)
    screen.blit(correct_text, correct_rect)
    screen.blit(percentage_text, percentage_rect)

    back_button_rect = pygame.Rect(popup_rect.centerx - 125, popup_rect.centery + 50, 250, 50)
    createButton(screen, "main menu", back_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["black"])

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    waiting = False
                    resetGame()


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
    updateTimer()

    # main screen

    if main_screen:
        if fade_in:
            fadeInImage(main_image)
        screen.fill(color_pallete["black"])
        screen.blit(main_image, (0, 0))
        start_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 30, 300, 60)
        createButton(screen, "start!", start_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["red"])
        quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 10 + 100, 300, 60)
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
        ready_button_rect = pygame.Rect(width // 2 - 150, height // 2 + 10 + 100, 300, 60)
        createButton(screen, "ready!", ready_button_rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["red"])
        if begin_switch:
            info_screen = False
            countdown_screen = True
            begin_switch = False
            countdown_index = 3
    
    # countdown screen
    if countdown_screen:
        displayCountdown()
    
    # game screen
    if game_screen:
        in_arabic, options, selected_font = gameLogic()
        screen.fill(color_pallete["black"])
        screen.blit(game_bg, (0, 0))

        arabic_text_surface = selected_font.render(in_arabic, True, color_pallete["white"])
        arabic_text_rect = arabic_text_surface.get_rect(center=(width // 2, height // 2 - 115))
        screen.blit(arabic_text_surface, arabic_text_rect)

        question_number_surface = lexend_bold.render(f"{correct_answers}/{question_number}", True, color_pallete["white"])
        question_number_rect = question_number_surface.get_rect(center=(60, 50))
        screen.blit(question_number_surface, question_number_rect)

        timer_number_surface = lexend_bold.render(f"{timer_value // 60}:{timer_value % 60:02d}", True, color_pallete["white"])
        timer_number_rect = timer_number_surface.get_rect(center=(width - 70, 50))
        screen.blit(timer_number_surface, timer_number_rect)

        for text, rect in options:
            createButton(screen, text, rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["black"])

        if answered:
            current_time = pygame.time.get_ticks()
            for text, rect in options:
                if text == correct:
                    createButton(screen, text, rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["green"])
                    result_surface = lexend_bold.render(f"Correct!", True, color_pallete["green"])
                elif text == selected_option:
                    createButton(screen, text, rect, color_pallete["button"], color_pallete["buttonHover"], color_pallete["red"])
                    result_surface = lexend_bold.render(f"Incorrect!", True, color_pallete["red"])
            result_rect = result_surface.get_rect(center=(width // 2, 50))
            screen.blit(result_surface, result_rect)
            if current_time - answer_time >= 1000:
                answered = False
                question_number += 1
                selected_word = False


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
                if quit_button_rect.collidepoint(event.pos):
                    running = False
        
        # info screen
        if info_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button_rect.collidepoint(event.pos):
                    begin_switch = True
                    fade_out = True
        
        # game screen
        if game_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, rect in options:
                    if rect.collidepoint(event.pos):
                        selected_option = text
                        if text == correct:
                            print("correct!")
                            correct_answers += 1
                        else:
                            print(f"{text} - incorrect")
                        answered = True
                        answer_time = pygame.time.get_ticks()
                        break
                    
    if game_over:
        displayGameOverPopup()
    else:
        pygame.display.flip()

# Quit pygame
pygame.quit()
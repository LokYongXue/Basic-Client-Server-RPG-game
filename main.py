#RPG game using TCP 
import pygame
from sprites import *
from config import *
import sys
import socket

class Game:
    def __init__(self):
        pygame.init()  #initial method to use pygame
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))  #create game window with WIN_WIDTH,WIN_HEIGHT
        self.clock = pygame.time.Clock()  # allow to set frame rate of game
        self.font = pygame.font.Font('ARIAL.TTF',32) 
        self.font_question = pygame.font.Font('ARIAL.TTF',18)
        self.running = True
        self.score = 0
        
        #load the image from the file
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.gameOver_background = pygame.image.load('./img/gameover.png')
        self.question_background = pygame.image.load('./img/question.png')
        self.gamepass_background = pygame.image.load('./img/gamepass.png')
         
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i) #j for x position, i for y position
                if column =="B":
                    Block(self, j, i)
                if column =='E':
                    enemy = Enemy(self,j,i)
                    if len(self.question) > 0:
                        enemy.question = self.question.pop(0)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        # a new game start
        self.playing = True # use to determine whether the player died or exit

        #Question Pools
        #1 page 8
        #2 page 4
        #3 page 6
        #4 page 12 
        #5 page 8
        self.question = [
    {"text": "Which of the following is NOT an argument for the socket.getsockopt() method?", "choices": ["SOCKET_ADDRESS", "OPTNAME", "LEVEL", "VALUE"], "correct_answer": "SOCKET_ADDRESS"},
    {"text": "Which of the following protocols commonly uses stream sockets?", "choices": ["SMTP", "TCP", "ICMP", "UDP"], "correct_answer": "TCP"},
    {"text": "Which of the following methods is used to retrieve socket options?", "choices": ["socket.bind()", "socket.close()", "socket.setsockopt()", "socket.getsockopt()"], "correct_answer": "socket.getsockopt()"},
    {"text": "Which of the following cannot be socket mode?", "choices": ["Blocking", "Non-blocking", "Connectionless", "Timeout"], "correct_answer": "Connectionless"},
    {"text": "What is the purpose of the socket.getsockopt() method?", "choices": ["To bind a socket to a specific address", "To set a socket option", "To close a socket connection", "To get the value of a socket option"], "correct_answer": "To get the value of a socket option"},
]
        self.answered_correctly = False #Reset State
        self.all_sprites = pygame.sprite.LayeredUpdates()  # group all the sprite so that all can be update at once
        self.blocks = pygame.sprite.LayeredUpdates() # for all the blocks/wall
        self.enemies = pygame.sprite.LayeredUpdates() # for the enemies

        self.createTilemap()
    

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    # update the screen so that it would not only a static image
    def update(self):
        self.all_sprites.update() # find the update method in the sprites.py that already code

        # Check for collision between player and enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            for enemy in hits:
                if not enemy.answered:
                    self.question_screen(enemy.question)
                    if self.answered_correctly:
                        enemy.answered = True  # Mark as answered
                        enemy.kill()
                    else:
                        self.game_over()

                #self.question_screen(enemy.question)
                #if self.answered_correctly:
                #   enemy.kill()
                
        
        if len(self.enemies) == 0:
            self.gamepass_screen()
  
    # display the sprite on the screen
    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(str(self.score), True, RED)
        score_rect = score_text.get_rect(topright=(WIN_WIDTH - 10, 10))
        self.screen.blit(score_text, score_rect)  #blit use to draw the parameter into the surface

        self.clock.tick(FPS) # control the frame per second to update
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def game_over(self):

        self.score = 0
        sock.send(str(self.score).encode('utf-8'))# Send updated score to server

        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT-60, 200, 50, WHITE, BLACK, 'Try again', 32)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running == False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos,mouse_pressed):
                self.new()
                self.main()
                
            #(0,0) left corner
            self.screen.blit(self.gameOver_background,(0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        title = self.font.render('Mini Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos,mouse_pressed):
                intro = False
                

            self.screen.blit(self.intro_background,(0,0))
            self.screen.blit(title,title_rect)
            self.screen.blit(play_button.image,play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def question_screen(self, question_data):
        # Extract question details
        question_text = question_data["text"]
        choices = question_data["choices"]
        correct_answer = question_data["correct_answer"]

        question_rendered = self.font_question.render(question_text, True, BLACK)
        question_rect = question_rendered.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 3))

        choice_buttons = []
        button_width, button_height = 400, 50
        button_y_start = WIN_HEIGHT / 2

        # Create buttons for choices
        for i, choice in enumerate(choices):
            button_x = (WIN_WIDTH - button_width) / 2
            button_y = button_y_start + i * (button_height + 10)
            button = Button(button_x, button_y, button_width, button_height, WHITE, BLACK, choice, 18)
            choice_buttons.append((choice, button))

        self.answered_correctly = False

        while self.running and not self.answered_correctly:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Check button presses
            for choice, button in choice_buttons:
                if button.is_pressed(mouse_pos, mouse_pressed):
                    if choice == correct_answer:
                        self.answered_correctly = True
                        self.add_score(20)  # Add 20 points for a correct answer

                        # Kill the enemy immediately to prevent the score add twice
                        for sprite in self.enemies:
                            if sprite.rect.colliderect(self.player.rect):
                                sprite.kill()
  
                    else:
                        self.game_over()
                    return

            #Clear queued events to avoid multiple detections (prevent score added twice)
            pygame.event.clear()

            # Display background, question, and choices
            self.screen.blit(self.question_background, (0, 0))  
            self.screen.blit(question_rendered, question_rect)
            for _, button in choice_buttons:
                self.screen.blit(button.image, button.rect)

            self.clock.tick(FPS)
            pygame.display.update()


    def add_score(self, points):
        self.score += points
        print(f"Score: {self.score}")
        sock.send(str(self.score).encode('utf-8'))# Send updated score to server


    def gamepass_screen(self):
        text = self.font.render('Congratulation', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        text_from_server = self.font.render(msg, True, WHITE)
        text_from_server = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        exit_button = Button(WIN_WIDTH-180, WIN_HEIGHT-60, 120, 50, WHITE, BLACK, 'Exit', 32)
        
        for sprite in self.all_sprites:
            sprite.kill()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running == False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if exit_button.is_pressed(mouse_pos,mouse_pressed):
                pygame.quit()
                sys.exit()

            #(0,0) left corner
            self.screen.blit(self.gamepass_background,(0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

#End of class game

#tcp connection 
print('Welcome to TCP Mini RPG game')
client_name = input('Enter your character name: ')
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect( (SERVER_HOST,SERVER_PORT) )
sock.send(client_name.encode('utf-8'))

while True:
    
    msg = sock.recv(1024).decode('UTF-8')
    if msg == 'Start':
        g = Game()
        g.intro_screen()
        g.new()
        while g.running:
            g.main()

        pygame.quit()
        sys.exit()
        break
print('Connection closed')
sock.close()
sys.exit()    




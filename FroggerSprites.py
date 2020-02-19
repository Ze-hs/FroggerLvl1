import pygame, random
class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.__image_list = []
        for index in range(8):
            self.__image_list.append("frog" + str(index) + ".png")
        self.__image_reset = self.__image_list[0]
        self.image = pygame.image.load(self.__image_list[0])
        self.image.convert()
        self.__screen = screen
        self.__extra_speed = 0
        self.rect = self.image.get_rect()
        self.reset_position()
        self.reset_movement()    
        
        self.__displacement = 0
        self.__moving = False
        
    def go_left(self):
        self.__dx -= 4
        self.__moving = True
        self.__image_reset = self.__image_list[2]
        self.image = pygame.image.load(self.__image_list[3])         
        
    def go_right(self):
        self.__dx += 4
        self.__moving = True
        self.__image_reset = self.__image_list[6]
        self.image = pygame.image.load(self.__image_list[7])         
      
    def go_up(self):
        self.__dy -= 4
        self.__moving = True
        self.__image_reset = self.__image_list[0]
        self.image = pygame.image.load(self.__image_list[1])        

    def go_down(self):
        self.__dy += 4
        self.__moving = True
        self.__image_reset = self.__image_list[4]
        self.image = pygame.image.load(self.__image_list[5])         
        
    def get_movement(self):
        return self.__moving 
        
    def get_above_water(self):
        if self.rect.top < self.__screen.get_height()/2 and self.rect.bottom > (32 * 2):
            return True    
        else:
            return False
        
    def reset_position(self):
        self.rect.centery = self.__screen.get_height() - 48
        self.rect.left = self.__screen.get_width()/2
        self.__displacement = 0
   
    def riding(self, speed):
        self.__extra_speed = speed
        self.__ride_log = True
        
    def not_riding(self):
        self.__extra_speed = 0
        self.__ride_log = False
        
    def reset_movement(self):
        self.__dx = 0
        self.__dy = 0
        self.__moving = False
        
    def update(self):
        self.rect.left += self.__dx + self.__extra_speed
        self.rect.top += self.__dy
        self.__displacement += self.__dx + self.__dy
        if self.__displacement % 32 == 0 and self.__displacement % 32 == 0:
            self.image = pygame.image.load(self.__image_reset)
            self.reset_movement() 
            
class Log(pygame.sprite.Sprite):
    def __init__(self, row, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.__image_list = []
        for index in range(2):
            self.__image_list.append("log" + str(index) + ".png")        
        self.image = pygame.image.load(self.__image_list[random.randint(0,1)])
        
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (7 - row) 
        self.rect.left = 0
        
        self.__screen = screen
        self.__dx = random.randint(2, 4)
        
    def get_speed(self):
        return self.__dx
    
    def update(self):
        self.rect.left += self.__dx
        if self.rect.left > self.__screen.get_width():
            self.rect.right = 0 

class Turtle(pygame.sprite.Sprite):
    def __init__(self, row, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__image_list = []
        for index in range(8):
            self.__image_list.append("turtle" + str(index) + ".png")
        self.image = pygame.image.load(self.__image_list[0])
        self.__current_image = 0
        
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (7 - row) 
        self.rect.right =  0
        
        self.__screen = screen
        self.__dx = -random.randint(1, 2)
        self.__on_surface = True
    
    def get_speed(self):
        return self.__dx
    
    def change_image(self):
        self.__current_image += 1
            
    def surface(self):
        self.__on_surface = True
        
    def dived(self):
        self.__on_surface = False
        
    def get_state(self):
        return self.__on_surface
    
    def update(self):
        self.rect.left += self.__dx
        
        if self.rect.right < 0:
            self.rect.left = self.__screen.get_width()
        
        if self.image == self.__image_list[4]:
            self.surfaced()
        elif self.image == self.__image_list[0]:
            self.dived()
        if self.__current_image >= 2 and self.__on_surface:
            self.__current_image = 0
        elif self.__current_image >= 8:
            self.__current_image = 0
        self.image = pygame.image.load(self.__image_list[self.__current_image])


class Car(pygame.sprite.Sprite):
    def __init__(self, row, speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__image_list = []
        for index in range(4):
            self.__image_list.append("car" + str(index) + ".png")        
        self.image = pygame.image.load(self.__image_list[random.randint(0,3)])
        
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (13 - row) 
        self.__row = row
        
        self.__screen = screen
        if row % 2:
            self.__dx = -speed
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.left = screen.get_width()
        else:
            self.__dx = speed
            self.rect.left = 0
    def get_row(self):
        return self.__row
    
    def get_speed(self):
        return self.__dx
    def update(self):
        self.rect.left += self.__dx
        if self.rect.left >= self.__screen.get_width():
            self.kill()
        elif self.rect.right <= 0:
            self.kill()
            
class Lives_keeper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.SysFont("arial", 30)
        self.__lives = 3

    def lose_life(self):
        self.__lives -= 1

    def game_over(self):
        if self.__lives == 0:
            return True

    def update(self):
        self.image = self.__font.render("Lives: " + str(self.__lives), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 15)
        
class Time_keeper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.SysFont("arial", 30)
        self.__time_left = 50
        
    def count_down(self):
        self.__time_left -= 1

    def time_up(self):
        if self.__time_left == 0:
            return True

    def update(self):
        self.image = self.__font.render("Time " + str(self.__time_left), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 15)
        
class Score_keeper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.SysFont("arial", 30)
        self.__score = 0
        self.__spots = 5
        
    def win(self):
        self.__score += 10
        self.__spots -= 1
        
    def increase_score(self):
        return self.__score 
        
    def get_goals_left(self):
        return self.__spots 

    def update(self):
        self.image = self.__font.render("Score " + str(self.__score), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (220, 15)

class Goal(pygame.sprite.Sprite):
    def __init__(self, row, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((10 , 10))
        self.image.fill((0,0, 0))
        self.image.convert()
        self.image.set_colorkey((0,0,0))
        
        self.rect = self.image.get_rect()
        self.rect.top = 32 * 2
        self.rect.right = (128 * row) + 35
        self.__taken = False
    
    def occupy(self):
        self.__taken = True
        self.image = pygame.image.load("frog0.png")
        
    def get_taken(self):
        return self.__taken

            
class Grid(pygame.sprite.Sprite):
    
    def __init__(self, screen, background):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((screen.get_size()))
        self.image.fill((255,255,255))
        self.__height = 32
        self.__width = 32
        self.rect = self.image.get_rect()
        
        for row in range(0, screen.get_height(), self.__height):
            pygame.draw.line(self.image, (45,163,52), (0,row), (screen.get_width(),row), 1)
            for col in range(0, screen.get_width(), self.__width):
                pygame.draw.line(self.image, (45,163,52), (col, 0), (col,screen.get_height()), 1)
        
        

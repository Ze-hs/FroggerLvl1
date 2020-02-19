'''
Author: Ze Hao Su

Date: May 30, 2018

Description: This module includes all the classes necessary to create the game 
             Frogger
'''

import pygame, random

class Background(pygame.sprite.Sprite):
    '''This class creates the background image sprites'''
    
    def __init__(self, screen):
        '''This update method just displays the image'''
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load("background.jpg")
        self.rect = self.image.get_rect()
        
class Player(pygame.sprite.Sprite):
    '''This class creates the player sprites. It controls the movement
    of the player as well as the position of the player. It takes in 1 parameter
    which is the screen.
    '''
    def __init__(self, screen):
        '''This initializer method initializes the basic instance variables
        suchs as image lists, image, rect, and speed'''
        pygame.sprite.Sprite.__init__(self)
        
        #Loads all the images for the player
        self.__image_list = []
        for index in range(8):
            self.__image_list.append("frog" + str(index) + ".png")
        
        #Sets up the starting image
        self.__image_reset = self.__image_list[0]
        self.image = pygame.image.load(self.__image_list[0])
        self.image.convert()
        self.__screen = screen
        
        #Sets up the initial position and speed
        self.rect = self.image.get_rect()
        self.reset_position()
        self.reset_movement() 
        self.__extra_speed = 0        
        self.__displacement = 0
        self.__moving = False
        
    def go_left(self):
        '''This method allows the player to move to the left and change the 
        image accordingly. Takes no parameters and does not return anything'''
        self.__dx -= 8
        self.__moving = True
        self.__image_reset = self.__image_list[2]
        self.image = pygame.image.load(self.__image_list[3])         
        
    def go_right(self):
        '''This method allows the player to move to the right and change the 
        image accordingly. Takes no parameters and does not return anything'''        
        self.__dx += 8
        self.__moving = True
        self.__image_reset = self.__image_list[6]
        self.image = pygame.image.load(self.__image_list[7])         
      
    def go_up(self):
        '''This method allows the player to move to the up and change the 
        image accordingly. Takes no parameters and does not return anything'''        
        self.__dy -= 8
        self.__moving = True
        self.__image_reset = self.__image_list[0]
        self.image = pygame.image.load(self.__image_list[1])        

    def go_down(self):
        '''This method allows the player to move to the down and change the 
        image accordingly. Takes no parameters and does not return anything'''        
        self.__dy += 8
        self.__moving = True
        self.__image_reset = self.__image_list[4]
        self.image = pygame.image.load(self.__image_list[5])         
        
    def get_movement(self):
        '''This method return the boolean value that checks if the player
        is moving or not. Takes no parameters'''
        return self.__moving 
        
    def get_above_water(self):
        '''This method return the boolean value that checks if the player
        is on the top half of the screen. Takes no parameters'''        
        if self.rect.top < self.__screen.get_height()/2 and self.rect.bottom > (32 * 2):
            return True    
        else:
            return False
        
    def reset_position(self):
        '''This method resets the player's position to the bottom of the screen.
        Takes no parameters and does not return anything'''
        self.rect.centery = self.__screen.get_height() - 48
        self.rect.left = self.__screen.get_width()/2
        self.__displacement = 0
   
    def riding(self, speed):
        '''This method takes a integer or a float number and determines the
        extra speed that would be added to the player. Does not return anything.'''
        self.__extra_speed = speed
        self.__riding = True
        
    def not_riding(self):
        '''This method sets the extra speed to 0. Takes no parameters and does
        not return anything.'''
        self.__extra_speed = 0
        self.__riding = False
        
    def reset_movement(self):
        '''This method sets the player's speed to 0. Takes no parameters and does
        not return anything.'''        
        self.__dx = 0
        self.__dy = 0
        self.__moving = False
        
    def update(self):
        '''This update method stops the player when reaching the game screen 
        or when the player has moved 32 pixels. It also moves the player'''
        #If the player reaches the ends of the game screen then stops it from
        #going further
        if (self.rect.left <= 0 and self.__dx < 0) or \
           (self.rect.right >= self.__screen.get_width() and self.__dx > 0) or\
           (self.rect.bottom >= self.__screen.get_height() -32 and self.__dy > 0):
            self.reset_movement() 
            self.__displacement = 0
        
        #Moves the player based on the total speed 
        self.rect.left += self.__dx + self.__extra_speed
        self.rect.top += self.__dy
        self.__displacement += self.__dx + self.__dy
        
        #If the player has moved 32 pixels then it stops moving and changes its
        #image accordingly
        if self.__displacement % 32 == 0:
            self.image = pygame.image.load(self.__image_reset)
            self.reset_movement() 
        
class Log(pygame.sprite.Sprite):
    '''This class creates the log sprites. It controls the movement
    of the log as well as the position of the log. It takes in 3 parameters
    which is the row number, speed of the log and the screen.'''
    
    def __init__(self, row, speed, screen):
        '''This initializer method initializes the basic instance variables
        suchs as image lists, image, rect, and speed'''        
        
        pygame.sprite.Sprite.__init__(self)
        #Loads the image lists
        self.__image_list = []
        for index in range(2):
            self.__image_list.append("log" + str(index) + ".png")        
        self.image = pygame.image.load(self.__image_list[random.randint(0,1)])
        
        #Sets the image and locations
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (7 - row) 
        self.rect.right = 0
        
        #Make the rect smaller for collision purposes
        self.rect = self.rect.inflate(-16, 0)
    
        self.__screen = screen
        self.__dx = speed
        self.__row = row
    
    def get_speed(self):
        '''This method returns the speed of the log. Takes no parameters'''
        return self.__dx
    
    def get_row(self):
        '''This method returns the row of the log. Takes no parameters'''
        return self.__row
   
    def update(self):
        '''This updater method resets the postion of the log to the left of the 
        screen when the log reaches the end of the screen'''
        self.rect.left += self.__dx
        if self.rect.left > self.__screen.get_width():
            self.rect.right = 0

class Turtle(pygame.sprite.Sprite):
    '''This class creates the turtle sprites. It controls the movement
    of the turtle as well as the position of the turtle. It takes in 3 parameters
    which is the row number, speed and the screen.'''    
    
    def __init__(self, row, speed, screen):
        '''This initializer method initializes the basic instance variables
        suchs as image lists, image, rect, and speed'''         
        
        pygame.sprite.Sprite.__init__(self)
        #This loads all the images for the turtle 
        self.__image_list = []
        for index in range(8):
            self.__image_list.append("turtle" + str(index) + ".png")
        #Sets the starting image
        self.image = pygame.image.load(self.__image_list[0])
        self.__current_image = 0
        
        #Sets the location and speed
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (7 - row) 
        self.rect.left =  screen.get_width()
        self.__dx = speed
        
        self.__screen = screen
        self.__on_surface = True
        self.__row = row
        self.__moved = False
    
    def get_speed(self):
        '''This method returns the speed of the turtle. Takes no parameters.'''
        return self.__dx
    
    def get_row(self):
        '''This method returns the row number of the turtle. Takes no parameters.'''
        return self.__row    
    
    def change_image(self):
        '''This method adds 1 to the counter controlling the image of the turtle.
        Takes no parameters and does not return anything'''
        self.__current_image += 1
            
    def surface(self):
        '''This method sets an instance variable to True to later check if the 
        turtle dived or not. Takes no parameters and does not return anything'''
        self.__on_surface = True
        
    def dived(self):
        '''This method sets an instance variable to False to later check if the 
        turtle dived or not. Takes no parameters and does not return anything'''        
        self.__on_surface = False
        
    def get_state(self):
        '''This method returns a boolean value to check if the turtle dived or 
        not. Takes no parameters.'''
        return self.__on_surface
    
    def update(self):
        '''This updater method moves the turtle and kills it if it leaves the 
        screen. Also checks if it dived or not and changes the image accordingly'''
        self.rect.left += self.__dx
        
        #Kills the sprite if it leaves the screen
        if self.rect.right <= 0:
            self.kill()
        
        #Calls a method that tells the turtle it dived
        if self.image == self.__image_list[4]:
            self.dived()
        elif self.image == self.__image_list[0]:
            self.surfaced()
        
        #If the turtle has not dived yet, the turtle loops throught 2 images
        if self.__current_image >= 2 and self.__on_surface:
            self.__current_image = 0
        #If the image has completely dived which is in image 4, then move
        #the rect so the player cannot reach it
        elif self.__current_image == 4 and not self.__moved:
            self.rect.centery -= 600
            self.__moved = True
        #If it finished diving and is surfacing, move the rect back
        elif (not self.__current_image == 4) and self.__moved:
            self.rect.centery +=  600
            self.__moved = False
        #If the turtle if diving, the turtle loops through 8 images
        elif self.__current_image >= 8:
            self.__current_image = 0
        self.image = pygame.image.load(self.__image_list[self.__current_image])


class Car(pygame.sprite.Sprite):
    '''This class creates the car sprites. It controls the movement
    of the car as well as the position of the car. It takes in 3 parameters
    which is the row number, speed and the screen.'''   
    
    def __init__(self, row, speed, screen):
        '''This initializer method initializes the basic instance variables
        suchs as image lists, image, rect, and speed'''         
        pygame.sprite.Sprite.__init__(self)
        
        #This loads all the images for the car
        self.__image_list = []
        for index in range(4):
            self.__image_list.append("car" + str(index) + ".png")   
        
        #sets the starting image and and starting location
        self.image = pygame.image.load(self.__image_list[random.randint(0,3)])
        self.rect = self.image.get_rect()
        self.rect.top = 32 * (13 - row)
        
        self.__row = row
        self.__screen = screen
        
        #This makes it so that the cars in every other row would move in the same
        #direction
        if row % 2:
            self.__dx = -speed
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.left = screen.get_width()
        #As for the rest of the cars, they would move on the opposite direction
        else:
            self.__dx = speed
            self.rect.left = 0
            
    def get_row(self):
        '''This method returns the row of the car. Takes no parameters'''
        return self.__row
    
    def get_speed(self):
        '''This method returns the speed of the car. Takes no parameters'''
        return abs(self.__dx)
    
    def update(self):
        '''This updater method makes it so that when the car leaves the screen,
        it would kill itself'''
        self.rect.left += self.__dx
        if self.rect.left >= self.__screen.get_width() or self.rect.right <= 0:
            self.kill()
            
class Lives_keeper(pygame.sprite.Sprite):
    '''This class creates the sprite for the lives keeper'''
    def __init__(self):
        '''This initializer initializes the font as well as the the 
        instance variable containing the lives remaning'''
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("FreeSansBold.ttf", 25)
        self.__lives = 3

    def lose_life(self):
        '''This method reduces the amount of lives left. Takes no parameter and
        does not return anything'''
        self.__lives -= 1

    def game_over(self):
        '''This method returns True if remaining lives reaches 0. Takes no parameters'''
        if self.__lives == 0:
            return True

    def update(self):
        '''This updater method displays the lives remaining'''
        self.image = self.__font.render("Lives: " + str(self.__lives), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (500, 20)
        
class Time_keeper(pygame.sprite.Sprite):
    '''This class creates the sprite for the time keeper'''
    def __init__(self):
        '''This initializer initializes the font as well as the the 
        instance variable containing the time'''
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("FreeSansBold.ttf", 25)
        self.__time_left = 30
    
    def increase_time(self):
        '''This method increases the time remaining. Takes no parameters and
        does not return anything'''
        self.__time_left += 15
        
    def count_down(self):
        '''This method reduces the time remaining.  Takes no parameters and
        does not return anything'''
        self.__time_left -= 1

    def time_up(self):
        '''This method returns True if the time remaining reaches 0'''
        if self.__time_left == 0:
            return True

    def update(self):
        '''This updater method displays the time remaining'''
        self.image = self.__font.render("Time " + str(self.__time_left), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (80, 20)
        
class Score_keeper(pygame.sprite.Sprite):
    '''This class creates the sprite for the score keeper'''
    def __init__(self):
        '''This initializer initializes the font as well as the the 
        instance variable containing the score and the amount of end goals left'''        
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.Font("FreeSansBold.ttf", 25)
        self.__score = 0
        self.__spots = 5
        
    def win(self):
        '''This method increases the score and reduces the amount of end goals.
        Takes no parameters and does return anything.'''
        self.__score += 100
        self.__spots -= 1
        
    def get_goals_left(self):
        '''This method returns the amount of end goals left. Takes no parameters'''
        return self.__spots 

    def update(self):
        '''This updater method displays the score'''
        self.image = self.__font.render("Score " + str(self.__score), 1, (175, 157, 192))
        self.rect = self.image.get_rect()
        self.rect.center = (290, 20)

class Goal(pygame.sprite.Sprite):
    '''This class creates the end goal sprites. It controls the position and 
    the image of the goal. It takes in 2 parameters which is the row number, and the screen.'''      
    def __init__(self, row, screen):
        """This initializer initializes the basic instance variables"""
        pygame.sprite.Sprite.__init__(self)
        
        #Creates the surface and hides it
        self.image = pygame.Surface((10 , 10))
        self.image.fill((0,0, 0))
        self.image.convert()
        self.image.set_colorkey((0,0,0))
        
        #Sets the position of the goals
        self.rect = self.image.get_rect()
        self.rect.top = 32 * 2
        self.rect.right = (128 * row) + 35
        self.__taken = False
        self.__row = row
    
    def occupy(self):
        '''This method changes the image and makes it no longer available 
        for the player to take. Takes no parameters and does not return
        anything'''
        self.__taken = True
        self.image = pygame.image.load("frog0.png")
        self.rect.centerx = (128 * self.__row) + 22
        
    def get_taken(self):
        '''This method returns a boolean value depending if the goal is taken
        or not. Takes no parameters'''
        return self.__taken

            

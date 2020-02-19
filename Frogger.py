'''
Author: Ze Hao Su

Date: May 30, 2018

Description: This game is a copy of the original 1981 arcade game called Frogger. The
objective of the game is to guide the frog from the bottom of the screen to the top.
Along the way, there will be many obstacles suchs as the vehicles, river, logs and 
turtles. The player can control the frog using the "WASD" keys and each time the frog 
reaches his goal, some extra time will be alloted
'''

# Import and Initialize
import pygame, FroggerSprites, random
pygame.init()
pygame.mixer.init()

def main():
    #Display configuration
    screen = pygame.display.set_mode((576, 512))
    pygame.display.set_caption("Frogger!!!")
    
    #Entity
    background = pygame.image.load("Frogger3d.jpg")
    background.convert()
    screen.blit(background, (0,0))
    
    #Loads all the music and sound effects
    pygame.mixer.music.load("background_music.ogg")
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(-1)
    hop = pygame.mixer.Sound("hop.ogg")
    hop.set_volume(.6)     
    splash = pygame.mixer.Sound("splash.ogg")
    splash.set_volume(.6)  
    crash = pygame.mixer.Sound("crash.ogg")
    crash.set_volume(.6)    
    
    logs = []
    cars = []
    turtles = []
    goals = []
    
    #Creating sprites for player, lives keeper, time keeper, score keeper and background
    player = FroggerSprites.Player(screen)
    lives = FroggerSprites.Lives_keeper()
    timer = FroggerSprites.Time_keeper()
    score = FroggerSprites.Score_keeper()
    background_image = FroggerSprites.Background(screen)
    
    #Creating the sprites for logs, turtles, cars and end goals
    for row in range(5):
        #Only instantiate the logs if row is not even
        if not row % 2:
            log = FroggerSprites.Log(row, random.randrange(2, 5,2), screen)
            logs.append(log)
        #Only instantiate the turtles if row is not even
        else:
            turtle = FroggerSprites.Turtle(row, -random.randrange(2, 7,2),screen)
            turtles.append(turtle)            
        car = FroggerSprites.Car(row, random.randrange(2, 9,2),screen)
        cars.append(car)
        goal = FroggerSprites.Goal(row, screen)
        goals.append(goal)
    
    #Grouping all the sprites together
    turtle_group = pygame.sprite.Group(turtles)
    car_group = pygame.sprite.Group(cars)
    log_group = pygame.sprite.Group(logs)
    goal_group = pygame.sprite.Group(goals)
    middle_group = pygame.sprite.Group(log_group, car_group, turtle_group,
                                       goal_group)
    top_group = pygame.sprite.Group(player, lives, timer, score)
    all_sprites = pygame.sprite.OrderedUpdates(background_image, middle_group, top_group)
    
    #Action
    
        #Assign key variables
    clock = pygame.time.Clock()
    keep_going = True 
    counter = 0
    
        #Loop
    while keep_going:
        #Time
        clock.tick(30)
        
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
            elif event.type == pygame.KEYDOWN and not player.get_movement():        
                if event.key == pygame.K_a:
                    player.go_left()
                    hop.play()
                elif event.key == pygame.K_d:
                    player.go_right()
                    hop.play()
                elif event.key == pygame.K_w:
                    player.go_up() 
                    hop.play()
                elif event.key == pygame.K_s:
                    player.go_down()
                    hop.play()
        
        #Making variables to later check if player collided with any sprites
        collided_turtle = pygame.sprite.spritecollide(player, turtle_group, False)
        collided_log = pygame.sprite.spritecollide(player, log_group, False)
        collided_goal = pygame.sprite.spritecollide(player, goal_group, False)
        
        #If the player is on the water and is either on a log or a turtle, 
        #then the speed of the player increases based on the speed of log/turtle
        if player.get_above_water():
            if collided_log and collided_log[0].rect.centery == player.rect.centery:
                player.riding(collided_log[0].get_speed())
            elif collided_turtle and collided_turtle[0].rect.centery == player.rect.centery:
                player.riding(collided_turtle[0].get_speed())
            #If they are neither on a log nor a turtle, then the player is
            #sent back to the start and loses a life
            elif not collided_log and not collided_turtle:
                lives.lose_life()
                player_reset(player)
                splash.play()
        else:
            player.not_riding()
              
        #If the player reaches the end goal and the end goal is not taken then
        #the player wins, gets some extra time, is sent back to the start and
        #the end zone is then taken
        if pygame.sprite.spritecollide(player, goal_group, False) and not collided_goal[0].get_taken():
            score.win()
            player_reset(player)
            timer.increase_time()
            collided_goal[0].occupy()
        #If the player crashed with the car, he is sent back to the start 
        #and loses a life
        elif pygame.sprite.spritecollide(player, car_group, False): 
            lives.lose_life()
            player_reset(player)
            crash.play()
        
        #Spawn more cars, and turtles
        spawn(car_group, cars, FroggerSprites.Car, screen)
        spawn(turtle_group, turtles, FroggerSprites.Turtle, screen)
        
        #Groups those cars and turtles
        car_group = pygame.sprite.Group(cars)   
        turtle_group = pygame.sprite.Group(turtles)   
        
        #Add them to even more groups          
        middle_group = pygame.sprite.Group(log_group, car_group, turtle_group,
                                           goal_group)
        top_group = pygame.sprite.Group(player, lives, timer, score)
        all_sprites = pygame.sprite.OrderedUpdates(background_image, middle_group, top_group)        
        
        #timer
        counter += 1
        #For every second or 30 frame
        if not counter % 30:
            #Reduce the timer
            timer.count_down()
            
            #Give the turtles 1 in 5 chance to dive down
            for turtle_sprites in turtle_group:
                if random.randint(1,5) == 1 and turtle_sprites.get_state():
                    turtle_sprites.dived()
                #Animation for the turtle diving down
                turtle_sprites.change_image()
        
        #If time ran out, player ran out of lives, or there are no end goals left
        #Game over
        if lives.game_over() or timer.time_up() or not score.get_goals_left():
            keep_going = False
            
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        
        
    # One last blit to show the logo
    all_sprites.clear(screen, background)
    screen.blit(background, (0 , 0))
    pygame.display.flip() 
    pygame.mixer.music.fadeout(500)
    pygame.time.delay(500)
    pygame.quit()

                    
def spawn(group, list_name, class_name, screen):
    '''This function checks if any of the sprites in the sprite group reached
    halfway across the screen. If they did then it instantiate another sprite.
    This function takes 4 parameters which are a group, a list, a class name
    and a screen. This does not return anything'''
    for sprites in group:
        if sprites.rect.left == screen.get_width()/2:
            list_name.append(class_name(sprites.get_row(), sprites.get_speed(),screen)) 

def player_reset(player):
    """This function makes the player reset the their position. It takes the 
    player as the parameter and does not return anything"""
    player.reset_position()
    player.reset_movement()
    player.not_riding()    
main()
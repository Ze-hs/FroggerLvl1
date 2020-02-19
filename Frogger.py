#Idea
import pygame, FroggerSprites, random
pygame.init()
def main():
    #Display configuration
    screen = pygame.display.set_mode((576, 512))
    pygame.display.set_caption("Frogger!!!")
    
    #Entity
    background = pygame.Surface((screen.get_size()))
    background = pygame.image.load("background.jpg")
    background.convert()
    #background.fill((255, 255, 255))
    screen.blit(background, (0,0))    
    
    logs = []
    cars = []
    turtles = []
    goals = []
    grid = FroggerSprites.Grid(screen, background)
    player = FroggerSprites.Player(screen)
    lives = FroggerSprites.Lives_keeper()
    timer = FroggerSprites.Time_keeper()
    score = FroggerSprites.Score_keeper()
    for row in range(5):
        if not row % 2:
            log = FroggerSprites.Log(row, screen)
            logs.append(log)
        else:
            turtle = FroggerSprites.Turtle(row, screen)
            turtles.append(turtle)            
        car = FroggerSprites.Car(row, random.randint(2, 6),screen)
        cars.append(car)
        goal = FroggerSprites.Goal(row, screen)
        goals.append(goal)
    
    
    turtle_group = pygame.sprite.Group(turtles)
    car_group = pygame.sprite.Group(cars)
    log_group = pygame.sprite.Group(logs)
    goal_group = pygame.sprite.Group(goals)
    all_sprites = pygame.sprite.OrderedUpdates(log_group, car_group, turtle_group,
                                               goal_group, player, lives, timer, score )
    
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
                elif event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_w:
                    player.go_up()                
                elif event.key == pygame.K_s:
                    player.go_down()      
        
        
              
        collided_turtle = pygame.sprite.spritecollide(player, turtle_group, False)
        collided_log = pygame.sprite.spritecollide(player, log_group, False)
        collided_goal = pygame.sprite.spritecollide(player, goal_group, False)
        if player.get_above_water() and collided_log:
            if collided_log[0].rect.centery == player.rect.centery:
                player.riding(collided_log[0].get_speed())
            else:
                player.not_riding()
        elif player.get_above_water() and collided_turtle:
            if collided_turtle[0].rect.centery == player.rect.centery:
                player.riding(collided_turtle[0].get_speed())
            else:
                player.not_riding()
                
        if (player.get_above_water() and not collided_log and not collided_turtle)\
           or pygame.sprite.spritecollide(player, car_group, False): 
            lives.lose_life()
            player.reset_position()
            player.reset_movement()
            player.not_riding()
            
        if pygame.sprite.spritecollide(player, goal_group, False):
            score.win()
            player.reset_position()
            player.reset_movement()
            player.not_riding() 
            if not collided_goal[0].get_taken():
                collided_goal[0].occupy()
        for sprites in car_group:
            if sprites.rect.left == screen.get_width()/3:
                cars.append(FroggerSprites.Car(sprites.get_row(), sprites.get_speed(),screen))
                car_group = pygame.sprite.Group(cars)
                all_sprites = pygame.sprite.OrderedUpdates(log_group, car_group, turtle_group,
                                                           goal_group, player, lives, timer, score )          
          
        #timer
        counter += 1
        if not counter % 30:
            timer.count_down()
            for turtle_sprites in turtle_group:
                if random.randint(1,3) == 1 and turtle_sprites.get_state():
                    turtle_sprites.dived()
                turtle_sprites.change_image()
        
        if lives.game_over() or timer.time_up() or not score.get_goals_left():
            keep_going = False
            
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
main()
                    

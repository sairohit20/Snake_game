# -*- coding: utf-8 -*-
"""
Created on Sun May 16 09:55:32 2021

@author: src20
"""

from flask import Flask
import pygame
from pygame.locals import *
import random
app = Flask(__name__)

@app.route('/')
def hello_python():
    cell_size=10
    direction=1 #1 is up 2 is right 3 is down 4 is left
    update_snake=0
    food=[0,0]
    new_food=True
    new_piece=[0,0]
    score=0
    font=pygame.font.SysFont(None,40)
    game_over=False
    clicked=False
    #creating snake
    snake_pos=[[int(screen_width/2),int(screen_height/2)]]
    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size])
    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size*2])
    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size]*3)
    
    
    #for colours
    bg=(0,0,0)
    body=(255, 255, 255)
    blue=(0,0,128)
    food_colour= (255, 255, 0)
    green=(0, 255, 0)
    
    
    #setting up rectangle for play again
    again_rect=Rect(screen_width//2-100,screen_height//2,210,50)
    
    
    def draw_screen():
        screen.fill(bg)
    
    def write_score():
        score_text="SCORE: "+str(score)
        score_img=font.render(score_text,True,green)
        screen.blit(score_img,(0,0))
    
    def check_gameover(game_over):
        head_count=0
        #to check if snake crashed itself
        for segment in snake_pos:
            if snake_pos[0]==segment and head_count>0:
                game_over=True
            head_count+=1
        #to check if snake went out of scrren
        if snake_pos[0][0]<0 or snake_pos[0][0]>screen_width or snake_pos[0][1]<0 or snake_pos[0][1]>screen_height:
            game_over=True
        return game_over
    
    
    def draw_gameover():   
        
        game_over="GAME OVER!!!"
        game_over_img=font.render(game_over,True,food_colour)
        screen.blit(game_over_img,(screen_width//2-100,screen_height//2-50))
        
        play_again="PLAY AGAIN??"
        play_again_img=font.render(play_again,True,bg)
        pygame.draw.rect(screen,food_colour,again_rect)
        screen.blit(play_again_img,(screen_width//2-100,screen_height//2+10))
        
    
    #vreating loop to run the game
    run=True 
    while run:
        
        draw_screen()
        write_score()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP and direction!=3:
                    direction=1
                elif event.key==pygame.K_RIGHT and direction!=4:
                    direction=2
                elif event.key==pygame.K_DOWN and direction!=1:
                    direction=3
                elif event.key==pygame.K_LEFT and direction!=2:
                    direction=4
    
    #creating food               
        if new_food ==True:
            new_food = False
            food[0]=cell_size*random.randint(0,(screen_width/cell_size)-1)
            food[1]=cell_size*random.randint(0,(screen_height/cell_size)-1)
            
    #drawing food
        pygame.draw.rect(screen,food_colour,(food[0],food[1],cell_size,cell_size))
        
    #eating of food
        if snake_pos[0]==food:
            new_food=True
            new_piece=list(snake_pos[-1])
            if direction==1:
                new_piece[1]+=cell_size
            elif direction==3:
                new_piece[1]-=cell_size
            elif direction==2:
                new_piece[0]-=cell_size
            elif direction==4:
                new_piece[0]+=cell_size
            snake_pos.append(new_piece)  #adding new piece to snake
            score+=1  #increasing score
        if game_over==False:
            if update_snake>99:
                update_snake=0
                snake_pos=snake_pos[-1:]+snake_pos[:-1]
                if direction==1:
                    snake_pos[0][0]=snake_pos[1][0]
                    snake_pos[0][1]=snake_pos[1][1]-cell_size
                if direction==3:
                    snake_pos[0][0]=snake_pos[1][0]
                    snake_pos[0][1]=snake_pos[1][1]+cell_size
                if direction==2:
                    snake_pos[0][1]=snake_pos[1][1]
                    snake_pos[0][0]=snake_pos[1][0]+cell_size
                if direction==4:
                    snake_pos[0][1]=snake_pos[1][1]
                    snake_pos[0][0]=snake_pos[1][0]-cell_size
                game_over=check_gameover(game_over)
                
        if game_over==True:
            draw_gameover()
            if event.type==pygame.MOUSEBUTTONDOWN and clicked==False:
                clicked=True
            if event.type==pygame.MOUSEBUTTONUP and clicked==True:
                clicked=False
                pos=pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    #reset variables
                    cell_size=10
                    direction=1 #1 is up 2 is right 3 is down 4 is left
                    update_snake=0
                    food=[0,0]
                    new_food=True
                    new_piece=[0,0]
                    score=0
                    game_over=False
                    #creating snake
                    snake_pos=[[int(screen_width/2),int(screen_height/2)]]
                    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size])
                    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size*2])
                    snake_pos.append([int(screen_width/2),int(screen_height/2)+cell_size]*3)
                
        
        #creating snake on screen
        head=1
        for x in snake_pos:
            if head==0:
                pygame.draw.rect(screen,body,(x[0],x[1],cell_size,cell_size))
                pygame.draw.rect(screen,body,(x[0]+1,x[1]+1,cell_size-2,cell_size-2))
            if head==1:
                pygame.draw.rect(screen,body,(x[0],x[1],cell_size,cell_size))
                pygame.draw.rect(screen,blue,(x[0]+1,x[1]+1,cell_size-2,cell_size-2))
                head=0
                        
        #to update display
        pygame.display.update()
        update_snake+=1
                
    pygame.quit()

if __name__ == '__main__':
   app.run()
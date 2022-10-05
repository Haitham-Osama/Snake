from tkinter import *
from PIL import Image,ImageTk
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
BACKGROUND_COLOR = '#0F0F0F'


class Snake:
    
    def __init__(self) -> None:
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])
            
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag='snake')
            self.squares.append(square)


class Food:
    
    def __init__(self) -> None:
        x= random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE ### (* SPACE_SIZE) to convert to pixels, (* the size of each item in the game )
        y= random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE ###(GAME_HEIGHT/SPACE_SIZE) spots possible to add food on (14x14)
        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOR,tag='food')# x,y starting corner, +SPACE_SIZE ending corner


def start():
    global score,SPEED
    SPEED,score = 150,0
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake,food)


def next_turn(snake,food):
    x,y = snake.coordinates[0]
    
    if direction == 'up':
        y-=SPACE_SIZE  #to move one space up
    elif direction == 'down':
        y+=SPACE_SIZE  #to move one space down 
    elif direction == 'left':
        x-=SPACE_SIZE  #to move one space left
    elif direction == 'right':
        x+=SPACE_SIZE  #to move one space right
        
    snake.coordinates.insert(0,(x,y))
    
    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR)
    snake.squares.insert(0,square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score,SPEED
        score+=1
        if SPEED > 50: SPEED-=5
        label.config(text='Score:{}'.format(score))
        
        canvas.delete('food')
        food = Food() # to create another food object
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collision(snake):
        game_over()
    else:window.after(SPEED,next_turn,snake,food) #snake and food are the args for next_turn function
    
    
def change_direction(new_direction):
    
    global direction
    ###(and direction != 'left') so it doesn't make a 180
    if new_direction == 'left' and direction != 'right':direction = new_direction
    elif new_direction == 'right' and direction != 'left':direction = new_direction
    elif new_direction == 'up' and direction != 'down':direction = new_direction
    elif new_direction == 'down' and direction != 'up':direction = new_direction
    

def check_collision(snake):
    x,y= snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:return True  ### game over
    elif y < 0 or y >= GAME_HEIGHT:return True  ### game over
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:return True  ### game over (if the head is touching any of the body parts)
    
    return False
    
    
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
                       font=('Minecraft',70,'bold'),text='GAME OVER',fill='red',tag='gameover')
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2+60,
                       font=('Minecraft',20,),text='Press any key to restart',fill='red',tag='restart')

    
window = Tk()
iconImage = Image.open("logo.png")
icon = ImageTk.PhotoImage(iconImage)
window.config(bg='white'),window.title("SNAKE"),window.iconphoto(True,icon)
window.resizable(False,False)



score = 0
direction = 'down'

label = Label(window,text = "Score:{}".format(score),font=('Minecraft',40),pady=5,bg='white')
label.pack()

canvas = Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

# launch in the middle
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x=int((screen_width/2) - (window_width/2))
y=int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>',lambda event:change_direction('left'))
window.bind('<Right>',lambda event:change_direction('right'))
window.bind('<Up>',lambda event:change_direction('up'))
window.bind('<Down>',lambda event:change_direction('down'))

canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
                   font=('Minecraft',35,'bold'),text='PRESS ANY KEY TO START',fill='red',tag='start')
window.bind('<Return>',lambda event:start())

window.mainloop()
import turtle
import time
import random
import os
import pygame
from pygame import mixer

# Initialize pygame mixer
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("eat.wav") 
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Delay for controlling the game speed
delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by @Adhish Nidhi Tiwari")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Function to save high score to a file
def save_high_score():
    with open("high_score.txt", "w") as file:
        file.write((high_score))

# Function to load high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Initialize the high score from the file
high_score = load_high_score()

# Main menu
menu = turtle.Turtle()
menu.speed(0)
menu.color("white")
menu.penup()
menu.hideturtle()
menu.goto(0, 50)
menu.write("Snake Game", align="center", font=("Courier", 36, "bold"))
menu.goto(0, -30)
menu.write("Press 'Space' to Start", align="center", font=("Courier", 24))
menu.goto(0, -60)
menu.write("Press 'Q' to Quit", align="center", font=("Courier", 24))
menu.goto(0, -90)
menu.write("High Score: {}".format(high_score), align="center", font=("Courier", 18))

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: {}".format(high_score), align="center", font=("Courier", 24, "normal"))

# Function to go up
def go_up():
    if head.direction != "down":
        head.direction = "up"

# Function to go down
def go_down():
    if head.direction != "up":
        head.direction = "down"

# Function to go left
def go_left():
    if head.direction != "right":
        head.direction = "left"

# Function to go right
def go_right():
    if head.direction != "left":
        head.direction = "right"

# Function to move the snake
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Function to start the game
def start_game():
    global game_started
    game_started = True
    menu.clear()

# Function to quit the game
def quit_game():
    global game_over
    game_over = True

# Function to update the high score and save it
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score()  # Save the high score immediately
        # Also, update the high score displayed in the menu
        menu.clear()
        menu.goto(0, -90)
        menu.write("High Score: {}".format(high_score), align="center", font=("Courier", 18))

# Initialize game states
game_started = False
game_over = False

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(start_game, "space")
wn.onkeypress(quit_game, "q")

# Main game loop
while not game_over:
    wn.update()

    if not game_started:
        continue

    # Check for a collision with the border
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        # Play the game over sound effect
        game_over_sound.play()
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Play the eat sound effect
        eat_sound.play()

        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            # Play the game over sound effect
            
            game_over_sound.play()
            
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1
        
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Check for a new high score and update it
    update_high_score()

    time.sleep(delay)

wn.bye()
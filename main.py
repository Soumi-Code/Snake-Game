import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.title("SNAKE GAME")
screen.setup(width=700, height=700)
screen.tracer(0)
screen.bgcolor("#1d1d1d")

# Border creation
border = turtle.Turtle()
border.speed(5)
border.pensize(4)
border.penup()
border.goto(-300, 250)
border.pendown()
border.color("red")
border.forward(600)  # Top border
border.right(90)
border.forward(500)  # Right border
border.right(90)
border.forward(600)  # Bottom border
border.right(90)
border.forward(500)  # Left border
border.penup()
border.hideturtle()

# Game variables
score = 0
high_score = 0
delay = 0.1
SNAKE_SIZE = 20
game_running = True

# Snake setup
snake = turtle.Turtle()
snake.speed(0)
snake.shape("square")
snake.color("green")
snake.penup()
snake.goto(0, 0)
snake.direction = 'stop'

# Food setup
fruit = turtle.Turtle()
fruit.speed(0)
fruit.shape("square")
fruit.color("white")
fruit.penup()
fruit.goto(30, 30)

# Snake body segments
body_segments = []

# Scoring display
scoring = turtle.Turtle()
scoring.speed(0)
scoring.color("white")
scoring.penup()
scoring.hideturtle()
scoring.goto(0, 300)
scoring.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "bold"))

# Snake movement functions
def snake_go_up():
    if snake.direction != "down":
        snake.direction = "up"

def snake_go_down():
    if snake.direction != "up":
        snake.direction = "down"

def snake_go_left():
    if snake.direction != "right":
        snake.direction = "left"

def snake_go_right():
    if snake.direction != "left":
        snake.direction = "right"

# Move snake in the current direction
def snake_move():
    if snake.direction == "up":
        snake.sety(snake.ycor() + SNAKE_SIZE)
    if snake.direction == "down":
        snake.sety(snake.ycor() - SNAKE_SIZE)
    if snake.direction == "left":
        snake.setx(snake.xcor() - SNAKE_SIZE)
    if snake.direction == "right":
        snake.setx(snake.xcor() + SNAKE_SIZE)

# Reset the game
def reset_game():
    global score, delay, game_running
    time.sleep(1)
    snake.goto(0, 0)
    snake.direction = "stop"
    for segment in body_segments:
        segment.hideturtle()
    body_segments.clear()
    fruit.goto(random.randint(-290, 270), random.randint(-240, 240))
    score = 0
    delay = 0.1
    game_running = True
    update_score_display()

# End game
def game_over():
    global high_score, game_running
    if score > high_score:
        high_score = score
    scoring.clear()
    scoring.goto(0, 0)
    scoring.write("GAME OVER\nScore: {}  High Score: {}\nPress 'r' to Restart".format(score, high_score), align="center", font=("Courier", 30, "bold"))
    game_running = False

# Update score display
def update_score_display():
    scoring.clear()
    scoring.goto(0, 300)
    scoring.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "bold"))

# Keyboard binding
screen.listen()
screen.onkeypress(snake_go_up, "Up")
screen.onkeypress(snake_go_down, "Down")
screen.onkeypress(snake_go_left, "Left")
screen.onkeypress(snake_go_right, "Right")
screen.onkeypress(reset_game, "r")

# Game loop
try:
    while True:
        screen.update()

        if game_running:
            # Border collision detection (adjusted to align with visible red border)
            if (snake.xcor() >= 290 - SNAKE_SIZE / 2 or snake.xcor() <= -290 + SNAKE_SIZE / 2 or 
                snake.ycor() >= 240 - SNAKE_SIZE / 2 or snake.ycor() <= -240 + SNAKE_SIZE / 2):
                game_over()
                continue
            
            # Move the snake
            snake_move()

            # Food collision detection
            if snake.distance(fruit) < SNAKE_SIZE:
                fruit.goto(random.randint(-290, 270), random.randint(-240, 240))
                score += 1
                delay -= 0.001
                update_score_display()

                # Add new segment to snake's body
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("red")
                new_segment.penup()
                body_segments.append(new_segment)

            # Move body segments
            for i in range(len(body_segments) - 1, 0, -1):
                body_segments[i].goto(body_segments[i - 1].xcor(), body_segments[i - 1].ycor())
            if body_segments:
                body_segments[0].goto(snake.xcor(), snake.ycor())

            # Self-collision detection
            for segment in body_segments[1:]:
                if segment.distance(snake) < SNAKE_SIZE:
                    game_over()
                    break

            time.sleep(delay)
except turtle.Terminator:
    print("Turtle graphics window closed.")

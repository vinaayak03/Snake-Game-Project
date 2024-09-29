from tkinter import *
import random

# Constants for the game window, snake speed, and appearance
GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 75  # Speed of the game (lower values mean faster)
SPACE_SIZE = 65  # Size of each grid cell
BODY_PARTS = 1  # Initial number of snake body parts
SNAKE_COLOUR = "#110F0A"  # Snake color
FOOD_COLOUR = "#AE9076"  # Food color
BACKGROUND_COLOUR = "#342C1D"  # Background color

# Snake class defines the behavior and appearance of the snake
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS  # Number of body parts
        self.coordinates = []  # Coordinates of each body part
        self.squares = []  # List to keep track of each body part's graphical square

        # Initialize snake's body at (0, 0) on the canvas
        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create a rectangle for each body part (currently just 1)
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)

# Food class defines the behavior and appearance of the food
class Food:
    def __init__(self):
        # Randomly place food in one of the grid cells
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]  # Store food's coordinates

        # Create a graphical oval representing the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")

# Function to handle the logic for each turn (moving the snake)
def next_turn(snake, food):
    
    # Get the current coordinates of the snake's head
    x, y = snake.coordinates[0]
    
    # Move the snake in the direction set by the user
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert the new coordinates for the snake's head
    snake.coordinates.insert(0, (x, y))

    # Create a new rectangle for the new head position
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1  # Increase score
        label.config(text="Score:{}".format(score))  # Update the score label
        canvas.delete("food")  # Remove the old food
        food = Food()  # Create new food
    else:
        # If no food is eaten, remove the tail of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions (with walls or the snake itself)
    if check_collisions(snake):
        game_over()  # End the game if a collision occurs
    else:
        # Continue the game with the next turn
        window.after(SPEED, next_turn, snake, food)

# Function to change the direction of the snake based on user input
def change_direction(new_direction):
    global direction

    # Prevent the snake from moving in the opposite direction (i.e., no 180-degree turns)
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Function to check for collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]  # Get the head's coordinates

    # Check if the snake hits the wall
    if x < 0 or x >= GAME_WIDTH: 
        return True
    elif y < 0 or y >= GAME_HEIGHT: 
        return True

    # Check if the snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

# Function to end the game and display "GAME OVER"
def game_over():
    canvas.delete(ALL)  # Clear the canvas
    # Display the game over text
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("arial", 70), text="GAME OVER", fill="white", tag="gameover")

# Main window setup
window = Tk()
window.title("Snake Eater")
window.resizable(False, False)

# Initialize the score and direction
score = 0
direction = "down"

# Score label
label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

# Canvas where the game is drawn
canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Update window to get its correct dimensions
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind the arrow keys to change the direction of the snake
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Right>", lambda event: change_direction("right"))

# Create the snake and food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Start the Tkinter event loop
window.mainloop()

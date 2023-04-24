#  SPACE MOVER

#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.


# Import standard Python modules needed to complete this assignment.
# You MUST not use any other modules for your solution.
from turtle import *
from math import *
from random import *
from random import randint, choice
from sys import exit as abort
from os.path import isfile

# Define constant values used in the main program that sets up
# the drawing canvas.  Do not change any of these values unless instructed.
# cell size in pixels (default is 100)
cell_size = 100
# number of cells across the width of grid (default is 8)
grid_width = 7 # was 8 
# number of cells up the length of grid (default is 5)
grid_height = 7
# size of the margin left/right of the grid (pixels)
x_margin = cell_size * 2 
# size of the margin below/above the grid (pixels)
y_margin = cell_size
window_height = grid_height * cell_size + y_margin * 2
window_width = grid_width * cell_size + x_margin * 2.5
# font for the cell coords
small_font = ('Arial', cell_size // 5, 'normal') 
# font for any other text
big_font = ('Arial', cell_size // 4, 'normal') 

# Validity checks on grid size - do not change this code
assert cell_size >= 80, 'Cells must be at least 80x80 pixels in size'
assert grid_width >= 7, 'Grid must be at least 7 squares wide'
assert (grid_height >= 5) and (grid_height % 2 != 0), \
       'Grid must be at least 5 squares high and height must be odd'

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# manage the drawing canvas for your image.

# Set up the canvas and draw the background for the overall image
def create_drawing_canvas(bg_colour = 'light grey',
                          line_colour = 'slate grey',
                          draw_grid = True,
                          label_spaces = True): # NO! DON'T CHANGE THIS!
    
    # Set up the drawing canvas with enough space for the grid and
    # spaces on either side
    setup(window_width, window_height)
    bgcolor(bg_colour)

    # Draw as quickly as possible
    tracer(False)

    # Get ready to draw the grid
    penup()
    color(line_colour)
    width(2)

    # Determine the left-bottom coords of the grid
    left_edge = -(grid_width * cell_size) // 2 
    bottom_edge = -(grid_height * cell_size) // 2

    # Optionally draw the grid
    if draw_grid:

        # Draw the horizontal grid lines
        setheading(0) # face east
        for line_no in range(0, grid_height + 1):
            penup()
            goto(left_edge, bottom_edge + line_no * cell_size)
            pendown()
            forward(grid_width * cell_size)
            
        # Draw the vertical grid lines
        setheading(90) # face north
        for line_no in range(0, grid_width + 1):
            penup()
            goto(left_edge + line_no * cell_size, bottom_edge)
            pendown()
            forward(grid_height * cell_size)

        # Draw each of the labels on the x axis
        penup()
        y_offset = cell_size // 3 # pixels
        for x_label in range(0, grid_width):
            goto(left_edge + (x_label * cell_size) + (cell_size // 2),
                 bottom_edge - y_offset)
            write(str(x_label + 1), align = 'right', font = small_font)

        # Draw each of the labels on the y axis
        penup()
        x_offset, y_offset = cell_size // 5, cell_size // 10 # pixels
        for y_label in range(0, grid_height):
            goto(left_edge - x_offset, bottom_edge + (y_label * cell_size) +
                 (cell_size // 2) - y_offset)
            write(chr(y_label + ord("A")), align = 'center', font = small_font)

        # Mark the "special" cell
        goto(-cell_size * grid_width // 2 + 0.5 * cell_size, 0)
        dot(cell_size // 6)
        goto(cell_size * grid_width // 2 - 0.5 * cell_size, 0)

    # Optionally mark the blank spaces ... NO! YOU CAN'T CHANGE ANY OF THIS CODE!
    if label_spaces:
        # Left side
        goto(-((grid_width + 1) * cell_size) // 2, -(cell_size // 2))
        write('Draw your\nsymbol \nhere', align = 'right', font = big_font)    
        # Right side
        goto(((grid_width + 1) * cell_size) // 2, -(cell_size // 2))
        write('Draw the\ncounter\nhere', align = 'left', font = big_font)

    
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)

# End the program and release the drawing canvas to the operating
# system.  By default the cursor (turtle) is hidden when the
# program ends.  Call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any drawing still in progress is displayed
    if hide_cursor:
        hideturtle()
    done()

##############################    
def actions(new_seed = None):
    seed(new_seed)
    return symbol_actions(grid_width, grid_height)

#--------------------------------------------------------------------#
def symbol_actions(width = 1, height = 1):

    # Define the ways the entities can move around the grid
    directions = ['East', 'West', 'North', 'South']
    
    # Choose the total number of entity actions
    num_actions = randint(0, 20)

    # Create the data set
    actions_list = []

    # Create the individual steps
    for step in range(0, num_actions):
        # Choose which way the entity wants to move
        direction = choice(directions)

        # Choose the number of cells the entity wants to move
        # (ignoring the limitations on their ability to do so)
        if direction in ['North', 'South']:
            num_cells = randint(1, height // 3)
        else:
            num_cells = randint(1, width // 2)
        # Add the chosen action to the data set
        actions_list.append([num_cells, direction])

    # Print the whole data set to the shell window, laid out
    # so that it's easy to distinguish the actions attempted by
    # the entity
    print('The entity actions to visualise are as follows:\n')
    print(str(actions_list).replace(', [', ', \n ['))
    # Return the data set to the caller
    return actions_list

def start_moving(data_set):
    
    perimeter_count = 1
    move_count = 1
    speed(0)
    
    #Function to display how many time panda touch perimeter
    def display_perimeter_count():
        up()
        goto(425, 0)
        down()
        color("black")
        write(f" count: {perimeter_count}", font=("Arial", 12, "normal"))
    
    #Function to display how many time panda move
    def display_move_count():
        nonlocal move_count
        up()
        goto(xcor() + 30, ycor() - 50)
        down()
        
        write(move_count, font=("Arial", 16, "normal"))
    #Function to draw a ring for panda
    def ring(col, rad):
        fillcolor(col)
        begin_fill()
        circle(rad)
        end_fill()
    # Function to draw a square

    def draw_square(size):
        fillcolor("blue")
        begin_fill()
        
            
        down()
        pencolor('black')
        for i in range(4):
            forward(size)
            right(90)
        end_fill()
    # Function to draw a count square
    def square_count(size):
        up()
        goto(500, 50)
        fillcolor("sky blue")
        begin_fill()
        
        down()
        pencolor('black')
        for i in range(4):
            forward(size)
            right(90)
        end_fill()
        #display_move_count()
        display_perimeter_count()

    #write the sentence "Perimeter count"    
    up()
    goto(425,-100)
    down()
    color("black")
    write("Perimeter \n count", font=("Arial", 16, "normal"))
    up()    
            
               
    # Scale down factor for the panda
    scale = 0.8
    #Function to draw a panda out of the grid and it's place
    up()
    goto(-510,50)

    def panda():

        draw_square(100)

        # Adjust pen size 
        pensize(2)

##### Draw ears #####
        # Draw first ear
        up()
        goto(xcor() + 35*scale, ycor() - 40*scale )
        
        down()
        ring('black', 15*scale)

        # Draw second ear
        up()
        goto(xcor() + 60*scale,ycor() )
        
        down()
        ring('black', 15*scale)

##### Draw face #####
        up()
        goto(xcor()-30*scale, ycor() - 55*scale)
        
        down()
        ring('white', 40*scale)

##### Draw eyes black #####

        # Draw first eye
        up()
        goto(xcor() -18*scale,ycor() + 40*scale)
        
        down()
        ring('black', 8*scale)

        # Draw second eye
        up()
        goto(xcor() + 35*scale, ycor())
        
        down()
        ring('black', 8*scale)

##### Draw eyes white #####

        # Draw first eye
        up()
        goto(xcor()-35 * scale, ycor()+3 * scale)
        
        down()
        ring('white', 4*scale)

        # Draw second eye
        up()
        goto(xcor()+35 * scale, ycor())
        
        down()
        ring('white', 4*scale)

        # Draw nose 
        up()
        goto(xcor()-18 * scale, ycor()-16*scale)
        
        down()
        ring('black', 5*scale)

        # Draw mouth 
        up()
        goto(xcor(),ycor() )
        
        down()
        right(90)
        circle(5*scale, 180)
        up()
        goto(xcor()-10*scale,ycor())
        
        down()
        left(360)
        circle(5*scale, -180)
        up()
        goto(-475,-75)
        write("panda",font=("Arial", 16, "normal"))


    # call panda function    
    panda()
    square_count(100)
    
  
    

#Function to draw a panda which is movable
    def panda_draw(x,y):

        up()
        home()
        goto(-350 + x,50 + y)
   
    ##### Draw square #####
        draw_square(100)

# Adjust pen size
        pensize(2)

##### Draw ears #####
# Draw first ear
        up()
        goto(xcor() + 35*scale, ycor() - 40*scale )
            
        down()
        ring('black', 15*scale)

# Draw second ear
        up()
        goto(xcor() + 60*scale,ycor() )
            
        down()
        ring('black', 15*scale)

##### Draw face #####
        up()
        goto(xcor()-30*scale, ycor() - 55*scale)
            
        down()
        ring('white', 40*scale)

##### Draw eyes black #####

# Draw first eye
        up()
        goto(xcor() -18*scale,ycor() + 40*scale)
            
        down()
        ring('black', 8*scale)

# Draw second eye
        up()
        goto(xcor() + 35*scale, ycor())
            
        down()
        ring('black', 8*scale)

##### Draw eyes white #####

# Draw first eye
        up()
        goto(xcor()-35 * scale, ycor()+3 * scale)
            
        down()
        ring('white', 4*scale)

# Draw second eye
        up()
        goto(xcor()+35 * scale, ycor())
            
        down()
        ring('white', 4*scale)
 
##### Draw nose #####
        up()
        goto(xcor()-18 * scale, ycor()-16*scale)
            
        down()
        ring('black', 5*scale)

##### Draw mouth #####
        up()
        goto(xcor(),ycor() )
            
        down()
        right(90)
        circle(5*scale, 180)
        up()
        goto(xcor()-10*scale,ycor())
            
        down()
        left(360)
        circle(5*scale, -180)
        display_move_count()
# call panda Function to put panda on the initial position
    panda_draw(0,0)
# Function that write "panda has finished"
    def write_warning():
        up()
        goto(150,350)
        color("red")
        down()
        write("On the edge",font=("Arial", 32, "normal"))
        up()
# Function that write "On the edge"  
    def write_finish():
        up()
        goto(150,350)
        color("black")
        down()
        write("panda has finished",font=("Arial", 32, "normal"))
        up()
    
    def move_panda(directions):
        x, y = 0, 0  # starting position
        #Use nonlocal so that I can use these variable in the function
        nonlocal perimeter_count 
        nonlocal move_count
       
        for distance, direction_str in directions:
            
            for i in range(distance):
                new_x, new_y = x, y
                if direction_str == 'East':
                    new_x += 100
                elif direction_str == 'West':
                    new_x -= 100
                elif direction_str == 'North':
                    new_y += 100
                else:
                    new_y -= 100

            # Check if new position is within bounds
                if 0 <= new_x <= 600 and -300 <= new_y <= 300:
                    x, y = new_x, new_y
                    move_count += 1    
                    if x == 0 or x == 600 or y == -300 or y == 300:
                       
                       perimeter_count += 1
                       square_count(100)

                       
                else:
                    square_count(100)
                    break 
                if perimeter_count == 10:
                    return write_warning()
                
                panda_draw(x, y)

        return write_finish()         

            
    move_panda(data_set)
    
  
    hideturtle()


#
#--------------------------------------------------------------------#



#-----Main Program to Create Drawing Canvas--------------------------#
#
# This main program sets up the canvas, ready for you to start
# drawing your solution.  Do NOT change any of this code except
# as indicated by the comments marked '*****'.  Do NOT put any of
# your solution code in this area.
#

# Set up the drawing canvas
# ***** You can change the background and line colours, and choose
# ***** whether or not to draw the grid and other elements, by
# ***** providing arguments to this function call
create_drawing_canvas("green","red",True,False)

# Control the drawing speed
speed('fastest')

# Decide whether or not to show the drawing being done step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** forever while the cursor moves slooooowly around the screen
tracer(True)


title("Panda March")


start_moving(actions(8)) 
 
# Exit gracefully
release_drawing_canvas()

#
#--------------------------------------------------------------------#

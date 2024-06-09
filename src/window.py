from tkinter import Tk, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.__root = Tk()                                          # Initiate a root window
        self.__root.geometry(f"{width}x{height}")                   # Set the root window's width and height
        self.__root.title("Maze solver")                            # Set the root window's title
        self.__root.protocol("WM_DELETE_WINDOW", self.close)        # Connect self.close to the "delete window" action
        self.canvas = Canvas(self.__root, width=width, height=height, borderwidth=0, highlightthickness=0)              # Create a widget for drawing graphics (borders are part of the coordinate space, so remove them to see the outer lines)
        self.canvas.pack()                                          # Pack the widget into the root window
        self.__running = False                                      # Define the app's running state
        self._width = width
        self._height = height

    def redraw(self):
        self.__root.update_idletasks()                            # Process all pending idle tasks, without processing any other events
        self.__root.update()                                      # Process all pending events, call event callbacks, complete any pending geometry management, redraw widgets as necessary, and call all pending idle tasks

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)                          # Draw a line in root's canvas

    def __repr__(self):
        return f"Window size - width:{self._width}px, height:{self._height}px."

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point (x: {self.x}, y: {self.y})"


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.line_id = None                                 # line_id is used to specify Line ids for Line deletions

    def draw(self, canvas, fill_color):
        self.line_id = canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

    def __repr__(self):
        return f"Line from point1({self.point1.x}, {self.point1.y}) to point2({self.point2.x}, {self.point2.y})"
    

class Cell:
    def __init__(self, starting_point, ending_point, window):
        # Define Cell points between walls
        self._top_left = Point(starting_point.x, starting_point.y)
        self._top_right = Point(ending_point.x, starting_point.y)
        self._bottom_left = Point(starting_point.x, ending_point.y)
        self._botom_right = Point(ending_point.x, ending_point.y)

        # Define the Cell's center - to be used when drawing paths between Cells
        self._center = Point(((ending_point.x - starting_point.x) // 2) + starting_point.x, ((ending_point.y - starting_point.y) // 2) + starting_point.y)

        self._left_wall = Line(self._top_left, self._bottom_left)
        self._right_wall = Line(self._top_right, self._botom_right)
        self._top_wall = Line(self._top_left, self._top_right)
        self._bottom_wall = Line(self._bottom_left, self._botom_right)

        self.window = window
        self.__canvas = self.window.canvas        
        
        # Define the wall states - will be False after breaking them
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

    def draw(self):
        # Draw a black wall on the Cell's canvas - takes in a wall parameter, all are drawn on initiation 
        draw_wall_lambda = lambda wall: wall.draw(self.__canvas, "black")               

        if self.left_wall:
            draw_wall_lambda(self._left_wall)
        if self.right_wall:
            draw_wall_lambda(self._right_wall)
        if self.top_wall:
            draw_wall_lambda(self._top_wall)
        if self.bottom_wall:
            draw_wall_lambda(self._bottom_wall)

    def break_wall(self, *args):
        # Break down a wall on the Cell's canvas - takes in a wall parameter, line_id from the line's canvas.create method is used (automated)
        break_wall_lambda = lambda wall: self.__canvas.delete(wall.line_id)

        for arg in args:
            if arg == "left" and self.left_wall:
                self.left_wall = False
                break_wall_lambda(self._left_wall)
            elif arg == "right" and self.right_wall:
                self.right_wall = False
                break_wall_lambda(self._right_wall)
            elif arg == "top" and self.top_wall:
                self.top_wall = False
                break_wall_lambda(self._top_wall)
            elif arg == "bottom" and self.bottom_wall:
                self.bottom_wall = False
                break_wall_lambda(self._bottom_wall)
            else:
                raise Exception("Invalid argument or wall already broken. Arguments can be 'left', 'right', 'top' and/or 'bottom'.")
            
    def draw_move(self, to_cell, undo=False):
        if type(to_cell) != Cell:
            raise TypeError("Please provide a valid cell destination to move to.")

        if undo == False:
            self._move_color = "red"
        else:
            self._move_color = "gray"

        # Create a path from this cell to one applied as a parameter (to_cell)
        self.move_to_cell_id = Line(self._center, to_cell._center).draw(self.__canvas, self._move_color)

    
    def __repr__(self):
        return f"Cell: top_left:{self._top_left}, top_right:{self._top_right}, bottom_left:{self._bottom_left}, bottom_right:{self._botom_right}"




class Maze:
    def __init__(self, cell_size_x, cell_size_y, window):
        self.window = window
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._num_cols = self.window._width // self._cell_size_x            # Get the max number of columns based on the width of the window and width of columns
        self._num_rows = self.window._height // self._cell_size_y           # Get the max number of rows based on the height of the window and height of columns

        if self._cell_size_x > self.window._width or self.window._width // self._cell_size_x <= 1:
            raise ValueError("Cell width should be at least half of the window width.")
        if self._cell_size_y > self.window._height or self.window._height // self._cell_size_y <= 1:
            raise ValueError("Cell height should be at least half of the window height.")

    def _create_cells(self):
        self.cols = []                          # Initialize the Mazes column list
        for x in range(self._num_cols):
            col = []                                # Initialize the row list for each column
            for y in range(self._num_rows):             # Create each cell                
                cell = Cell(
                    Point(x * self._cell_size_x, y * self._cell_size_y),
                    Point((x + 1) * self._cell_size_x, (y + 1) * self._cell_size_y),
                    self.window
                )
                cell.draw()                             # Draw the cell
                self._animate()                         # Animate after drawing each cell
                col.append(cell)                        # Add cell to the column
            self.cols.append(col)                   # Add column to cols

    def _animate(self):
        self.window.redraw()            # Redraw the window / "Show what was drawn so far"
        sleep(0.05)                     # Sleep to slow down the animation to a human-visible speed
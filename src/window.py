from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()                                          # Initiate a root window
        self.__root.geometry(f"{width}x{height}")                   # Set the root window's width and height
        self.__root.title("Maze solver")                            # Set the root window's title
        self.__root.protocol("WM_DELETE_WINDOW", self.close)        # Connect self.close to the "delete window" action
        self.canvas = Canvas(self.__root)                                    # Create a widget for drawing graphics
        self.canvas.pack()                                        # Pack the widget into the root window
        self.__running = False                                      # Define the app's running state

    def redraw(self):
        self.__root.update_idletasks()                              # Process all pending idle tasks, without processing any other events
        # self.__root.update()                                      # Process all pending events, call event callbacks, complete any pending geometry management, redraw widgets as necessary, and call all pending idle tasks

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)                        # Draw a line in root's canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point (x: {self.x}, y: {self.y}"


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.line_id = None

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
        self.__top_left = Point(starting_point.x, starting_point.y)
        self.__top_right = Point(ending_point.x, starting_point.y)
        self.__bottom_left = Point(starting_point.x, ending_point.y)
        self.__botom_right = Point(ending_point.x, ending_point.y)

        self._left_wall = Line(self.__top_left, self.__bottom_left)
        self._right_wall = Line(self.__top_right, self.__botom_right)
        self._top_wall = Line(self.__top_left, self.__top_right)
        self._bottom_wall = Line(self.__bottom_left, self.__botom_right)

        self.__canvas = window.canvas        
        
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

    def draw(self):
        draw_wall = lambda wall: wall.draw(self.__canvas, "black")

        if self.left_wall:
            draw_wall(self._left_wall)
        if self.right_wall:
            draw_wall(self._right_wall)
        if self.top_wall:
            draw_wall(self._top_wall)
        if self.bottom_wall:
            draw_wall(self._bottom_wall)

    def break_wall(self, *args):
        break_wall = lambda wall: self.__canvas.delete(wall.line_id)

        for arg in args:
            if arg == "left" and self.left_wall:
                self.left_wall = False
                break_wall(self._left_wall)
            elif arg == "right" and self.right_wall:
                self.right_wall = False
                break_wall(self._right_wall)
            elif arg == "top" and self.top_wall:
                self.top_wall = False
                break_wall(self._top_wall)
            elif arg == "bottom" and self.bottom_wall:
                self.bottom_wall = False
                break_wall(self._bottom_wall)
            else:
                raise Exception("Invalid argument or wall already broken. Arguments can be 'left', 'right', 'top' and/or 'bottom'.")
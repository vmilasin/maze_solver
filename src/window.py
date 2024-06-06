from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()                                          # Initiate a root window
        self.__root.geometry(f"{width}x{height}")                   # Set the root window's width and height
        self.__root.title("Maze solver")                            # Set the root window's title
        self.__root.protocol("WM_DELETE_WINDOW", self.close)        # Connect self.close to the "delete window" action
        self.__canvas = Canvas()                                    # Create a widget for drawind graphics
        self.__canvas.pack()                                        # Pack the widget into the root window
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
        line.draw(self.__canvas, fill_color)


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

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

    def __repr__(self):
        return f"Line from point1({self.point1.x}, {self.point1.y}) to point2({self.point2.x}, {self.point2.y})"
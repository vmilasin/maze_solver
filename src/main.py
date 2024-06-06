from window import Window, Point, Line

def main():
    win = Window(800, 600)
    point1 = Point(20, 60)
    point2 = Point(40, 80)
    point3 = Point(80, 40)
    point4 = Point(120, 20)
    point5 = Point(20, 120)
    line1 = Line(point1, point3)
    line2 = Line(point2, point4)
    line3 = Line(point3, point5)
    line4 = Line(point5, point1)
    win.draw_line(line1, "black")
    win.draw_line(line2, "red")
    win.draw_line(line3, "yellow")
    win.draw_line(line4, "black")
    win.wait_for_close()

main()
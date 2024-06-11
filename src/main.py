from window import Window, Point, Cell, Maze

def main():
    win = Window(800, 640)
    '''point1 = Point(0, 0)
    point2 = Point(40, 0)
    point3 = Point(80, 0)
    point4 = Point(0, 40)
    point5 = Point(40, 40)
    point6 = Point(80, 40)
    point7 = Point(0, 80)
    point8 = Point(40, 80)
    point9 = Point(80, 80)

    cell1 = Cell(point1, point5, win)
    cell2 = Cell(point2, point6, win)
    cell3 = Cell(point4, point8, win)
    cell4 = Cell(point5, point9, win)

    cells = [cell1, cell2, cell3, cell4]
    for cell in cells:
        cell.draw()

    cell1.break_wall("right")
    cell2.break_wall("bottom")
    cell4.break_wall("top", "right")

    cell1.draw_move(cell2)
    cell2.draw_move(cell3)
    cell3.draw_move(cell4)'''
    
    maze = Maze(80, 80, win)
    maze._create_cells()
    maze._break_entrance_and_exit()
    maze._break_walls_r()
    maze._solve()

    win.wait_for_close()

main()
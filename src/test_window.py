import unittest
from unittest.mock import Mock, call
from window import Window, Point, Line, Cell

class TestPoint(unittest.TestCase):
    def test_point_creation(self):
        point = Point(3, 4) 
        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)

class TestLine(unittest.TestCase):
    def test_line_creation(self):
        p1 = Point(0, 0)
        p2 = Point(100, 100)
        line = Line(p1, p2)
        self.assertEqual(line.point1, p1)
        self.assertEqual(line.point2, p2)

class TestWindow(unittest.TestCase):
    def test_draw_line(self):
        window = Window(800, 400)
        
        p1 = Point(0, 0)
        p2 = Point(100, 100)
        line = Line(p1, p2)
        
        # Mock the Canvas object
        mock_canvas = Mock()
        window.canvas = mock_canvas
        
        window.draw_line(line, "red")
        
        # Check if the create_line method on the canvas is called with the correct arguments
        mock_canvas.create_line.assert_called_once_with(
            p1.x, p1.y, p2.x, p2.y, fill="red", width=2
        )


class TestCell(unittest.TestCase):
    def setUp(self):
        # Called before every test to set up the environment
        self.win = Window(800, 600)
        self.mock_canvas = Mock()
        self.win.canvas = self.mock_canvas

        # Create points for a small grid
        self.point1 = Point(0, 0)
        self.point2 = Point(40, 0)
        self.point3 = Point(80, 0)
        self.point4 = Point(0, 40)
        self.point5 = Point(40, 40)
        self.point6 = Point(80, 40)
        self.point7 = Point(0, 80)
        self.point8 = Point(40, 80)
        self.point9 = Point(80, 80)

        # Initialize cells
        self.cell1 = Cell(self.point1, self.point5, self.win)
        self.cell2 = Cell(self.point2, self.point6, self.win)
        self.cell3 = Cell(self.point4, self.point8, self.win)
        self.cell4 = Cell(self.point5, self.point9, self.win)

        # Draw all cells
        cells = [self.cell1, self.cell2, self.cell3, self.cell4]
        for cell in cells:
            cell.draw()

        # Break down walls
        self.cell1.break_wall("right")
        self.cell2.break_wall("bottom")
        self.cell4.break_wall("top", "right")

        # Move between cells
        self.cell1.draw_move(self.cell2)
        self.cell2.draw_move(self.cell4)

    def tearDown(self):
        # Called after every test to clean up
        del self.win
        del self.mock_canvas
        del self.cell1
        del self.cell2
        del self.cell3
        del self.cell4

    
    def test_create_cells(self):
        expected_create_calls = [
            call.create_line(0, 0, 0, 40, fill="black", width=2),       # c1 left wall
            call.create_line(40, 0, 40, 40, fill="black", width=2),     # c1 right wall
            call.create_line(0, 0, 40, 0, fill="black", width=2),       # c1 top wall
            call.create_line(0, 40, 40, 40, fill="black", width=2),     # c1 bottom wall   
            call.create_line(40, 0, 40, 40, fill="black", width=2),     # c2 L
            call.create_line(80, 0, 80, 40, fill="black", width=2),     # c2 R
            call.create_line(40, 0, 80, 0, fill="black", width=2),      # c2 T
            call.create_line(40, 40, 80, 40, fill="black", width=2),    # c2 B
            call.create_line(0, 40, 0, 80, fill="black", width=2),      # c3 L
            call.create_line(40, 40, 40, 80, fill="black", width=2),    # c3 R
            call.create_line(0, 40, 40, 40, fill="black", width=2),     # c3 T
            call.create_line(0, 80, 40, 80, fill="black", width=2),     # c3 B
            call.create_line(40, 40, 40, 80, fill="black", width=2),    # c4 L
            call.create_line(80, 40, 80, 80, fill="black", width=2),    # c4 R
            call.create_line(40, 40, 80, 40, fill="black", width=2),    # c4 T
            call.create_line(40, 80, 80, 80, fill="black", width=2)     # c4 B    
        ]
        self.win.canvas.create_line.assert_has_calls(expected_create_calls, any_order=True)
        

    def test_break_walls(self):
        expected_delete_calls = [
            call.delete(self.cell1._right_wall.line_id),
            call.delete(self.cell2._bottom_wall.line_id),
            call.delete(self.cell3._top_wall.line_id),
            call.delete(self.cell3._bottom_wall.line_id)
        ]
        self.win.canvas.delete.assert_has_calls(expected_delete_calls, any_order=True)

    
    def test_move_to_cell(self):
        expected_move_calls = [
            call.create_line(20, 20, 60, 20, fill="red", width=2), 
            call.create_line(60, 20, 60, 60, fill="red", width=2),    
        ]
        self.win.canvas.create_line.assert_has_calls(expected_move_calls, any_order=True)







if __name__ == '__main__':
    unittest.main()
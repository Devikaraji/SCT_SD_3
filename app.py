from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows your HTML page to talk to the Python server

def find_empty(grid):
    """Finds an empty cell (represented by 0) in the grid."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)  # row, col
    return None

def is_valid(grid, num, pos):
    """Checks if a number is valid in a given position."""
    row, col = pos

    # Check row
    for j in range(9):
        if grid[row][j] == num and j != col:
            return False

    # Check column
    for i in range(9):
        if grid[i][col] == num and i != row:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_sudoku(grid):
    """Solves the Sudoku puzzle using a backtracking algorithm."""
    find = find_empty(grid)
    if not find:
        return True  # Puzzle is solved
    else:
        row, col = find

    for num in range(1, 10): # Try numbers 1 through 9
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            if solve_sudoku(grid):
                return True # If the recursive call found a solution

            # Backtrack: reset the cell if the path didn't lead to a solution
            grid[row][col] = 0
            
    return False # Trigger backtracking in the previous call

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    grid = data['grid']

    if solve_sudoku(grid):
        return jsonify({'solution': grid})
    else:
        return jsonify({'error': 'This puzzle is unsolvable.'}), 400

if __name__ == '__main__':
    print("Sudoku solver server started on http://127.0.0.1:5000")
    app.run(debug=True)
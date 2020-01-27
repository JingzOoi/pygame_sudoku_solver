# pygame_sudoku_solver

Solving sudoku using Python.  
Pygame is used for the display and controls, while the actual solving uses backtracking.  
Tried to emulate OOP as close as possible.

## Installation
0. Prerequisites: 

* Python 3.7+ (3.6 might work with no problems in theory)
* pip

1. Clone/download-and-extract this repository into a folder. Start up Powershell/Command Prompt in said folder. (Shift + Right click -> *Open Powershell window here*)  
2. (Optional) Make a virtual environment.
```
python -m venv venv
```
3. Install the required module(s).
```
pip install -r requirements.txt
```

4. You're good to go.

## Using the program
1. Start up the program. You should see a window with a Sudoku board with an additional grid.

2. (Optional) To test it, press Enter. This triggers the solve command and solves the board with no numbers given. You should see a valid solved board on the window starting with 1, 2, 3, 4...

3. (Optional) Press Space to clear the grid.

4. The additional grid on your bottom left shows the current value being held by the cursor. Clicking a grid with it will cause said grid to change to show that number. Pressing the number keys on your keyboard causes the current value to change. Using this feature, fill the board with an initial state (the board that is yet to be solved). Should you have made a mistake, right clicking on the grid should erase its number.

5. When you finish the initial state, (make sure to double check), press Enter.

6. The board should be solved.

## Technicalities
There are 5 classes in the code:  
* `Grid`: A space on a Sudoku board. Holds a value unique to column, row, and box (a 3 grid by 3 grid section of the board).
* `Board`: A collection of Grids. Handles positioning. 
* `Game`: A Sudoku game. Handles logic.
* `Window`: A pygame window application. Handles events.
* `Renderer`: An instance of a renderer. Handles drawing on the Window.

The size of every element depends on the size of the Grids. To change the size of the overall application, just change the value of `Grid.SIZE`.

## To-Do
1. Error handling: the program stops responding when it tries to solve a board that has incorrect inputs (e.g. same number on same row) by the user. Also needs to catch unsolvable puzzles.

2. Better user input method: current user input method is a bit incovenient.
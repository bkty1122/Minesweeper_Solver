Minesweeper Solver: a classic game which can be solved by problem-constraint model

This is a Minesweeper Solver which combines the very classic "Counting method" algothrim and "Problem Constraint" library for further enhancing the analytical states. For example, if the "counting method" algothrim cannot find a safe tiles, the solver will automatically switch to the "problem constraint" algothrim, which takes a long time to calculate, as it need to first generates all possible combinations under the constraint provided by the gameboard, then calculating different tiles' probability of containing mines, which takes more memorys than running the "counting method" algothrim.

For initialising the gameboard, run GUI.py in the file. Remember to activate the environment first, by running: venv\activate in the terminal.


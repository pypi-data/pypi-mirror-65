# py_libsudoku
Python binding for libsudoku - a C++ lib for generating and solving Sudoku puzzles.

## Installing as a Python Extension

Can be installed from directly from [**PyPi**](https://pypi.org/project/py-libsudoku) with:

    pip install py-libsudoku
    
Installation requires a C++ 11 compliant compiler and CMake version 3.5 or above.

## Cloning the Repository

**py_libsudoku** references [**pybind11**](https://github.com/pybind/pybind11) and [**libsudoku**](https://github.com/raulcostajunior/libsudoku) as submodules. To clone **py_sudoku**, use:

    git clone --recurse-submodules https://github.com/raulcostajunior/py_libsudoku.git

Then install in your current Python environment - requires a C++ 11 compliant compiler and CMake version 3.5 or above:

    cd [directory where py_libsudoku is]
    pip install .

Demo scripts with examples on how to use the lib:

    demo_board.py
    demo_solver.py
    demo_generator.py



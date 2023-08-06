#include "board.h"
#include "generator.h"
#include "solver.h"

#include <cstdint>
#include <iostream>
#include <sstream>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
namespace py = pybind11;

PYBIND11_MODULE(py_libsudoku, m)
{
     m.doc() = "Python bindings for libsudoku";

     py::enum_<sudoku::SetValueResult>(m, "SetValueResult")
         .value("NO_ERROR", sudoku::SetValueResult::NoError)
         .value("INVALID_VALUE", sudoku::SetValueResult::InvalidValue)
         .value("VALUE_INVALIDATES_BOARD", sudoku::SetValueResult::ValueInvalidatesBoard);

     py::class_<sudoku::Board>(m, "Board")

         .def(py::init(), "Creates an empty board.")

         .def(py::init<const std::vector<std::uint8_t> &>(),
              "Creates a board with the given values (up to 81 values between 0 and 9).")

         .def(py::init<const sudoku::Board &>(), "Creates a board that is a copy of a given board.")

         .def_property_readonly("isEmpty",
                                &sudoku::Board::isEmpty,
                                "True if all the positions in the board are 0.")

         .def_property_readonly("isValid",
                                &sudoku::Board::isValid,
                                "True if the board has no invalid values nor repetitions of values "
                                "across lines, columns or sections.")

         .def_property_readonly("isComplete",
                                &sudoku::Board::isComplete,
                                "True if the board corresponds to a solved puzzle.")

         .def("valueAt",
              &sudoku::Board::valueAt,
              "The value at a given board position - (line, column) pair.",
              py::arg("line"),
              py::arg("column"))

         .def("setValueAt",
              &sudoku::Board::setValueAt,
              "Sets the value at a given board position - (line, column) pair.",
              py::arg("line"),
              py::arg("column"),
              py::arg("value"))

         .def("getInvalidPositions",
              &sudoku::Board::getInvalidPositions,
              "Returns the board positions that contain invalid value - "
              "either for being out of range or for violating the non repetion rules.")

         .def("getPossibleValues",
              &sudoku::Board::getPossibleValues,
              "Returns the values that can be placed in a given non empty position without invalidating "
              "the board.")

         .def("clear", &sudoku::Board::clear, "Clears the board by assigning 0 to all its positions.")

         .def(py::self == py::self)

         .def("__repr__",
              [](const sudoku::Board &board) {
                   std::ostringstream ostr;
                   ostr << "<py_libsudoku.Board:\n";
                   ostr << board;
                   ostr << ">\n";
                   return ostr.str();
              })

         .def("__str__",
              [](const sudoku::Board &board) {
                   std::ostringstream ostr;
                   ostr << std::endl;
                   ostr << "------+-----+------";
                   ostr << std::endl;
                   for (int vGroup = 0; vGroup < 3; vGroup++)
                   {
                        for (int lin = 0; lin < 3; lin++)
                        {
                             ostr << "|" << (int)board.valueAt(lin + 3 * vGroup, 0) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 1) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 2) << "|";
                             ostr << (int)board.valueAt(lin + 3 * vGroup, 3) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 4) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 5) << "|";
                             ostr << (int)board.valueAt(lin + 3 * vGroup, 6) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 7) << " "
                                  << (int)board.valueAt(lin + 3 * vGroup, 8) << "|";
                             ostr << std::endl;
                        }
                        if (vGroup < 2)
                        {
                             ostr << "------+-----+------";
                             ostr << std::endl;
                        }
                   }
                   ostr << "------+-----+------";
                   ostr << std::endl;

                   return ostr.str();
              })

         .def("__len__", [](const sudoku::Board &) { return 81; })

         .def("__getitem__", [](const sudoku::Board &b, size_t i) {
              if (i >= 81)
                   throw py::index_error();
              return b.valueAt(i / 9, i % 9);
         });

     py::enum_<sudoku::SolverResult>(m, "SolverResult")
         .value("NO_ERROR", sudoku::SolverResult::NoError)
         .value("INVALID_BOARD", sudoku::SolverResult::InvalidBoard)
         .value("EMPTY_BOARD", sudoku::SolverResult::EmptyBoard)
         .value("ALREADY_SOLVED", sudoku::SolverResult::AlreadySolved)
         .value("HAS_NO_SOLUTION", sudoku::SolverResult::HasNoSolution)
         .value("INVALID_CANDIDATES_VECTOR", sudoku::SolverResult::InvalidatesCandidatesVector)
         .value("ASYNC_SOLVED_CANCELLED", sudoku::SolverResult::AsyncSolvingCancelled)
         .value("ASYNC_SOLVING_SUBMITTED", sudoku::SolverResult::AsyncSolvingSubmitted)
         .value("ASYNC_SOLVING_BUSY", sudoku::SolverResult::AsyncSolvingBusy);

     py::class_<sudoku::Solver>(m, "Solver")

         .def(py::init())

         .def("solve",
              (sudoku::SolverResult(sudoku::Solver::*)(const sudoku::Board &, sudoku::Board &)) & sudoku::Solver::solve,
              "Solves a Sudoku puzzle using the default candidates vector.")

         .def("solve",
              (sudoku::SolverResult(sudoku::Solver::*)(const sudoku::Board &, const std::vector<uint8_t> &, sudoku::Board &)) & sudoku::Solver::solve,
              "Solves a Sudoku puzzle using the given candidates vector.")

         .def("asyncSolveForGood", &sudoku::Solver::asyncSolveForGood,
              "Assynchronously finds all solutions for a given board")

         .def("cancelAsyncSolving", &sudoku::Solver::cancelAsyncSolving,
              "Cancels any ongoing asyncSolveForGood processing.");

     py::enum_<sudoku::GeneratorResult>(m, "GeneratorResult")
         .value("NO_ERROR", sudoku::GeneratorResult::NoError)
         .value("ASYNC_GEN_CANCELLED", sudoku::GeneratorResult::AsyncGenCancelled)
         .value("ASYNC_GEN_SUBMITTED", sudoku::GeneratorResult::AsyncGenSubmitted)
         .value("ASYNC_GEN_BUSY", sudoku::GeneratorResult::AsyncGenBusy);

     py::enum_<sudoku::PuzzleDifficulty>(m, "PuzzleDifficulty")
         .value("EASY", sudoku::PuzzleDifficulty::Easy)
         .value("MEDIUM", sudoku::PuzzleDifficulty::Medium)
         .value("HARD", sudoku::PuzzleDifficulty::Hard);

     py::class_<sudoku::Generator>(m, "Generator")

         .def(py::init())

         .def("asyncGenerate", &sudoku::Generator::asyncGenerate,
              "Assynchronously generates a board with a given difficulty level.")

         .def("cancelAsyncGenerate", &sudoku::Generator::cancelAsyncGenerate,
              "Cancels any ongoing asyncGenerate processing.")

         .def("maxEmptyPositions", &sudoku::Generator::maxEmptyPositions,
              "The maximum number of empty positions allowed in a generated puzzle with a given difficulty.");
}

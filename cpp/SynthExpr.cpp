#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "formulas.h"
#include "functions.h"
#include "generators.h"

namespace py = pybind11;

// PYBIND11_MAKE_OPAQUE(std::shared_ptr<Formula>);

PYBIND11_MODULE(SynthExpr, m) {
    // Formulas
    py::class_<Formula, FormulaPtr>(m, "Formula")
        .def(py::init<>()); // Assuming default constructors are available

    py::class_<Var, Formula, VarPtr>(m, "Var")
        .def(py::init<std::string>());

    py::class_<Not, Formula, NotPtr>(m, "Not")
        .def(py::init<FormulaPtr>());

    py::class_<And, Formula, AndPtr>(m, "And")
        .def(py::init<FormulaPtr, FormulaPtr>());

    py::class_<Or, Formula, OrPtr>(m, "Or")
        .def(py::init<FormulaPtr, FormulaPtr>());

    py::class_<Implies, Formula, ImpliesPtr>(m, "Implies")
        .def(py::init<FormulaPtr, FormulaPtr>());

    py::class_<Iff, Formula, IffPtr>(m, "Iff")
        .def(py::init<FormulaPtr, FormulaPtr>());

    // Functions
    py::class_<ToStringFunction>(m, "ToString")
        .def(py::init<>())
        .def("__call__", &ToStringFunction::operator());

    // Generators
    py::class_<RandomGeneratorZipf>(m, "RandomGeneratorZipf")
        .def(py::init<>())
        .def(py::init<std::vector<VarPtr>, int, double, double>())
        .def("seed", &RandomGeneratorZipf::seed)
        .def("__call__", [](RandomGeneratorZipf &self) { return self.operator()(); });
        // .def("__call__", &RandomGeneratorZipf::operator());
}


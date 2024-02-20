#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "formulas.h"
#include "visitors.h"
#include "generators.h"

namespace py = pybind11;

PYBIND11_MODULE(SynthExpr, m) {
    // Formulas
    py::class_<Formula>(m, "Formula");
    py::class_<Var, Formula>(m, "Var")
        .def(py::init<std::string>());
    py::class_<Not, Formula>(m, "Not")
        .def(py::init<Formula&>());
    py::class_<And, Formula>(m, "And")
        .def(py::init<Formula&, Formula&>());
    py::class_<Or, Formula>(m, "Or")
        .def(py::init<Formula&, Formula&>());
    py::class_<Implies, Formula>(m, "Implies")
        .def(py::init<Formula&, Formula&>());
    py::class_<Iff, Formula>(m, "Iff")
        .def(py::init<Formula&, Formula&>());
        
    // Visitors
    py::class_<ToStringVisitor, std::shared_ptr<ToStringVisitor>>(m, "ToString")
        .def(py::init<>())
        .def("__call__", &ToStringVisitor::operator());

    // Generators
    py::class_<RandomGeneratorZipf>(m, "RandomGeneratorZipf")
        .def(py::init<>())
        .def(py::init<std::vector<Var>, int, double, double>())
        .def("seed", &RandomGeneratorZipf::seed)
        .def("__call__", [](RandomGeneratorZipf &self) { return self.operator()(); });
        // .def("__call__", &RandomGeneratorZipf::operator());
}


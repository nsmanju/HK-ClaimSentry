#include <pybind11/pybind11.h>
#include "rule_engine.h"
namespace py = pybind11;
PYBIND11_MODULE(claim_engine_cpp, m) {
    py::class_<Claim>(m, "Claim").def(py::init<>())
        .def_readwrite("hospital_code", &Claim::hospital_code)
        .def_readwrite("amount_hkd", &Claim::amount_hkd)
        .def_readwrite("hko_signal", &Claim::hko_signal)
        .def_readwrite("diagnosis_en", &Claim::diagnosis_en);
    py::class_<FlagResult>(m, "FlagResult")
        .def_readonly("flagged", &FlagResult::flagged)
        .def_readonly("reason", &FlagResult::reason)
        .def_readonly("risk_score", &FlagResult::risk_score);
    m.def("scrutinize_claim", &scrutinize_claim, "HK Insurance Claim Scrutiny - C++ Engine");
}

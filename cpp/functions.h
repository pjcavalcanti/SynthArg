#ifndef VISITORS_H
#define VISITORS_H

#include "formulas.h"

class ToStringFunction {
    public:
        std::string operator()(const FormulaPtr f) const {
            switch (f->type) {
                case Formula::VAR:
                    return std::static_pointer_cast<Var>(f)->name;
                case Formula::NOT:
                    return "!" + operator()(f->f1);
                case Formula::AND:
                    return "(" + operator()(f->f1) + " & " + operator()(f->f2) + ")";
                case Formula::OR:
                    return "(" + operator()(f->f1) + " | " + operator()(f->f2) + ")";
                case Formula::IMPLIES:
                    return "(" + operator()(f->f1) + " -> " + operator()(f->f2) + ")";
                case Formula::IFF:
                    return "(" + operator()(f->f1) + " <-> " + operator()(f->f2) + ")";
            }
            throw std::runtime_error("Unknown formula type");
        }
};

#endif
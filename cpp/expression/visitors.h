#ifndef VISITORS_H
#define VISITORS_H

#include "formulas.h"

class ToStringVisitor : public Visitor<std::string> {
    private:
        std::string visit(const Var* formula) override {
            return formula->name;
        }
        std::string visit(const Not* formula) override {
            return "!" + formula->f1->accept(this);
        }
        std::string visit(const And* formula) override {
            return "(" + formula->f1->accept(this) + " & " + formula->f2->accept(this) + ")";
        }
        std::string visit(const Or* formula) override {
            return "(" + formula->f1->accept(this) + " | " + formula->f2->accept(this) + ")";
        }
        std::string visit(const Implies* formula) override {
            return "(" + formula->f1->accept(this) + " -> " + formula->f2->accept(this) + ")";
        }
        std::string visit(const Iff* formula) override {
            return "(" + formula->f1->accept(this) + " <-> " + formula->f2->accept(this) + ")";
        }

    public:
        ToStringVisitor() {};
        std::string operator()(Formula &formula) {
            return formula.accept(this);
        }
};

#endif
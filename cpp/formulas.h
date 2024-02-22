#ifndef FORMULAS_H
#define FORMULAS_H

#include <string>
#include <memory>

struct Formula;
struct Var;
struct Not;
struct And;
struct Or;
struct Implies;
struct Iff;

using FormulaPtr = std::shared_ptr<Formula>;
using VarPtr = std::shared_ptr<Var>;
using NotPtr = std::shared_ptr<Not>;
using AndPtr = std::shared_ptr<And>;
using OrPtr = std::shared_ptr<Or>;
using ImpliesPtr = std::shared_ptr<Implies>;
using IffPtr = std::shared_ptr<Iff>;

struct Formula {
    enum Type {
        VAR,
        NOT,
        AND,
        OR,
        IMPLIES,
        IFF,
    };
    Type type;
    std::shared_ptr<Formula> f1;
    std::shared_ptr<Formula> f2;
    virtual ~Formula() = default;
};

struct Var : Formula {
    std::string name;
    Var(std::string name) : name(name) {
        type = VAR;
    }
    static std::shared_ptr<Var> create (std::string name) {
        return std::make_shared<Var>(name);
    }
};

struct Not : Formula {
    Not(std::shared_ptr<Formula> _f1) {
        type = NOT;
        f1 = _f1;
    }
    static std::shared_ptr<Not> create (std::shared_ptr<Formula> f1) {
        return std::make_shared<Not>(f1);
    }
};

struct And : Formula {
    And(std::shared_ptr<Formula> _f1, std::shared_ptr<Formula> _f2) {
        type = AND;
        f1 = _f1;
        f2 = _f2;
    }
    static std::shared_ptr<And> create (std::shared_ptr<Formula> f1, std::shared_ptr<Formula> f2) {
        return std::make_shared<And>(f1, f2);
    }
};

struct Or : Formula {
    Or(std::shared_ptr<Formula> _f1, std::shared_ptr<Formula> _f2) {
        type = OR;
        f1 = _f1;
        f2 = _f2;
    }
    static std::shared_ptr<Or> create (std::shared_ptr<Formula> f1, std::shared_ptr<Formula> f2) {
        return std::make_shared<Or>(f1, f2);
    }
};

struct Implies : Formula {
    Implies(std::shared_ptr<Formula> _f1, std::shared_ptr<Formula> _f2) {
        type = IMPLIES;
        f1 = _f1;
        f2 = _f2;
    }
    static std::shared_ptr<Implies> create (std::shared_ptr<Formula> f1, std::shared_ptr<Formula> f2) {
        return std::make_shared<Implies>(f1, f2);
    }
};

struct Iff : Formula {
    Iff(std::shared_ptr<Formula> _f1, std::shared_ptr<Formula> _f2) {
        type = IFF;
        f1 = _f1;
        f2 = _f2;
    }
    static std::shared_ptr<Iff> create (std::shared_ptr<Formula> f1, std::shared_ptr<Formula> f2) {
        return std::make_shared<Iff>(f1, f2);
    }
};



#endif
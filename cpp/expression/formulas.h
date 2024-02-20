#ifndef FORMULAS_H
#define FORMULAS_H

#include <string>

class Formula;
class Var;
class Not;
class And;
class Or;
class Implies;
class Iff;

#define MACRO_OVER_TYPES(MACRO) \
    MACRO(std::string) \
    MACRO(bool) \
    MACRO(Formula*) \
    MACRO(int) \
    MACRO(void) \
    MACRO(double) \
    MACRO(char)

#define ACCEPT_T(T) \
    T accept(Visitor<T>* visitor) override { \
        return visitor->visit(this); \
    }

#define VIRTUAL_ACCEPT_T(T) \
    virtual T accept(Visitor<T>* visitor) = 0;

#define ACCEPT_VISITOR_MACRO() \
    MACRO_OVER_TYPES(ACCEPT_T)
    
template <typename T>
class Visitor {
    public:
        virtual T visit(const Var* formula) = 0;
        virtual T visit(const Not* formula) = 0;
        virtual T visit(const And* formula) = 0;
        virtual T visit(const Or* formula) = 0;
        virtual T visit(const Implies* formula) = 0;
        virtual T visit(const Iff* formula) = 0;
        virtual ~Visitor() {}
};

class Formula {
    public:
        MACRO_OVER_TYPES(VIRTUAL_ACCEPT_T)
        
        virtual ~Formula() {}
};

class Var : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)

        std::string name;
        Var(std::string name) : name(name) {}
};

class Not : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Not(Formula &f1) : f1(&f1) {}
};

class And : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        And(Formula &f1, Formula &f2) : f1(&f1), f2(&f2) {}
};

class Or : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Or(Formula &f1, Formula &f2) : f1(&f1), f2(&f2) {}
};

class Implies : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Implies(Formula &f1, Formula &f2) : f1(&f1), f2(&f2) {}
};

class Iff : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Iff(Formula &f1, Formula &f2) : f1(&f1), f2(&f2) {}
};

#endif
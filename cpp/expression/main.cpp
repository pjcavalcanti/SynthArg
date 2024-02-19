#include <string>
#include <stdexcept>
#include <iostream>

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
        Not(Formula* f1) : f1(f1) {}
};

class And : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        And(Formula* f1, Formula* f2) : f1(f1), f2(f2) {}
};

class Or : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Or(Formula* f1, Formula* f2) : f1(f1), f2(f2) {}
};

class Implies : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Implies(Formula* f1, Formula* f2) : f1(f1), f2(f2) {}
};

class Iff : public Formula {
    public:
        MACRO_OVER_TYPES(ACCEPT_T)
        
        Formula* f1;
        Formula* f2;
        Iff(Formula* f1, Formula* f2) : f1(f1), f2(f2) {}
};

class ToStringVisitor : public Visitor<std::string> {
    public:
        ToStringVisitor() {};
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
};


int main() {
    Var x("x");
    Var p("y");
    Not Notx(&x);
    And xAndp (&x, &p);
    Or xOrp (&x, &p);
    Implies xImpliesp (&x, &p);
    Iff xIffp (&x, &p);

    ToStringVisitor* visitor = new ToStringVisitor();

    std::cout << x.accept(visitor) << std::endl;
    std::cout << Notx.accept(visitor) << std::endl;
    std::cout << xAndp.accept(visitor) << std::endl;
    std::cout << xOrp.accept(visitor) << std::endl;
    std::cout << xImpliesp.accept(visitor) << std::endl;
    std::cout << xIffp.accept(visitor) << std::endl;

    return 0;
}
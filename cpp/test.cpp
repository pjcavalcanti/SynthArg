#include <iostream>
#include <vector>

#include "formulas.h"
#include "functions.h"
#include "generators.h"

void testToString() {
    #define cout std::cout
    #define endl std::endl

    auto p = Var::create("p");
    auto q = Var::create("q");
    auto Notp = Not::create(p);
    auto pAndq = And::create(p, q);
    auto pOrq = Or::create(p, q);
    auto pImpliesq = Implies::create(p, q);
    auto pIffq = Iff::create(p, q);

    auto toString = ToStringFunction();

    cout << toString(p) << endl;
    cout << toString(Notp) << endl;
    cout << toString(pAndq) << endl;
    cout << toString(pOrq) << endl;
    cout << toString(pImpliesq) << endl;
    cout << toString(pIffq) << endl;

    auto NotNotpAndq = Not::create(And::create(Not::create(p), q));

    cout << toString(NotNotpAndq) << endl;
}

void testRandExpr() {
    #define cout std::cout
    #define endl std::endl

    double a = 1.1;
    double b = 2.7;
    int maxDepth = 5;
    std::vector<VarPtr> vars = {Var::create("x"), Var::create("y"), Var::create("z")};

    RandomGeneratorZipf randGen = RandomGeneratorZipf(vars, maxDepth, a, b);
    randGen.seed(1);

    auto toString = ToStringFunction();

    FormulaPtr expr = randGen();
    cout << toString(expr) << endl;
    for (int i = 0; i < 10; i++) {
        cout << toString(expr) << endl;
        expr = randGen();
    }
}

void testCountNodes() {
    struct NodeCounter {
        int operator()(const FormulaPtr f) const {
            switch (f->type) {
                case Formula::VAR:
                    return 1;
                case Formula::NOT:
                    return 1 + operator()(f->f1);
                case Formula::AND:
                case Formula::OR:
                case Formula::IMPLIES:
                case Formula::IFF:
                    return 1 + operator()(f->f1) + operator()(f->f2);
            }
        }
    };
    auto counter = NodeCounter();

    std::vector<VarPtr> vars = {Var::create("x"),
                                Var::create("y"),
                                Var::create("z")};
    double a = 1.1;
    double b = 2.7;
    int maxDepth = 5;

    auto toString = ToStringFunction();
    auto randGen = RandomGeneratorZipf(vars, maxDepth, a, b);
    randGen.seed(1);

    int totalNodes = 0;

    FormulaPtr expr = randGen();
    totalNodes += counter(expr);
    cout << toString(expr) << " " << " has " <<  counter(expr) << " nodes." << endl;
    for (int i = 0; i < 10; i++) {
        expr = randGen();
        totalNodes += counter(expr);
        cout << toString(expr) << " " << " has " <<  counter(expr) << " nodes." << endl;
    }
    cout << "Total nodes: " << totalNodes << endl;
}


int main() {
    // testToString();
    // testRandExpr();
    testCountNodes();
    return 0;
}


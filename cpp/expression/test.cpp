#include <iostream>

#include "formulas.h"
#include "visitors.h"
#include "generators.h"

void testToString() {
    Var x("x");
    Var p("y");
    Not Notx(x);
    And xAndp (x, p);
    Or xOrp (x, p);
    Implies xImpliesp (x, p);
    Iff xIffp (x, p);

    ToStringVisitor toString = ToStringVisitor();

    std::cout << toString(x) << std::endl;
    std::cout << toString(Notx) << std::endl;
    std::cout << toString(xAndp) << std::endl;
    std::cout << toString(xOrp) << std::endl;
    std::cout << toString(xImpliesp) << std::endl;
    std::cout << toString(xIffp) << std::endl;
}

void testRandExpr() {
    double a = 1.1;
    double b = 2.7;
    int maxDepth = 5;
    std::vector<Var> vars = {Var("x"), Var("y"), Var("z")};

    RandomGeneratorZipf randGen = RandomGeneratorZipf(vars, maxDepth, a, b);
    randGen.seed(1);

    ToStringVisitor toString = ToStringVisitor();
    Formula* expr = randGen();
    for (int i = 0; i < 10; i++) {
        std::cout << toString(*expr) << std::endl;
        expr = randGen();
    }
}
int main() {
    testRandExpr();
    return 0;
}


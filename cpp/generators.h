#ifndef GENERATORS_H
#define GENERATORS_H

#include <random>
#include <vector>
#include <cmath>

#include <iostream>

#include "formulas.h"

class RandomFormulaGenerator {
    virtual void seed(int seed) = 0;
    virtual FormulaPtr operator()() = 0;
};

class RandomGeneratorZipf : public RandomFormulaGenerator{
    private:
        enum class LeafTypes {
            Var,
            NumberOfLeafTypes
        };
        enum class UnaryTypes {
            Not,
            NumberOfUnaryTypes
        };
        enum class BinaryTypes {
            And,
            Or,
            Implies,
            Iff,
            NumberOfBinaryTypes
        };
        std::mt19937 rdg;
        std::vector<VarPtr> vars;
        std::vector<double> depthProbs; 
        int maxDepth;
        double a;
        double b;

        void init_depth_probs() {
            this->depthProbs = std::vector<double>(this->maxDepth);
            for (int i = 0; i < this->maxDepth; i++) {
                this->depthProbs[i] = 1.0 / pow((i + b), a);
            }
            for (int i = 1; i < this->maxDepth; i++) {
                this->depthProbs[i] += this->depthProbs[i - 1];
            }
            for (int i = 0; i < this->maxDepth; i++) {
                this->depthProbs[i] /= this->depthProbs[this->maxDepth - 1];
            }
        }


    public:
        RandomGeneratorZipf() {
            this->rdg.seed(std::random_device()());
            this->maxDepth = 5;
            this->a = 1.1;
            this->b = 2.7;
            this->vars = {Var::create("x"), Var::create("y"), Var::create("z")};

            this->init_depth_probs();
        };
        RandomGeneratorZipf(std::vector<VarPtr> vars, int maxDepth, double a, double b) {
            this->rdg.seed(std::random_device()());
            this->maxDepth = maxDepth;
            this->a = a;
            this->b = b;
            this->vars = vars;

            this->init_depth_probs();
        }


        void seed(int seed) override {
            this->rdg.seed(seed);
        };

        FormulaPtr operator()() override {
            return this->operator()(0);
        }

        FormulaPtr operator()(int currDepth) {
            bool shouldStop = (currDepth >= this->maxDepth) || ((this->rdg() % 100) / 100.0 < this->depthProbs[currDepth]);

            if (shouldStop) {
                return Var::create(this->vars[this->rdg() % this->vars.size()]->name);
            }

            int arity = this->rdg() % (3) + 1;
            if (arity == 1) {
                FormulaPtr f1 = this->operator()(currDepth + 1);
                return Not::create(f1);
            }

            FormulaPtr f1 = this->operator()(currDepth + 1);
            FormulaPtr f2 = this->operator()(currDepth + 1);

            int type = this->rdg() % static_cast<int>(BinaryTypes::NumberOfBinaryTypes);

            switch (static_cast<BinaryTypes>(type)) {
                case BinaryTypes::And:
                    return And::create(f1, f2);
                case BinaryTypes::Or:
                    return Or::create(f1, f2);
                case BinaryTypes::Implies:
                    return Implies::create(f1, f2);
                case BinaryTypes::Iff:
                    return Iff::create(f1, f2);
                case BinaryTypes::NumberOfBinaryTypes:
                    return nullptr;
            }
            return nullptr;
        }
};

#endif
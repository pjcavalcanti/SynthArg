#ifndef PROOFS_H
#define PROOFS_H

class ProofVisitor {
public:
    virtual void visit(const Proof* proof) = 0;
    virtual ~ProofVisitor() {}
};

class Proof {
public:
    virtual;
};



#endif
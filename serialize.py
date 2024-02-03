import json
from zol import Variable, And, Or, Not, Implies, Iff, Expression

def serialize_expression(expr):
    assert isinstance(expr, Expression)

    if isinstance(expr, And):
        return {
            "type": "And",
            "args": [serialize_expression(arg) for arg in expr.descendants()]
        }
    elif isinstance(expr, Or):
        return {
            "type": "Or",
            "args": [serialize_expression(arg) for arg in expr.descendants()]
        }
    elif isinstance(expr, Not):
        return {
            "type": "Not",
            "args": [serialize_expression(arg) for arg in expr.descendants()]
        }
    elif isinstance(expr, Implies):
        return {
            "type": "Implies",
            "args": [serialize_expression(arg) for arg in expr.descendants()]
        }
    elif isinstance(expr, Iff):
        return {
            "type": "Iff",
            "args": [serialize_expression(arg) for arg in expr.descendants()]
        }
    elif isinstance(expr, Variable):
        return {
            "type": "Variable",
            "name": expr.name
        }
    raise ValueError(f"Unknown expression type: {expr}")

def deserialize_expression(expr):
    assert isinstance(expr, dict)

    if expr["type"] == "And":
        return And(*[deserialize_expression(arg) for arg in expr["args"]])
    elif expr["type"] == "Or":
        return Or(*[deserialize_expression(arg) for arg in expr["args"]])
    elif expr["type"] == "Not":
        return Not(deserialize_expression(expr["args"][0]))
    elif expr["type"] == "Implies":
        return Implies(deserialize_expression(expr["args"][0]), deserialize_expression(expr["args"][1]))
    elif expr["type"] == "Iff":
        return Iff(deserialize_expression(expr["args"][0]), deserialize_expression(expr["args"][1]))
    elif expr["type"] == "Variable":
        return Variable(expr["name"])
    raise ValueError(f"Unknown expression type: {expr}")

def save_expressions(exprs, filename):
    with open(filename, "w") as f:
        for expr in exprs:
            json.dump(serialize_expression(expr), f)
            f.write("\n")

def load_expressions(filename):
    with open(filename) as f:
        return [deserialize_expression(json.loads(line)) for line in f]
    
if __name__ == "__main__":
    from generators import RandomExpressionZipf
    import os
    from tqdm import tqdm

    # Test with simple expressions
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    expr1 = And(Or(a, b), Not(c))
    expr2 = Implies(a, b)
    
    assert deserialize_expression(serialize_expression(expr1)) == expr1
    assert deserialize_expression(serialize_expression(expr2)) == expr2
    save_expressions([expr1, expr2], "test1.json")
    dexprs = load_expressions("test1.json")
    assert dexprs[0] == expr1
    assert dexprs[1] == expr2
    os.remove("test1.json")

    # Test with random expressions
    getRandExpr = RandomExpressionZipf(["a", "b", "c", "d", "e", "f"],10, 2, 3)
    exprs = []
    for _ in tqdm(range(1000)):
        expr = getRandExpr()
        assert deserialize_expression(serialize_expression(expr)) == expr
        exprs.append(expr)
    save_expressions(exprs, "test2.json")
    dexprs = load_expressions("test2.json")
    for expr, dexpr in zip(exprs, dexprs):
        assert expr == dexpr
    os.remove("test2.json")

    print("All tests passed")

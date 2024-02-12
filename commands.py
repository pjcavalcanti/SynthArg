from abc import ABC
from enum import Enum, auto
from zol import *
from generators import *


rdExprGen = RandomExpressionZipf(["a", "b", "c", "d", "e"], 5, 1.1, 2.7)
rdExprGen.seed(4)


class TreeNode:
    def __init__(self):
        self._data = None
        self._parent = None
        self._children = []

    def add_data(self, data):
        self._data = data

    def add_parent(self, parent):
        self._parent = parent

    def add_child(self, child):
        child.add_parent(self)
        self._children.append(child)

    def reset(self):
        self.__init__()

    def data(self):
        return self._data

    def parent(self):
        return self._parent

    def children(self):
        return self._children


class Actions(Enum):
    MAKE_TREE_DEEPER = auto()
    SELECT_PARENT = auto()
    SELECT_CHILD = auto()
    SELECT_VARIABLE = auto()
    QUIT = auto()


class NodeTypes(Enum):
    AND = auto()
    OR = auto()
    NOT = auto()
    IMPLIES = auto()
    VARIABLE = auto()
    IFF = auto()


class Variables(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()


class ExprGenGame:
    def __init__(self):
        self.exprTree = TreeNode()
        self.currNode = self.exprTree

    def getAvailableActions(self):
        options = [Actions.QUIT]
        if self.currNode.parent() is not None:
            options.append(Actions.SELECT_PARENT)
        if self.currNode.data() is None:
            options.append(Actions.MAKE_TREE_DEEPER)
            options.append(Actions.SELECT_VARIABLE)
        if self.currNode.data().type is not NodeTypes.VARIABLE:
            options.append(Actions.SELECT_CHILD)
        return options

    def reset(self):
        self.__init__()

    def chooseAction(self, action):
        self.currAction = action

    def quit(self):
        self.reset()
        return None

    def makeTreeDeeper(self, nodeType):
        self.currNode.reset()
        self.currNode.add_data(nodeType)

        if nodeType in [NodeTypes.AND, NodeTypes.OR, NodeTypes.IMPLIES, NodeTypes.IFF]:
            leftChild = TreeNode()
            rightChild = TreeNode()
            self.currNode.add_child(leftChild)
            self.currNode.add_child(rightChild)
        if nodeType in [NodeTypes.NOT]:
            child = TreeNode()
            self.currNode.add_child(child)

    def selectParent(self):
        self.currNode = self.currNode.parent()

    def selectChild(self, childIndex):
        self.currNode = self.currNode.children()[
            childIndex % len(self.currNode.children())
        ]

    def selectVariable(self, var):
        self.currNode.add_data(var)

    def getExpression(self):
        if self.currNode.data() is Variables:
            return Variable(self.currNode.data().name)
        elif self.currNode.data() in [
            NodeTypes.AND,
            NodeTypes.OR,
            NodeTypes.IMPLIES,
            NodeTypes.IFF,
        ]:
            return self.logicalConnector(self.currNode.data())(
                self.getExpression(self.currNode.children()[0]),
                self.getExpression(self.currNode.children()[1]),
            )
        elif self.currNode.data() is NodeTypes.NOT:
            return Not(self.getExpression(self.currNode.children()[0]))
        return None

    def logicalConnector(self, nodeType):
        if nodeType is NodeTypes.AND:
            return And
        if nodeType is NodeTypes.OR:
            return Or
        if nodeType is NodeTypes.NOT:
            return Not
        if nodeType is NodeTypes.IMPLIES:
            return Implies
        if nodeType is NodeTypes.IFF:
            return Iff
        if nodeType is NodeTypes.VARIABLE:
            return Variable


g = ExprGenGame()
node = TreeNode()
node.add_data(Variables.A)
print(Variable(node.data().name))

from point import *
import typing
import numpy as np


class TreeNode(Point):
    def __init__(self, treeNode: Point) -> None:
        super().__init__(*treeNode)
        self.father = None
        self.childLeft = None
        self.childRight = None


class TreeNodes:
    def __init__(self, treeNodes: typing.List[Point]) -> None:
        self.treeNodes = [TreeNode(node) for node in treeNodes]

    def __len__(self):
        return len(self.treeNodes)

    def __getitem__(self, key):
        return self.treeNodes[key]

    def __repr__(self):
        return str(self.treeNodes)

    def getSplitDimension(self, treeNodeDepth=1) -> int:
        return treeNodeDepth % min(list(x.dimension for x in self.treeNodes))

    def getMidpoint(self, dimension: int) -> TreeNode:
        dim = list(x[dimension] for x in self.treeNodes)
        rank = list(np.argsort(dim))
        if (len(self.treeNodes) % 2 == 0):
            return self.treeNodes[rank.index(len(rank)/2)]
        else:
            return self.treeNodes[rank.index((len(rank)-1)/2)]


def buildTree(treeNodes: TreeNodes, fatherNode=None, childTreeDirection=None, Depth=0):
    if len(treeNodes) == 0:
        return None

    splitDimension = treeNodes.getSplitDimension(Depth)
    rootNode = treeNodes.getMidpoint(splitDimension)
    rootNode.father = fatherNode
    if childTreeDirection == 'left':
        fatherNode.childLeft = rootNode
    if childTreeDirection == "right":
        fatherNode.childRight = rootNode

    LeftChildren, RightChildren = [], []
    Queue = [] 
    for node in treeNodes:
        if node[splitDimension] < rootNode[splitDimension]:
            LeftChildren.append(node)
        elif node[splitDimension] > rootNode[splitDimension]:
            RightChildren.append(node)
        elif node is rootNode:
            continue
        else:
            Queue.append(node)
    for node in Queue:
        if len(RightChildren) >= len(LeftChildren):
            LeftChildren.append(node)
        else:
            RightChildren.append(node)
    depth = Depth + 1
    leftChildBinaryTreeNodes = TreeNodes(LeftChildren)
    print(f"leftsub, d={depth}, nodes: {leftChildBinaryTreeNodes}")
    buildTree(leftChildBinaryTreeNodes, fatherNode=rootNode,
              childTreeDirection='left', Depth=depth)
    rightChildBinaryTreeNodes = TreeNodes(RightChildren)
    print(f"rightsub, d={depth}, nodes: {rightChildBinaryTreeNodes}")
    buildTree(rightChildBinaryTreeNodes, fatherNode=rootNode,
              childTreeDirection='right', Depth=depth)
    print(f"第{Depth}层, {rootNode}")
    return rootNode


buildTree(TreeNodes([Point(2, 1), Point(2, 2), Point(2, 4), Point(4, 3)]))

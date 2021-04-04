from l2radius_search import RadiusNNResultSet
from l2KNNResult import KNNResultSet
import numpy as np
import math


# data generation
# db_size = 10
# data = np.random.permutation(db_size).tolist()


class Node:
    def __init__(self, key, value=-1):
        self.left = None
        self.right = None
        self.key = key
        self.value = value


def insert(root, key, value=-1):
    # recursively insert each an element
    if root is None:
        root = Node(key, value)
    else:
        if key < root.key:
            root.left = insert(root.left, key, value)
        elif key > root.key:
            root.right = insert(root.right, key, value)
        else:
            pass
    return root


# insert each element
# root = None
# for i, point in enumerate(data):
# 	root = insert(root, point, i)


def search_recursive(root, key):
    if root is None or root.key == key:
        return root
    if key < root.key:
        return search_recursive(root.left, key)
    elif key > root.key:
        return search_recursive(root.right, key)


# method 2: using "current_node" to simulate a stack
def search_iterative(root, key):
    current_node = root
    while current_node is not None:
        if current_node.key == key:
            return current_node
        elif key < current_node.key:
            current_node = current_node.left
        elif key > current_node.key:
            current_node = current_node.right
    return current_node


def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root)
        inorder(root.left)


def preorder(root):
    if root is not None:
        print(root)
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    if root is not None:
        postorder(root.left)
        postorder(root.right)
        print(root)


def radius_search(root: Node, result_set: RadiusNNResultSet, key):
    if root is None:
        return False

    # compare the root itself
    result_set.add_point(math.fabs(root.key - key), root.value)

    if root.key >= key:
        # iterate left branch first
        if radius_search(root.left, result_set, key):
            return True
        elif math.fabs(root.key - key) < result_set.worstDist():
            return radius_search(root.right, result_set, key)
        return False
    else:
        # iterate right branch first
        if radius_search(root.right, result_set, key):
            return True
        elif math.fabs(root.key - key) < result_set.worstDist():
            return radius_search(root.left, result_set, key)
        return False


def knn_search(root: Node, result_set: KNNResultSet, key):
    if root is None:
        return False

    # compare the root itself
    result_set.add_point(math.fabs(root.key - key), root.value)
    if result_set.worstDist() == 0:  # a special case - if the worst distance is 0, no need to search anymore
        return True

    if root.key >= key:
        # iterate left branch first, if key != query, need to go through one subtree
        if knn_search(root.left, result_set, key):
            return True
        elif math.fabs(root.key - key) < result_set.worstDist():
            return knn_search(root.left, result_set, key)
        return False
    else:
        # iterate right branch first
        if knn_search(root.right, result_set, key):
            return True
        elif math.fabs(root.key - key) < result_set.worstDist():
            return knn_search(root.left, result_set, key)
        return False


def main():
    db_size = 100
    k = 5
    radius = 2.0

    data = np.random.permutation(db_size).tolist()

    root = None
    for i, point in enumerate(data):
        root = insert(root, point, i)

    query_key = 6
    result_set = KNNResultSet(capacity=k)
    knn_search(root, result_set, query_key)
    print("kNN Search:")
    print("index - distance")
    print(result_set)

    result_set = RadiusNNResultSet(radius=radius)
    radius_search(root, result_set, query_key)
    print("Radius NN Search:")
    print("index - distance")
    print(result_set)


if __name__ == '__main__':
    main()

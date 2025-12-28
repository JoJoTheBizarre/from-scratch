


class Node:
    def __init__(self, value=None):
        self.key =value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.key})"

class DuplicateKeyError(Exception):
    def __init__(self, key):
        super().__init__(f"Duplicate key: {key}")
        self.key = key

class KeyDoesNotExist(Exception):
    def __init__(self, key):
        super().__init__(f"Key Does not exist: {key}")
        self.key = key

class BinarySearchTree:
    def __init__(self):
        self.root: Node = None
        self._size: int = 0

    def insert(self, key: int) -> None:
        """Inserts a key in a BST, raises DuplicateKeyError if key already exists"""
        if self.root is None:
            self.root = Node(key)
            self._size += 1
            return

        current = self.root
        while True:
            if key == current.key:
                raise DuplicateKeyError(key)
            elif key < current.key:
                if current.left is None:
                    current.left = Node(key, parent=current)
                    self._size += 1
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(key, parent=current)
                    self._size += 1
                    return
                current = current.right

    def search(self, key: int) -> bool:
        """Returns True if key exists else False"""
        def traversal(root: Node, key:int)-> bool:
            if root is None:
                return False
            if root.key == key:
                return True
            elif root.key < key:
                return traversal(root.left, key)
            elif root.key > key:
                return traversal(root.right, key)
        return traversal(self.root, key)

    def delete(self, key: int) -> None:
        """
        Delete a node with the given key from the BST (no parent pointers).
        Raises KeyDoesNotExist if the key is not found.
        """
        
        node = self.root
        parent = None
        while node and node.key != key:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is None:
            raise KeyDoesNotExist(key)

        def replace_child(parent, old_child, new_child):
            if parent is None:
                self.root = new_child
            elif parent.left == old_child:
                parent.left = new_child
            else:
                parent.right = new_child

        if node.left is None:
            replace_child(parent, node, node.right)
        elif node.right is None:
            replace_child(parent, node, node.left)
        else:
            succ_parent = node
            successor = node.right
            while successor.left:
                succ_parent = successor
                successor = successor.left

            if succ_parent != node:
                replace_child(succ_parent, successor, successor.right)
                successor.right = node.right

            successor.left = node.left
            replace_child(parent, node, successor)

        self._size -= 1

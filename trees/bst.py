"""Binary Search Tree implementation with comprehensive features."""
from typing import Optional


class Node:
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None

    def __repr__(self) -> str:
        return f"Node({self.key})"


class DuplicateKeyError(Exception):
    def __init__(self, key: int):
        super().__init__(f"Duplicate key: {key}")
        self.key = key


class KeyDoesNotExist(Exception):
    def __init__(self, key: int):
        super().__init__(f"Key does not exist: {key}")
        self.key = key


class BinarySearchTree:
    root: Optional[Node]
    _size: int

    def __init__(self):
        self.root = None
        self._size = 0

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
                    current.left = Node(key)
                    self._size += 1
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(key)
                    self._size += 1
                    return
                current = current.right

    def search(self, key: int) -> bool:
        """Returns True if key exists else False"""
        def traversal(node: Optional[Node], search_key: int) -> bool:
            if node is None:
                return False
            if node.key == search_key:
                return True
            elif search_key < node.key:
                return traversal(node.left, search_key)
            else:
                return traversal(node.right, search_key)

        return traversal(self.root, key)

    def delete(self, key: int) -> None:
        """
        Delete a node with the given key from the BST.
        Raises KeyDoesNotExist if the key is not found.
        """
        node: Optional[Node] = self.root
        parent: Optional[Node] = None

        while node is not None and node.key != key:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is None:
            raise KeyDoesNotExist(key)

        def replace_child(
            parent_node: Optional[Node],
            old_child: Node,
            new_child: Optional[Node]
        ) -> None:
            if parent_node is None:
                self.root = new_child
            elif parent_node.left == old_child:
                parent_node.left = new_child
            else:
                parent_node.right = new_child

        if node.left is None:
            replace_child(parent, node, node.right)
        elif node.right is None:
            replace_child(parent, node, node.left)
        else:
            succ_parent: Node = node
            successor: Node = node.right

            while successor.left is not None:
                succ_parent = successor
                successor = successor.left

            if succ_parent != node:
                replace_child(succ_parent, successor, successor.right)
                successor.right = node.right

            successor.left = node.left
            replace_child(parent, node, successor)

        self._size -= 1

    def size(self) -> int:
        """Returns the number of nodes in the tree"""
        return self._size

    def is_empty(self) -> bool:
        """Returns True if the tree is empty"""
        return self.root is None

    def clear(self) -> None:
        """Removes all nodes from the tree"""
        self.root = None
        self._size = 0

    def min(self) -> int:
        """Returns the minimum key in the tree"""
        if self.root is None:
            raise ValueError("Tree is empty")

        current: Node = self.root
        while current.left is not None:
            current = current.left
        return current.key

    def max(self) -> int:
        """Returns the maximum key in the tree"""
        if self.root is None:
            raise ValueError("Tree is empty")

        current: Node = self.root
        while current.right is not None:
            current = current.right
        return current.key

    def height(self) -> int:
        """Returns the height of the tree (longest path from root to leaf)"""
        def _height(node: Optional[Node]) -> int:
            if node is None:
                return -1
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def inorder(self) -> list[int]:
        """Returns inorder traversal of the tree (sorted order)"""
        def _inorder(node: Optional[Node]):
            if node is not None:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)

        return list(_inorder(self.root))

    def preorder(self) -> list[int]:
        """Returns preorder traversal of the tree"""
        def _preorder(node: Optional[Node]):
            if node is not None:
                yield node.key
                yield from _preorder(node.left)
                yield from _preorder(node.right)

        return list(_preorder(self.root))

    def postorder(self) -> list[int]:
        """Returns postorder traversal of the tree"""
        def _postorder(node: Optional[Node]):
            if node is not None:
                yield from _postorder(node.left)
                yield from _postorder(node.right)
                yield node.key

        return list(_postorder(self.root))

    def __len__(self) -> int:
        """Returns the number of nodes in the tree"""
        return self._size

    def __contains__(self, key: int) -> bool:
        """Returns True if key exists in the tree (supports 'in' operator)"""
        return self.search(key)

    def __iter__(self):
        """Iterates through the tree in sorted order (inorder traversal)"""
        yield from self._inorder_iter(self.root)

    def _inorder_iter(self, node: Optional[Node]):
        """Helper for iterator"""
        if node is not None:
            yield from self._inorder_iter(node.left)
            yield node.key
            yield from self._inorder_iter(node.right)

    def __str__(self) -> str:
        """String representation of the tree"""
        if self.is_empty():
            return "BinarySearchTree(empty)"
        return f"BinarySearchTree(size={self._size}, root={self.root.key})"

    def __repr__(self) -> str:
        """Detailed representation of the tree"""
        return f"BinarySearchTree(nodes={self.inorder()})"

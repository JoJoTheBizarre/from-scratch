# Data Structures From Scratch

A collection of fundamental data structures implemented from scratch in Python, packaged with Poetry.

## Data Structures

### HashMap
A dynamic hash map implementation with:
- Collision handling via chaining
- Dynamic resizing based on load factor
- Support for int and string keys
- Dict-like interface (`[]`, `in`, `len()`)

### Binary Search Tree (BST)
A binary search tree implementation with:
- Insert, search, and delete operations
- Size tracking
- Min/max operations
- Three traversal methods (inorder, preorder, postorder)
- Custom exceptions for duplicate keys and missing keys

## Project Structure

```
from-scratch/
├── hashmap/
│   ├── __init__.py
│   └── hashmap.py
├── trees/
│   ├── __init__.py
│   └── bst.py
├── tests/
│   ├── test_hashmap.py    # 31 tests
│   └── test_bst.py         # 39 tests
├── pyproject.toml
└── README.md
```

## Installation

This project uses Poetry for dependency management:

```bash
poetry install
```

## Usage

### HashMap

```python
from hashmap import DynamicHashMap

hm = DynamicHashMap()
hm["key"] = "value"
hm.put("another", 123)

print(hm["key"])           # "value"
print(hm.get("another"))   # 123
print(len(hm))             # 2

for key, value in hm.items():
    print(f"{key}: {value}")
```

### Binary Search Tree

```python
from trees import BinarySearchTree

bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)

print(bst.search(30))      # True
print(bst.min())           # 30
print(bst.max())           # 70
print(bst.inorder())       # [30, 50, 70]

bst.delete(30)
print(bst.size())          # 2
```

## Running Tests

Run all tests:
```bash
poetry run pytest
```

Run tests with verbose output:
```bash
poetry run pytest -v
```

Run specific test file:
```bash
poetry run pytest tests/test_hashmap.py
poetry run pytest tests/test_bst.py
```

## Test Coverage

- **HashMap**: 31 tests covering core operations, resizing, collision handling, dict-like interface, and edge cases
- **BST**: 39 tests covering insert/search/delete, size tracking, min/max, traversals, and complex scenarios

Total: 70 tests, all passing

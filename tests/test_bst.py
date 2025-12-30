import pytest
from trees import BinarySearchTree, DuplicateKeyError, KeyDoesNotExist


# ---------- Basic operations ----------

def test_insert_and_search():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    assert bst.search(10) is True
    assert bst.search(5) is True
    assert bst.search(15) is True
    assert bst.search(20) is False


def test_insert_multiple_nodes():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for val in values:
        bst.insert(val)

    for val in values:
        assert bst.search(val) is True


def test_insert_duplicate_raises_error():
    bst = BinarySearchTree()
    bst.insert(10)

    with pytest.raises(DuplicateKeyError) as exc_info:
        bst.insert(10)

    assert exc_info.value.key == 10


def test_search_empty_tree():
    bst = BinarySearchTree()
    assert bst.search(10) is False


def test_search_nonexistent_key():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    assert bst.search(100) is False
    assert bst.search(7) is False


# ---------- Delete operations ----------

def test_delete_leaf_node():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    bst.delete(5)

    assert bst.search(5) is False
    assert bst.search(10) is True
    assert bst.search(15) is True
    assert bst.size() == 2


def test_delete_node_with_one_left_child():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(3)

    bst.delete(5)

    assert bst.search(5) is False
    assert bst.search(3) is True
    assert bst.search(10) is True


def test_delete_node_with_one_right_child():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(7)

    bst.delete(5)

    assert bst.search(5) is False
    assert bst.search(7) is True
    assert bst.search(10) is True


def test_delete_node_with_two_children():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    bst.delete(30)

    assert bst.search(30) is False
    assert bst.search(20) is True
    assert bst.search(40) is True
    assert bst.inorder() == [20, 40, 50, 60, 70, 80]


def test_delete_root_node():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    bst.delete(10)

    assert bst.search(10) is False
    assert bst.search(5) is True
    assert bst.search(15) is True


def test_delete_root_with_two_children():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    bst.delete(50)

    assert bst.search(50) is False
    assert bst.size() == 6
    assert bst.inorder() == [20, 30, 40, 60, 70, 80]


def test_delete_only_node():
    bst = BinarySearchTree()
    bst.insert(10)

    bst.delete(10)

    assert bst.search(10) is False
    assert bst.size() == 0


def test_delete_nonexistent_key_raises_error():
    bst = BinarySearchTree()
    bst.insert(10)

    with pytest.raises(KeyDoesNotExist) as exc_info:
        bst.delete(20)

    assert exc_info.value.key == 20


def test_delete_from_empty_tree_raises_error():
    bst = BinarySearchTree()

    with pytest.raises(KeyDoesNotExist):
        bst.delete(10)


# ---------- Size tracking ----------

def test_size_empty_tree():
    bst = BinarySearchTree()
    assert bst.size() == 0


def test_size_after_inserts():
    bst = BinarySearchTree()
    assert bst.size() == 0

    bst.insert(10)
    assert bst.size() == 1

    bst.insert(5)
    assert bst.size() == 2

    bst.insert(15)
    assert bst.size() == 3


def test_size_after_delete():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    assert bst.size() == 3

    bst.delete(5)
    assert bst.size() == 2

    bst.delete(15)
    assert bst.size() == 1

    bst.delete(10)
    assert bst.size() == 0


def test_size_with_duplicate_attempt():
    bst = BinarySearchTree()
    bst.insert(10)

    try:
        bst.insert(10)
    except DuplicateKeyError:
        pass

    assert bst.size() == 1


# ---------- Min/Max operations ----------

def test_min_single_node():
    bst = BinarySearchTree()
    bst.insert(10)
    assert bst.min() == 10


def test_min_multiple_nodes():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.min() == 20


def test_max_single_node():
    bst = BinarySearchTree()
    bst.insert(10)
    assert bst.max() == 10


def test_max_multiple_nodes():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.max() == 80


def test_min_empty_tree_raises_error():
    bst = BinarySearchTree()

    with pytest.raises(ValueError, match="Tree is empty"):
        bst.min()


def test_max_empty_tree_raises_error():
    bst = BinarySearchTree()

    with pytest.raises(ValueError, match="Tree is empty"):
        bst.max()


def test_min_after_deleting_minimum():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40]
    for val in values:
        bst.insert(val)

    bst.delete(20)
    assert bst.min() == 30


def test_max_after_deleting_maximum():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 80]
    for val in values:
        bst.insert(val)

    bst.delete(80)
    assert bst.max() == 70


# ---------- Traversal operations ----------

def test_inorder_traversal():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.inorder() == [20, 30, 40, 50, 60, 70, 80]


def test_inorder_empty_tree():
    bst = BinarySearchTree()
    assert bst.inorder() == []


def test_inorder_single_node():
    bst = BinarySearchTree()
    bst.insert(10)
    assert bst.inorder() == [10]


def test_preorder_traversal():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.preorder() == [50, 30, 20, 40, 70, 60, 80]


def test_preorder_empty_tree():
    bst = BinarySearchTree()
    assert bst.preorder() == []


def test_postorder_traversal():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.postorder() == [20, 40, 30, 60, 80, 70, 50]


def test_postorder_empty_tree():
    bst = BinarySearchTree()
    assert bst.postorder() == []


# ---------- Edge cases and complex scenarios ----------

def test_insert_ascending_order():
    bst = BinarySearchTree()
    values = [1, 2, 3, 4, 5]

    for val in values:
        bst.insert(val)

    assert bst.inorder() == [1, 2, 3, 4, 5]
    assert bst.size() == 5


def test_insert_descending_order():
    bst = BinarySearchTree()
    values = [5, 4, 3, 2, 1]

    for val in values:
        bst.insert(val)

    assert bst.inorder() == [1, 2, 3, 4, 5]
    assert bst.size() == 5


def test_multiple_deletes():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for val in values:
        bst.insert(val)

    bst.delete(20)
    bst.delete(40)
    bst.delete(70)

    assert bst.size() == 8
    assert bst.inorder() == [10, 25, 30, 35, 45, 50, 60, 80]


def test_delete_and_reinsert():
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    bst.delete(5)
    assert bst.search(5) is False

    bst.insert(5)
    assert bst.search(5) is True
    assert bst.size() == 3


def test_large_tree():
    bst = BinarySearchTree()
    values = list(range(1, 101))

    for val in values:
        bst.insert(val)

    assert bst.size() == 100
    assert bst.min() == 1
    assert bst.max() == 100
    assert all(bst.search(val) for val in values)


def test_traversal_after_deletes():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    bst.delete(30)
    bst.delete(70)

    assert bst.inorder() == [20, 40, 50, 60, 80]
    assert bst.preorder() == [50, 40, 20, 80, 60]
    assert bst.postorder() == [20, 40, 60, 80, 50]


# ---------- New utility methods ----------

def test_is_empty():
    bst = BinarySearchTree()
    assert bst.is_empty() is True

    bst.insert(10)
    assert bst.is_empty() is False

    bst.delete(10)
    assert bst.is_empty() is True


def test_clear():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40]
    for val in values:
        bst.insert(val)

    assert bst.size() == 5
    assert bst.is_empty() is False

    bst.clear()

    assert bst.size() == 0
    assert bst.is_empty() is True
    assert bst.search(50) is False


def test_clear_empty_tree():
    bst = BinarySearchTree()
    bst.clear()
    assert bst.is_empty() is True


def test_height_empty_tree():
    bst = BinarySearchTree()
    assert bst.height() == -1


def test_height_single_node():
    bst = BinarySearchTree()
    bst.insert(10)
    assert bst.height() == 0


def test_height_balanced_tree():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    assert bst.height() == 2


def test_height_unbalanced_tree():
    bst = BinarySearchTree()
    values = [1, 2, 3, 4, 5]
    for val in values:
        bst.insert(val)

    assert bst.height() == 4


def test_len_operator():
    bst = BinarySearchTree()
    assert len(bst) == 0

    bst.insert(10)
    bst.insert(5)
    bst.insert(15)

    assert len(bst) == 3

    bst.delete(5)
    assert len(bst) == 2


def test_contains_operator():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)

    assert 50 in bst
    assert 30 in bst
    assert 70 in bst
    assert 100 not in bst


def test_iter():
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)

    result = list(bst)
    assert result == [20, 30, 40, 50, 60, 70, 80]


def test_iter_empty_tree():
    bst = BinarySearchTree()
    assert list(bst) == []


def test_iter_in_for_loop():
    bst = BinarySearchTree()
    values = [5, 3, 7, 1, 9]
    for val in values:
        bst.insert(val)

    result = []
    for key in bst:
        result.append(key)

    assert result == [1, 3, 5, 7, 9]


def test_str_empty_tree():
    bst = BinarySearchTree()
    assert str(bst) == "BinarySearchTree(empty)"


def test_str_with_nodes():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)

    s = str(bst)
    assert "size=3" in s
    assert "root=50" in s


def test_repr():
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)

    r = repr(bst)
    assert "BinarySearchTree" in r
    assert "[30, 50, 70]" in r

import pytest
from hashmap import DynamicHashMap


def test_put_and_get():
    hm = DynamicHashMap()
    hm.put("a", 1)
    hm.put("b", 2)

    assert hm.get("a") == 1
    assert hm.get("b") == 2


def test_put_overwrite():
    hm = DynamicHashMap()
    hm.put("a", 1)
    hm.put("a", 99)

    assert hm.get("a") == 99
    assert hm.size() == 1


def test_get_default():
    hm = DynamicHashMap()
    assert hm.get("missing") is None
    assert hm.get("missing", 42) == 42


def test_contains():
    hm = DynamicHashMap()
    hm.put("x", 10)

    assert hm.contains("x") is True
    assert hm.contains("y") is False


def test_remove():
    hm = DynamicHashMap()
    hm.put("a", 1)
    hm.put("b", 2)

    hm.remove("a")

    assert hm.get("a") is None
    assert hm.size() == 1


def test_remove_missing_key():
    hm = DynamicHashMap()
    with pytest.raises(KeyError):
        hm.remove("missing")


def test_size():
    hm = DynamicHashMap()
    assert hm.size() == 0

    hm.put("a", 1)
    hm.put("b", 2)

    assert hm.size() == 2


def test_clear():
    hm = DynamicHashMap()
    hm.put("a", 1)
    hm.put("b", 2)

    hm.clear()

    assert hm.size() == 0
    assert hm.contains("a") is False
    assert hm.contains("b") is False


def test_collision_handling():
    hm = DynamicHashMap(initial_capacity=4)

    # these collide since 1 % 4 == 5 % 4
    hm.put(1, "one")
    hm.put(5, "five")

    assert hm.get(1) == "one"
    assert hm.get(5) == "five"
    assert hm.size() == 2


def test_remove_from_collision_chain():
    hm = DynamicHashMap(initial_capacity=4)

    hm.put(1, "one")
    hm.put(5, "five")
    hm.put(9, "nine")

    hm.remove(5)

    assert hm.get(1) == "one"
    assert hm.get(5) is None
    assert hm.get(9) == "nine"
    assert hm.size() == 2


def test_resize():
    hm = DynamicHashMap(initial_capacity=4, load_factor=0.75)

    hm.put("a", 1)
    hm.put("b", 2)
    hm.put("c", 3)

    assert hm.capacity == 8
    assert hm.size() == 3
    assert hm.get("a") == 1
    assert hm.get("b") == 2
    assert hm.get("c") == 3


def test_resize_preserves_collisions():
    hm = DynamicHashMap(initial_capacity=2, load_factor=1)

    hm.put(0, "zero")
    hm.put(2, "two")

    assert hm.capacity == 4
    assert hm.get(0) == "zero"
    assert hm.get(2) == "two"


# ---------- Dict-like interface tests ----------

def test_len():
    hm = DynamicHashMap()
    assert len(hm) == 0

    hm.put("a", 1)
    hm.put("b", 2)
    assert len(hm) == 2

    hm.remove("a")
    assert len(hm) == 1


def test_getitem():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["b"] = 2

    assert hm["a"] == 1
    assert hm["b"] == 2


def test_getitem_missing_raises_keyerror():
    hm = DynamicHashMap()
    with pytest.raises(KeyError):
        _ = hm["missing"]


def test_setitem():
    hm = DynamicHashMap()
    hm["x"] = 10
    hm["y"] = 20

    assert hm.get("x") == 10
    assert hm.get("y") == 20
    assert len(hm) == 2


def test_setitem_overwrite():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["a"] = 99

    assert hm["a"] == 99
    assert len(hm) == 1


def test_contains_operator():
    hm = DynamicHashMap()
    hm["x"] = 10

    assert "x" in hm
    assert "y" not in hm


# ---------- Iteration tests ----------

def test_keys():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["b"] = 2
    hm["c"] = 3

    keys = list(hm.keys())
    assert len(keys) == 3
    assert set(keys) == {"a", "b", "c"}


def test_keys_empty():
    hm = DynamicHashMap()
    assert list(hm.keys()) == []


def test_values():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["b"] = 2
    hm["c"] = 3

    values = list(hm.values())
    assert len(values) == 3
    assert set(values) == {1, 2, 3}


def test_values_empty():
    hm = DynamicHashMap()
    assert list(hm.values()) == []


def test_items():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["b"] = 2
    hm["c"] = 3

    items = list(hm.items())
    assert len(items) == 3
    assert set(items) == {("a", 1), ("b", 2), ("c", 3)}


def test_items_empty():
    hm = DynamicHashMap()
    assert list(hm.items()) == []


def test_iteration_with_collisions():
    hm = DynamicHashMap(initial_capacity=4)
    hm.put(1, "one")
    hm.put(5, "five")
    hm.put(9, "nine")

    keys = set(hm.keys())
    values = set(hm.values())

    assert keys == {1, 5, 9}
    assert values == {"one", "five", "nine"}


# ---------- Edge case tests ----------

def test_string_hashing():
    hm = DynamicHashMap()
    hm["hello"] = 1
    hm["world"] = 2
    hm["python"] = 3

    assert hm["hello"] == 1
    assert hm["world"] == 2
    assert hm["python"] == 3
    assert len(hm) == 3


def test_large_hashmap():
    hm = DynamicHashMap()

    for i in range(100):
        hm[i] = i * 2

    assert len(hm) == 100

    for i in range(100):
        assert hm[i] == i * 2


def test_resize_multiple_times():
    hm = DynamicHashMap(initial_capacity=2, load_factor=0.75)

    for i in range(20):
        hm[i] = i

    assert len(hm) == 20
    assert hm.capacity >= 32

    for i in range(20):
        assert hm[i] == i


def test_mixed_key_types():
    hm = DynamicHashMap()
    hm[1] = "int key"
    hm["one"] = "string key"
    hm[2] = "another int"
    hm["two"] = "another string"

    assert hm[1] == "int key"
    assert hm["one"] == "string key"
    assert hm[2] == "another int"
    assert hm["two"] == "another string"
    assert len(hm) == 4


def test_clear_and_reuse():
    hm = DynamicHashMap()
    hm["a"] = 1
    hm["b"] = 2

    hm.clear()
    assert len(hm) == 0

    hm["c"] = 3
    hm["d"] = 4

    assert len(hm) == 2
    assert hm["c"] == 3
    assert hm["d"] == 4


def test_iteration_after_resize():
    hm = DynamicHashMap(initial_capacity=2, load_factor=0.75)

    for i in range(10):
        hm[i] = i * 10

    keys = set(hm.keys())
    values = set(hm.values())

    assert keys == set(range(10))
    assert values == {i * 10 for i in range(10)}


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


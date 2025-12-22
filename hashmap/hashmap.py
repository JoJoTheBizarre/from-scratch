from typing import Any

hashable = int | str


class Node:
    def __init__(self, key: hashable, value: Any):
        self.key = key
        self.value = value
        self.next = None


class Hasher:
    def __init__(self, size: int):
        self.size = size

    def set_size(self, size: int):
        self.size = size

    def hash(self, key: hashable) -> int:
        if isinstance(key, int):
            return key % self.size
        elif isinstance(key, str):
            hash_code = 0
            for c in key:
                hash_code = (hash_code * 31 + ord(c)) % self.size
            return hash_code
        else:
            raise TypeError(f"Unsupported key type: {type(key)}")


class DynamicHashMap:
    def __init__(self, initial_capacity: int = 8, load_factor: float = 0.75):
        self.load_factor = load_factor
        self.capacity = initial_capacity
        self.table = [None] * self.capacity
        self.hasher = Hasher(self.capacity)
        self.num_items = 0

    # ---------- Core operations ----------

    def put(self, key: hashable, value: Any):
        index = self.hasher.hash(key)
        current = self.table[index]

        if current is None:
            self.table[index] = Node(key, value)
            self.num_items += 1
        else:
            while True:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    current.next = Node(key, value)
                    self.num_items += 1
                    break
                current = current.next

        if self.num_items / self.capacity >= self.load_factor:
            self._resize(self.capacity * 2)


    def get(self, key: hashable, default=None):
        index = self.hasher.hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return default

    def remove(self, key: hashable):
        index = self.hasher.hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next

                self.num_items -= 1
                return

            prev = current
            current = current.next

        raise KeyError(key)

    # ---------- Utility methods ----------

    def contains(self, key: hashable) -> bool:
        index = self.hasher.hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return True
            current = current.next

        return False

    def size(self) -> int:
        return self.num_items
    
    def clear(self):
        self.table = [None] * self.capacity
        self.num_items = 0

    # ---------- Resizing ----------

    def _resize(self, new_capacity: int):
        old_table = self.table

        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.hasher.set_size(new_capacity)
        self.num_items = 0

        for head in old_table:
            current = head
            while current:
                self.put(current.key, current.value)
                current = current.next

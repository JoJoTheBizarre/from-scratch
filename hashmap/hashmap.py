from typing import Any

hashable = int | str

class Node():
    def __init__(self, value: int, key: hashable):
        self.value = value
        self.key = key
        self.next = None

class Hasher:
        def __init__(self, size):
            self.size = size
            self.type_mapping = {
                int: self._integer_hash,
                str: self._string_hash,
            }

        def set_size(self, size: int):
            self.size = size

        def add_handler(self, type: type, handler: callable):
            if not callable(handler):
                raise TypeError("handler must be callable :(")
            self.type_mapping[type] = handler 

        def hash(self, key):
            key_type = type(key)
            if key_type not in self.type_mapping:
                raise TypeError(f"Key type is not handled: {key_type}")
            return self.type_mapping[key_type](key)

        def _integer_hash(self, key: int) -> int:
            return key % self.size

        def _string_hash(self, key: str) -> int:
            hash_code = 0
            for c in key:
                hash_code = (hash_code * 31 + ord(c)) % self.size
            return hash_code

class DynamicHashMap():
    def __init__(self, initial_capacity: int= 8, load_factor: float=0.75):
        """
        Docstring for __init__
        
        :param load_factor: percentage load of the table = 
        """
        self.load_factor = load_factor
        self.size = initial_capacity
        self.table = [None for _ in range(self.size)]
        self.hasher = Hasher(self.size)
        self.num_items = 0

    

    def put(self, key: hashable, value: Any):
        hash_code = self.hasher.hash(key)
        current_node = self.table[hash_code]
        #bucket is empty make a new entry
        if current_node is None:
            new_node = Node(value=value, key=key)
            self.table[hash_code] = new_node
            self.num_items += 1
            return
        #a node already exists in the bucket
        else:
            while current_node:
                if current_node.key == key:
                    current_node.value = value
                    return
                else:
                    if current_node.next is None: #new item in the hashmap
                        current_node.next = Node(value=value, key=key)
                        self.num_items += 1
                        return
                    else:
                        current_node = current_node.next
import random
import time


class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            if self.head:
                self.head.prev = node
            self.head = node
            node.prev = None
            if self.tail is None:
                self.tail = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key: node
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return None

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def invalidate_range_containing_index(self, index):
        # Збираємо ключі, діапазони яких містять index
        keys_to_remove = [
            key for key in self.cache
            if key[0] <= index <= key[1]
        ]
        for key in keys_to_remove:
            node = self.cache[key]
            self.list.remove(node)
            del self.cache[key]


def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, cache, L, R):
    key = (L, R)
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result


def update_with_cache(array, cache, index, value):
    array[index] = value
    cache.invalidate_range_containing_index(index)


def generate_queries(N, Q):
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:
            L = random.randint(0, N-1)
            R = random.randint(L, N-1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N-1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))
    return queries


def main():
    N = 100_000
    Q = 50_000

    array_no_cache = [random.randint(1, 100) for _ in range(N)]
    array_cache = array_no_cache.copy()

    queries = generate_queries(N, Q)

    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            _, L, R = q
            _ = range_sum_no_cache(array_no_cache, L, R)
        else:
            _, index, value = q
            update_no_cache(array_no_cache, index, value)
    no_cache_time = time.time() - start

    cache = LRUCache(capacity=1000)
    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            _, L, R = q
            _ = range_sum_with_cache(array_cache, cache, L, R)
        else:
            _, index, value = q
            update_with_cache(array_cache, cache, index, value)
    cache_time = time.time() - start

    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")


if __name__ == "__main__":
    main()

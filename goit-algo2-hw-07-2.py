import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


class Node:
    def __init__(self, data, parent=None):
        self.data = data  # (key, value)
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node((key, value))
            return
        self._insert_node((key, value), self.root)

    def _insert_node(self, data, current_node):
        key = data[0]
        curr_key = current_node.data[0]
        if key < curr_key:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
                self._splay(current_node.left_node)
        elif key > curr_key:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)
                self._splay(current_node.right_node)
        else:
            current_node.data = data
            self._splay(current_node)

    def find(self, key):
        node = self.root
        while node is not None:
            if key < node.data[0]:
                node = node.left_node
            elif key > node.data[0]:
                node = node.right_node
            else:
                self._splay(node)
                return node.data[1]
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:  # Zig
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node and
                node.parent == node.parent.parent.left_node
            ):  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node and
                node.parent == node.parent.parent.right_node
            ):  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child

# --- Fibonacci з LRU Cache ---


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

# --- Fibonacci з Splay Tree ---


def fibonacci_splay(n, tree):
    cached = tree.find(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, val)
    return val


def measure_time(func, *args, repeats=5):
    timer = timeit.Timer(lambda: func(*args))
    times = timer.repeat(repeat=repeats, number=1)
    return sum(times) / len(times)


def main():
    ns = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)'}")
    print("-" * 50)

    for n in ns:
        fibonacci_lru.cache_clear()
        splay_tree = SplayTree()

        t_lru = measure_time(fibonacci_lru, n)
        t_splay = measure_time(fibonacci_splay, n, splay_tree)

        lru_times.append(t_lru)
        splay_times.append(t_splay)

        print(f"{n:<10}{t_lru:<20.8f}{t_splay:.8f}")

    plt.plot(ns, lru_times, label="LRU Cache")
    plt.plot(ns, splay_times, label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()

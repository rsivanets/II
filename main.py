import sys
import copy

sys.setrecursionlimit(99999999)
# избегаем зацикливания храним все состояния
total_states = []

initial_state = [
    [-1, 4, 3],
    [6, 2, 1],
    [7, 5, 8]
]


def pretty_print(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))


def get_unique_rows_in_array(arr):
    unique = []
    for i in arr:
        if i not in unique:
            unique.append(i)
    return unique


class Game:
    initial_state = []

    def __init__(self, state):
        self.initial_state = state

    def pretty_print(self, matrix):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

    def is_win(self, state):
        winner_state = [
            # [4, 2, 3],
            # [6, 5, 1],
            # [7, 8, -1]
            [1, 2, 3],
            [4, -1, 5],
            [6, 7, 8]
        ]
        return state == winner_state

    def get_flat_state(self, state):
        return [item for sublist in state for item in sublist]

    def find_where_empty(self, state):
        flat_state = self.get_flat_state(state)
        index = flat_state.index(-1)
        return [index // 3, index % 3]

    def move_to_top(self, cords):
        cords[0] -= 1
        return cords

    def move_to_left(self, cords):
        cords[1] -= 1
        return cords

    def move_to_right(self, cords):
        cords[1] += 1
        return cords

    def move_to_bottom(self, cords):
        cords[0] += 1
        return cords

    @staticmethod
    def is_valid_coordinates(coordinates):
        return 0 <= coordinates[0] <= 2 and 0 <= coordinates[1] <= 2

    def __find_potential_steps_by_coordinates(self, state):
        empty_coordinates = self.find_where_empty(state.copy())
        bottom = self.move_to_bottom(empty_coordinates.copy())
        right = self.move_to_right(empty_coordinates.copy())
        left = self.move_to_left(empty_coordinates.copy())
        top = self.move_to_top(empty_coordinates.copy())
        potential_coordinates = [
            bottom,
            right,
            left,
            top
        ]
        return list(filter(self.is_valid_coordinates, potential_coordinates))

    def move_empty_with_coords(self, coordinates, state, empty_coordinates):
        value_from_state = state[coordinates[0]][coordinates[1]]
        state[empty_coordinates[0]][empty_coordinates[1]] = value_from_state
        state[coordinates[0]][coordinates[1]] = -1
        return state

    def get_potential_steps(self):
        state = self.initial_state.copy()
        potentials = self.__find_potential_steps_by_coordinates(state.copy())
        empties = self.find_where_empty(state).copy()
        potentials_states = []
        for i in potentials:
            copied_state = copy.deepcopy(state)
            modified_state = self.move_empty_with_coords(i, copied_state, empties)
            if modified_state not in total_states:
                self.append = total_states.append(modified_state)
                potentials_states.append(modified_state)
        return potentials_states


class Node:
    state: Game
    parent: "Node"
    children: list = []
    is_winner: bool
    level = 1

    def __init__(self, parent, state, level):
        self.parent = parent
        self.state = state
        self.level = level
        self.is_winner = self.state.is_win(state.initial_state)

def get_full_copy(state):
    new_state = []
    for i in state:
        new_state.append(i)
    return new_state


def get_new_leafs_by_node(node):
    steps = node.state.get_potential_steps()
    # time.sleep(7)
    new_nodes = []
    for state in steps:
        game = Game(get_full_copy(state))
        new_node = Node(parent=node, state=game, level=node.level + 1)
        node.children.append(new_node)
        new_nodes.append(new_node)
    return new_nodes


class Searcher:
    queue = []
    visited_states = []
    count = 0
    value = "2"

    def visit_queue(self, node: Node):
        self.count += 1
        if node.state.initial_state in self.visited_states:
            print('skip')
           
            self.visit_queue(self.queue.pop(0))
        else:
            self.visited_states.append(node.state.initial_state)
        if node.state.is_win(node.state.initial_state):
            print(f"TOTAL NODES CREATED: {self.count}")
            return node
        else:
            if self.value == "2":
                val = input("Ввведите 2 чтобы сделать следующий шаг, введите что то другое чтобы избежать вывода")
                self.value = val
                print("=============")
                pretty_print(node.state.initial_state)
                print("============")
            leafs = get_new_leafs_by_node(node)
            for child in leafs:
                self.queue.append(child)
            return self.visit_queue(self.queue.pop(0))

    def search_with_iterative_depth(self):
        initial_game = Game(initial_state.copy())
        total_states.append(initial_state)
        initital_node = Node(parent=None, state=initial_game, level=1)
        winner_node = self.visit_queue(initital_node)
        return winner_node
    
    @staticmethod
    def print_results(node):
        queue = []
        parent = node.parent
        while parent:
            queue.append(node)
            node = parent
            parent = node.parent
        queue.reverse()
        print(f'TOTAL RESULT STEPS COUNT: {len(queue)}')
        for step in queue:
            print("============== STEP =================")
            pretty_print(step.state.initial_state)
            print("============ END STEP ===============")
            


node = Searcher().search_with_iterative_depth()
Searcher.print_results(node)
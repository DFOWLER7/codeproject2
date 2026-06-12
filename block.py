import random
import heapq

# World settings
ROWS = 15
COLS = 15
BLOCK_PERCENTAGE = 0.10


def create_world():
    """
    Creates a 15x15 grid where 10% of the nodes are blocked.
    0 = pathable
    1 = blocked
    """
    world = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    total_blocks = int(ROWS * COLS * BLOCK_PERCENTAGE)
    blocks_placed = 0

    while blocks_placed < total_blocks:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        if world[row][col] == 0:
            world[row][col] = 1
            blocks_placed += 1

    return world


def display_world(world, path=None, start=None, goal=None):
    """
    Displays the world in the console.
    . = open/pathable node
    # = blocked node
    S = start node
    G = goal node
    * = final path
    """
    if path is None:
        path = []

    print("\nGenerated 15x15 World:")
    print("   " + " ".join(f"{col:2}" for col in range(COLS)))

    for row in range(ROWS):
        print(f"{row:2} ", end="")

        for col in range(COLS):
            current = (row, col)

            if current == start:
                print(" S", end=" ")
            elif current == goal:
                print(" G", end=" ")
            elif current in path:
                print(" *", end=" ")
            elif world[row][col] == 1:
                print(" #", end=" ")
            else:
                print(" .", end=" ")

        print()


def manhattan_distance(node, goal):
    """
    Calculates Manhattan distance between two nodes.
    Manhattan distance = |x1 - x2| + |y1 - y2|
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def get_neighbors(node, world):
    """
    Returns valid pathable neighboring nodes.
    Movement is allowed up, down, left, and right.
    """
    row, col = node

    possible_moves = [
        (row - 1, col),  # up
        (row + 1, col),  # down
        (row, col - 1),  # left
        (row, col + 1)   # right
    ]

    neighbors = []

    for new_row, new_col in possible_moves:
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if world[new_row][new_col] == 0:
                neighbors.append((new_row, new_col))

    return neighbors


def reconstruct_path(came_from, current):
    """
    Rebuilds the path from goal back to start.
    """
    path = []

    while current in came_from:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path


def astar(world, start, goal):
    """
    A* pathfinding algorithm.
    Uses Manhattan distance as the heuristic.
    """
    open_list = []

    # heap entry: (f_score, node)
    heapq.heappush(open_list, (0, start))

    came_from = {}

    g_score = {}
    f_score = {}

    for row in range(ROWS):
        for col in range(COLS):
            g_score[(row, col)] = float("inf")
            f_score[(row, col)] = float("inf")

    g_score[start] = 0
    f_score[start] = manhattan_distance(start, goal)

    open_set = {start}

    while open_list:
        current = heapq.heappop(open_list)[1]
        open_set.discard(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, world):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)

                if neighbor not in open_set:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
                    open_set.add(neighbor)

    return None


def get_node_input(prompt, world):
    """
    Gets and validates user input for a node.
    User enters row and column.
    """
    while True:
        try:
            print(prompt)
            row = int(input("Enter row number 0-14: "))
            col = int(input("Enter column number 0-14: "))

            if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                print("Invalid location. Row and column must be between 0 and 14.")
            elif world[row][col] == 1:
                print("That node is blocked. Please choose a pathable node.")
            else:
                return (row, col)

        except ValueError:
            print("Invalid input. Please enter numbers only.")


def main():
    world = create_world()

    while True:
        display_world(world)

        start = get_node_input("\nSelect the START node.", world)
        goal = get_node_input("\nSelect the GOAL node.", world)

        if start == goal:
            print("\nStart and goal are the same node.")
            display_world(world, start=start, goal=goal)
        else:
            path = astar(world, start, goal)

            if path:
                print("\nPath found!")
                print("Path nodes:")

                full_path = [start] + path
                for node in full_path:
                    print(f"[{node[0]}, {node[1]}]", end=" ")

                print()
                display_world(world, path=path, start=start, goal=goal)
            else:
                print("\nNo path could be found.")
                display_world(world, start=start, goal=goal)

        again = input("\nWould you like to choose another start and goal? (y/n): ").lower()

        if again != "y":
            print("Program ended.")
            break


if __name__ == "__main__":
    main()

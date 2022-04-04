import copy
from queue import PriorityQueue
import time


def position_of_val(val, c_state):
    """
    get the position of the value and return the row and column
    :param val: the value
    :param c_state: the current state of the puzzle
    :return: the coordinates of the value
    """
    # the indexing starts at 1 with the row coming before the column so [1,1] would be the top left value

    row_num = 1
    for row in c_state:
        col_num = 0
        for place in row:
            col_num += 1
            if val == place:
                # print("the row of %d is %d, %d\n" % (val, row_num, col_num))
                return [row_num, col_num]
        row_num += 1


def val_at_position(x_val, y_val, current_state):
    """
    Function to get the value at a place in the puzzle
    :param x_val: the row number (1, 2, 3)
    :param y_val: the col number (1, 2, 3)
    :param current_state: the current state
    :return: returns the value at the coordinates specified
    """
    # takes coordinates 1,2,3,4 of x and y to return value at that spot
    return current_state[x_val - 1][y_val - 1]


def distance_for_individual(val, c_state, g_state):
    """
    calculate the distance between the current state and the goal state for a given value
    :param val: value you want to know about
    :param c_state: the current state
    :param g_state: the goal state
    :return: the x + y distance of how far the value is from its desired positon
    """

    # get the positions of the value in the current and final position
    current_pos = position_of_val(val, c_state)
    final_pos = position_of_val(val, g_state)

    # get the x and y value between the current and final position
    x_dist = abs(current_pos[0] - final_pos[0])
    y_dist = abs(current_pos[1] - final_pos[1])

    return int(x_dist + y_dist)


def manhattan(c_state, g_state):
    """
    function to calculate the manhattan distance of a puzzle
    :param c_state: current state of the puzzle
    :param g_state: goal state of the puzzle
    :return: the manhattan distance of the current state to the goal state
    """

    tiles = [1, 2, 3, 4, 5, 6, 7, 8]

    # function to get the total manhattan distance
    distance = 0
    for i in tiles:
        # for distance in individual
        dist = distance_for_individual(i, c_state, g_state)
        if dist != 0:
            # distance to the goal state
            distance += dist

    return int(distance)


def move(val, current_state):
    """
    moves the value around the puzzle if it is adjacent to 0
    :param val: desired value to move
    :param current_state: the current state of the puzzle
    :return: return the next state with the moved value
    """
    # function to move a value in the game
    c_state = copy.deepcopy(current_state)
    pos_of_val = position_of_val(val, current_state)
    pos_of_zero = position_of_val(0, current_state)

    c_state[pos_of_val[0]-1][pos_of_val[1]-1] = 0
    c_state[pos_of_zero[0]-1][pos_of_zero[1]-1] = val

    return c_state


def moves_and_weight(g, current_state, goal_state: list, directions):
    """
    generates a new child node and information around it derived from the parent node information
    :param g: g value of parent node
    :param current_state: current state of parent node
    :param goal_state: goal node
    :param directions: the directions so far, in the format [0,1,2,3] 0: right 1: left 2: down 3: up
    :return: a list in the form [f(x), g(x), child state that corresponds to f and g, directions with new direction]
    """
    c_state = copy.deepcopy(current_state)
    empty_pos = position_of_val(0, current_state)
    x_vals = [0, 0, 1, 1]
    y_vals = [1, 1, 0, 0]
    more_pos = [-1, 1, -1, 1]
    next_to = []
    # gets the positions adjacent to the 0 and checks if they are valid
    # if they are valid they are added to the queue
    for j in range(4):
        if 3 >= empty_pos[0] - x_vals[j] * more_pos[j] > 0 and 3 >= empty_pos[1] - y_vals[j] * more_pos[j] > 0:
            # next to is the coordinates of the positions next to 0
            x_pos = empty_pos[0] - x_vals[j] * more_pos[j]
            y_pos = empty_pos[1] - y_vals[j] * more_pos[j]
            next_to.append([x_pos, y_pos, j])
            # j is the direction of the move, where: 0: right, 1: left, 2: down, 3: up

    queue = []

    for i in next_to:
        xv = i[0]
        yv = i[1]
        direction = i[2]
        number = val_at_position(xv, yv, current_state)

        next_node = move(number, current_state)

        # this is the f(x) where g is g(x) and manhattan is the h(x)
        h = manhattan(next_node, goal_state)
        f = g + h

        # queue is appended with the weight and the new state
        queue.append((f, number, direction))

    queue.sort()

    weights_and_new_states = []
    g += 1

    # creates all available child nodes
    for i in queue:
        num = i[1]
        weight = i[0]
        directions1 = copy.deepcopy(directions)
        directions1.append(i[2])
        c_state2 = copy.deepcopy(c_state)
        new_state = move(num, c_state2)
        weights_and_new_states.append([weight, g, new_state, directions1])

    return weights_and_new_states


def search(s_state, goal_state):
    """
    the function to perform the search
    :param s_state: start state of the puzzle
    :param goal_state: goal state of the puzzle
    :return: the final path that the puzzle took in the form [1,2,3,4] (0: right 1: left 2: down 3: up) and number of iterations
    """

    queue = PriorityQueue()
    # use a priority queue for increased efficiency
    directions = []
    current_state = s_state
    g = 0
    # generate child nodes from start state and empty directions list then adds them to queue
    maw = moves_and_weight(g, current_state, goal_state, directions)
    for i in maw:
        queue.put(i)

    # a closed list as a set for efficiency
    closed = set()
    iterations = 0
    final_path = []
    won = False

    while not won:
        # plays until it is won. This can be a negative though as there are puzzles which cannot be won
        i = queue.get()
        if str(i[3]) not in closed:
            iterations += 1
            current_state = i[2]
            closed.add(str(i[3]))

            if current_state == goal_state:
                final_path = i[3]
                won = True

            next_nodes = moves_and_weight(i[1], i[2], goal_state, i[3])

            for j in next_nodes:
                queue.put(j)

    return final_path, iterations


def main(s_state, g_state):
    """
    main function for the puzzle that prints out necessary information and calls necessary functions
    :param s_state: start state of puzzle
    :param g_state: goal state of puzzle
    """
    dist = manhattan(s_state, g_state)

    print("Start state:")
    for i in s_state:
        print(i)
    print("Minimum length: %d" % dist)
    print("Running...")

    start_time = time.time()
    searched = search(s_state, g_state)

    if searched:
        print("\nPuzzle completed")
        print("Time taken: %d seconds\n" % (time.time()-start_time))
        print("Path: ")
        print(searched[0])
        print("Iteration count: %i" % searched[1])
        print("Puzzle path: ")
        path(s_state, searched[0])


def path(s_state, taken):
    """

    :param s_state:
    :param taken:
    :return:
    """

    c_state = copy.deepcopy(s_state)
    for i in taken:
        zero = position_of_val(0, c_state)
        if i == 0:
            # if move taken is right
            moving = [zero[0], zero[1] + 1]
        elif i == 1:
            # if move taken is left
            moving = [zero[0], zero[1] - 1]
        elif i == 2:
            # if move taken is down
            moving = [zero[0] + 1, zero[1]]
        elif i == 3:
            # if move taken is up
            moving = [zero[0] - 1, zero[1]]

        # recreates the path by moving the 0 around the puzzle
        pos = val_at_position(moving[0], moving[1], c_state)
        c_state = move(pos, c_state)
        for j in c_state:
            print(j)
        print("")


if __name__ == '__main__':
    # 0 represents an empty square that tiles can be moved into
    vals = [1, 2, 3, 4, 5, 6, 7, 8]
    """start_state = [[3, 1, 2],
                   [4, 7, 5],
                   [0, 6, 8]]"""

    start_state = [[7, 2, 4],
                   [5, 0, 6],
                   [8, 3, 1]]

    goal_state = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]

    g_s = [start_state, goal_state]

    print("Current configuration:\n")
    for i in g_s:
        for j in i:
            print(j)
        print()

    config_choice = False
    while not config_choice:
        choice = input("Would you like to use the current configuration? y/n: ")
        if choice.lower() == 'y':
            main(start_state, goal_state)
            config_choice = True
        elif choice.lower() == 'n':
            start = input("Please input start state in the following format where 0 is the empty space:\n"
                          "'123456780' to get the input [[1, 2, 3], [4, 5, 6], [7, 8, 0]] ")
            goal = input("Please input goal state in the same format: ")
            start_list = []
            goal_list = []

            for i in range(3):
                temp = []
                for j in range(3):
                    temp.append(int(start[(i*3) + j]))
                start_list.append(temp)

            for i in range(3):
                temp = []
                for j in range(3):
                    temp.append(int(goal[(i*3) + j]))
                goal_list.append(temp)

            main(start_list, goal_list)
            config_choice = True
        else:
            print("Please enter a valid input")

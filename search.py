# search.py
# contains the code to search for soluttion to puzzle
# handles A* and IDA*
# user input control specific searches
# outputs results to a csv file
import time
import argparse
import math

from OpenList import *
import puzzle


def search(initial_state, goal, depth):  # search for solution path
    # depth == 1000 ? True means A* : False means IDA*

    incumbent = None #incumbent is the current node that is the best path

    if depth == 1000:
        open_list = PriorityQueue()
        closed_list = {}
    else:
        open_list = Stack()
        closed_list = []
        count = 0

    moves = (puzzle.move_right, puzzle.move_down,
             puzzle.move_left, puzzle.move_up)

    initial_state.wh = initial_state.h * 1
    open_list.add_state(initial_state)

    #while open != 0 and not interrupted do:
    while len(open_list) > 0:  # Search

        # pop the minimum from open list
        n = (open_list.pop_state())

        # Add node to closed list or increment count
        if (incumbent is None) or (n.c + n.h < incumbent.c + incumbent.h):
            closed_list[n] = n
            expanded = len(closed_list) #making the length of the closed_list


            children = []
            for move in moves:  # generate valid children
                try:
                    children.append(move(n))
                except ValueError:
                    continue

            for child in children:  # calculate children heuristics
                child.calculate_h()
                child.wh = child.h * 1

            children.sort(key=lambda x: x.h)

            for child in children:  # add valid children to open list
                if incumbent is None or ((child.c + child.h)  < (incumbent.c + incumbent.h)):

                    if child == goal:  # return node and stats if goal
                        incumbent = child

                    elif child in closed_list and ((child.c < closed_list[child].c )):
                        open_list.add_state(child)
                        closed_list.pop(child)

                    else:
                        open_list.add_state(child)


    return incumbent, len(closed_list), len(open_list)



def main(width, heuristic, state, itd):
    # pass settings to puzzle module
    size = width ** 2
    puzzle.settings_init(width, size, heuristic)

    # Define puzzle goal
    gboard = list(x for x in range(1, size))
    gboard.append(0)
    goal = puzzle.State(gboard, None)

    # Define initial state
    if state is not None:
        try:
            if len(state) == size:
                iboard = [0 if x == "_" else int(x) for x in state]
                initial_state = puzzle.State(iboard, None)
            else:
                raise ValueError("Invalid state for given width.")
            if initial_state.is_solvable() is False:
                raise ValueError("Initial state: ", str(
                    initial_state), "is not solvable.")
        except ValueError as err:
            print(state)
            print(err)
            return
    else:
        initial_state = puzzle.generate_initial_state()

    initial_state.calculate_h()

    # IDA* depth is determined by the h(n) of the initial state since the heuristic is admissible
    # 1000 is a flag to run A* instead of IDA*
    if itd is True:
        depth = initial_state.h
    else:
        depth = 1000

    # Run search
    solution, closed_expanded, open_remaining = None, None, None
    start_time = time.time()
    while solution is None:
        try:
            solution, closed_expanded, open_remaining = search(
                initial_state, goal, depth)
        except ValueError as err:
            if itd is True:
                depth += 1
            else:
                print(err)
                return
    run_time = time.time() - start_time

    # Build path
    ptr = solution
    path = []
    while ptr is not None:
        path.append(str(ptr))
        ptr = ptr.parent

    path.reverse()

    # Output stats to file
    results = ", ".join(map(str, [size - 1, path[0], solution.c, heuristic,
                                  itd, closed_expanded, open_remaining, run_time]))
    f = open("results.csv", "a")
    f.write(results + "\n")
    f.close()

    # Print results
    print("(", closed_expanded, ", 'entries expanded. Queue still has ', ",
          open_remaining, ")", sep="")
    print("(", "'tileSearch.py:', ", solution.c, ", 'moves')", sep="")
    print("(", "'took', ", run_time, ", 'secs')", sep="")
    print(path)


def user_input():
    # Get user input
    parser = argparse.ArgumentParser(
        description="A program to solve sliding tile puzzles",
        epilog="example: python search.py -w 4 --heuristic linear -s 1 2 3 4 5 6 7 8 9 10 11 _ 13 14 15 12 -i")
    parser.add_argument("-w, --width",
                        nargs="?",
                        help="width of puzzle to solve. default = 3",
                        type=int,
                        default=3,
                        dest="width")
    parser.add_argument("--heuristic",
                        nargs="?",
                        choices=["number", "manhattan", "linear"],
                        help="heuristic to be used. default = manhattan",
                        type=str,
                        default="manhattan",
                        dest="heuristic")
    parser.add_argument("-s, --state",
                        nargs="*",
                        help="initial state. default = random",
                        type=str,
                        dest="state")
    parser.add_argument("-i, --id",
                        action="store_true",
                        help="use iterative deepening A*. default = false",
                        default=False,
                        dest="id")
    args = parser.parse_args()

    # call main with user input
    main(args.width, args.heuristic, args.state, args.id)


if __name__ == "__main__":
    user_input()

From Zack GitHub 

This project is a from-scratch implementation of AWA* (n2 - 1) puzzle. Three heuristics have been implemented and can be used from the command line.
Files:
OpenList.py - definitions for PriorityQueue and Stack classes to be used in search
puzzle.py - definitions for State class and move functions to be used in search
search.py - runs A* or IDA* to solve sliding tile puzzles and outputs data to results.csv
search.py command line options:
-h, --help: shows help text for calling search.py

-s, --state: specifies an initial state for the puzzle.  Numbers separated by spaces, blank tile is _
	ex: -s 1 2 3 4 5 6 7 8 _
	
-w, --width: specifies the width of the puzzle.  MUST be used if -s specified for a size other than the 8 puzzle
	ex: -w 4 (for 15 puzzle), -w 5 (for 24 puzzle)
	
--heuristic: specifies the heuristic to use.  Manhattan distance is default.  Options are [number, manhattan, linear]
	number = number of tiles misplaces
	manhattan = manhattan distance of misplaced tiles
	linear = manhattan distance of misplaced tiles with linear conflicts taken into account
	ex: --heuristic linear
	
-i, --id: flag that specifies to use IDA* instead of A*
	ex: -i
	
ex: python search.py -w 4 -s 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 _ --heuristic linear -i
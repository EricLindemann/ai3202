To run this use: "python Lindemann_assignment2.py worldname 1" for manhattan distance
or: "python Lindemann_assignment2.py worldname 2" for diagonal distance heuristic

diagonal distance uses the a^2 = b^2 + c^2, then multiplies a * 14 to get a distance that is always shorter than or equal to the best possible case. This is the heuristic I chose because it always underestimates the distance to the goal, giving an optimal path but does not underestimate by too much, making it too slow. The diagonal distance heuristic provides exactly the same number of nodes visited and paths as the manhattan distance heuristic. 

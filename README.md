### REQUIREMENTS

Python 3+ installed on your machine

PySide2 --> `pip install PySide2` in a terminal

### HOW TO USE 

In a terminal navigate to the pathfinding_visualizer repository and enter --> ```py pathfinder_exec.py```

Use top slider to adjust grid density  
Pick a start position  
Pick an end position  
Draw obstacles. Left click adds walls, right click removes.  
Select an algorithm from the list.  
 --- Dijkstra's algorithm guarantees shortest path.  
 --- A* (A-Star) algorithm is faster and uses heuristic evaluation but does not guarantee shortest path  
 --- Bidirectionnal Dijkstra algorithm starts from start pos and end pos ans solves when middle node is found.

Run the algorithm clicking the RUN button
Reset grid by pressing the RESET button
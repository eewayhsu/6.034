# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    raise NotImplementedError

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    raise NotImplementedError


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):


    #TRY 1

    """agenda = [[start]]
    currLoc = agenda[-1][-1]
    lastCheck = 1
    
    while lastCheck <= len(agenda) and goal not in graph.get_connected_nodes(currLoc):

        currPath = [i for i in agenda[-1]] 
        neighbors = graph.get_connected_nodes(currLoc)
        closeN = (float("inf"), None);
        
        for n in neighbors:
            edge = graph.get_edge(currLoc, n)
            heur = graph.get_heuristic(currLoc, n)
            dist = edge.length + heur

            test = [i for i in currPath]
            test.append(n)

            #Not a path already in agenda, not already seen, shortest
            if test not in agenda and n not in currPath and heur < closeN[0]:
                closeN = (dist, n)

        if closeN[1] == None:
            lastCheck += 1
            currLoc = agenda[-lastCheck][-1]

        else:        
            currPath.append(closeN[1])
            agenda.append(currPath)
            currLoc = agenda[-1][-1]

    currPath.append(goal)

    return currPath"""


    #TRY 2

    agenda = [[start]]
    while len(agenda) > 0:
        node = agenda.pop()
        if node[-1] == goal:
            return node
        currPaths = []
        for neighbor in graph.get_connected_nodes(node[-1]):
            if neighbor not in node:
                currPaths.append(node+[neighbor])
                
        #Get list of paths ranked from longest to shortest         
        currPaths = sorted(currPaths, key=lambda possPath: graph.get_heuristic(possPath[-1], goal), reverse=True)
        agenda.extend(currPaths)
    return []
    

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    agenda = [[start]]
    nodeList = [];
        
    while len(agenda) > 0:
        for node in agenda:
            if node[-1] == goal:
                return node
            
        currPaths = []
        for node in agenda:  
            for neighbor in graph.get_connected_nodes(node[-1]):
                if neighbor not in node:
                    currPaths.append(node + [neighbor])
                
        currPaths = sorted(currPaths, key=lambda possPath: graph.get_heuristic(possPath[-1], goal))
        agenda = currPaths[:beam_width]
    return []    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    totLength = 0
    
    for i in range(len(node_names)-1):
        totLength += graph.get_edge(node_names[i], node_names[i+1]).length    

    return totLength


def branch_and_bound(graph, start, goal):
    #Try 1 
    """agenda = [[start]]
    shortGoal = (float("inf"), None)
    
    while len(agenda) > 0:
        node = agenda[-1]

        if node[-1] == goal:
            if path_length(graph, node) < shortGoal[0]:
                shortGoal = (path_length(graph, node), node)

                newAgenda = []
                for possPath in agenda:
                    if path_length(graph, possPath) < shortGoal:
                        newAgenda.append(possPath)

                agenda = newAgenda
                node = agenda[-1]
        
        for neighbor in graph.get_connected_nodes(node[-1]):
            agenda.append(node + [neighbor])

        agenda = sorted(agenda, key=lambda possPath: path_length(graph, possPath), reverse=True)

    return shortGoal[1]"""

    #Try 2

    agenda = [[start]]
    while len(agenda) > 0:
        node = agenda.pop(0)
        if node[-1] == goal:
            return node

        for neighbor in graph.get_connected_nodes(node[-1]):
            if neighbor not in node:
                agenda.append(node + [neighbor])

        agenda = sorted(agenda, key=lambda possPath: path_length(graph, possPath))

    return []

def a_star(graph, start, goal):
    extList = []
    
    agenda = [[start]]
    while len(agenda) > 0:
        node = agenda.pop(0)
        extList.append(node[-1])
        if node[-1] == goal:
            return node

        for neighbor in graph.get_connected_nodes(node[-1]):
            if neighbor not in node and neighbor not in extList:
                agenda.append(node + [neighbor])

        agenda = sorted(agenda, key=lambda possPath: path_length(graph, possPath) + graph.get_heuristic(possPath[-1], goal))

    return []    


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    nodeList = graph.nodes

    for node in nodeList:
        path = branch_and_bound(graph, node, goal)
        if graph.is_valid_path(path):
            length = path_length(graph, path)
            if graph.get_heuristic(node, goal) > length:
                return False

    return True

def is_consistent(graph, goal):
    nodeList = graph.nodes

    for node1 in nodeList:
        for node2 in nodeList:
            path = branch_and_bound(graph, node1, node2)
            if graph.is_valid_path(path):
                length = path_length(graph, path)
            heur1 = graph.get_heuristic(node1, goal)
            heur2 = graph.get_heuristic(node2, goal)

            if abs(heur1 - heur2) > length:
                return False

    return True
    
#Start time 4:30pm
HOW_MANY_HOURS_THIS_PSET_TOOK = '4.5h The reading takes so long'
WHAT_I_FOUND_INTERESTING = 'thinking about the searches differently to more effectively code (using sort & stuff)'
WHAT_I_FOUND_BORING = 'Repeatedly typing similar code and eventually being confused'

import math
import turtle
import random
import TSP
import itertools
import time

def test():
    # Generate a randomized graph with vertex names as follows:
    R = RandomGraph(["A", "B", "C", "D", "E", "F", "G", "H"])
    # Print the cost/distance matrix for the randomized graph. We can use this to
    # represent our "distance function"
    print("Cost matrix for randomized graph R:")
    for r in R.CostMatrix(True):
        print(str(r))

    NNP = NearestNeighbor(R, "A", True)
    print("\n Nearest Neighbor Path Result:", NNP)
    print("Total Path Weight:", R.PathWeight(NNP, True))

    BFP = BruteForce(R, "A", True)
    print("\n Brute Force Path Result:", BFP)
    print("Total Path Weight:", R.PathWeight(BFP, True))

    NIP = NearestInsert(R, "A", True)

    PathDict = {"Nearest Neighbor": NNP, "Brute Force": BFP}

    #TSP.TracePaths(R, PathDict, False, True, True)

def RandomGraph(NameSet):
    # Generate a random graph with vertex names from the set "NameSet".
    # A TSP graph with bound 10 has 100 possible unique points, so
    # such a bound value should be sufficient for our purposes.
    RGraph = TSP.TSPGraph(10, "Randomized Graph")
    RGraph.PopulateRandom(NameSet)

    return RGraph

def BruteForce(GraphObj, StartVertName, CycleBool):
    # Check every unique path originating from the starting vertex, then
    # compare them to find the shortest one. Guarenteed to find an exact answer,
    # but computationally inefficient (O(n!) time completixty). If CycleBool == True, 
    # include the edge that gets us back to our starting vertex.
    finalpath = None
    pathdict = {}
    pathlist =[]
    GraphVertexNames = GraphObj.GetVertexNames()

    for p in itertools.permutations(GraphVertexNames):
        # Get every unique path in the graph starting at the specified vertex.
        # Add the starting vertex to the end of the path if neccessary to make it a cycle.
        if p[0] == StartVertName:
            patharray = []
            for t in p:
                patharray.append(t)

            if CycleBool == True:
                patharray.append(StartVertName)

            if patharray not in pathlist:
                pathlist.append(patharray)
            

    for i in range(0, len(pathlist)):
        # Get the length (total weight) of every path in pathlist
        currentpath = pathlist[i]
        pathlength = GraphObj.PathWeight(currentpath, False)
        pathdict[i] = pathlength

    # Sort the paths in pathdict based on their length (total weight)
    SortedLengths = dict(sorted(pathdict.items(), key=lambda item: item[1]))

    # Return the path with the shortest length as our finalpath
    finalpath = pathlist[min(SortedLengths, key=SortedLengths.get)]

    return finalpath

def NearestNeighbor(GraphObj, StartVertName, CycleBool):
    # Implementation of the "nearest neighbor" algorithm as described in Rosenkratz's paper.
    # Easy to implement and relatively fast, but doesn't always produce an optimal solution.
    # If CycleBool == True, include the edge that gets us back to our starting vertex.
    finalpath = []
    VisitedVertices = []
    CurrentVert = None
    PreviousVert = None
    GraphVertexNames = GraphObj.GetVertexNames()

    if GraphObj.NameInGraph(StartVertName) == True:
        CurrentVert = StartVertName
        finalpath.append(StartVertName)
        for V in GraphVertexNames:
            if len(finalpath) < len(GraphVertexNames):
                VisitedVertices.append(CurrentVert)
                VertDistances = {}
                SortedDistances = {}

            # Get the distances between the current vertex and every other vertex in the graph.
            # Here, we make the distance between any vertex and itself an arbitarily high value.
            # If a vertex has already been visited, we also make it an arbitrarily high value.
                for W in GraphVertexNames:
                    if CurrentVert == W or W in VisitedVertices:
                        VertDistances[W] = 999999
                    else:
                        VertDistances[W] = GraphObj.GetDistance(CurrentVert, W, False)
                
            
                SortedDistances = dict(sorted(VertDistances.items(), key=lambda item: item[1]))
                PreviousVert = CurrentVert

                if len(SortedDistances) > 0:
                    CurrentVert = min(SortedDistances, key=SortedDistances.get)
                    finalpath.append(CurrentVert)

                else:
                    for X in GraphVertexNames:
                        if X in finalpath:
                            GraphVertexNames.remove(X)
                            
        if CycleBool == True:
            finalpath.append(StartVertName)

    return finalpath

def NearestInsert(GraphObj, StartVertName, CycleBool):
    # Start with the starting vertex. At each step of the process, add
    # to our "final path" the vertex with the lowest distance to any vertex
    # already in our "final path". Repeat this until every vertex in the graph
    # has been visited once. If CycleBool == True, add the starting vertex to the
    # end of our path so it becomes a cycle.
    finalpath = []
    
    GraphVertices = GraphObj.GetVertexNames()
    UnvisitedVertices = GraphObj.GetVertexNames()

    if GraphObj.NameInGraph(StartVertName) == True:
        finalpath.append(StartVertName)
        UnvisitedVertices.remove(StartVertName)

        while len(UnvisitedVertices) > 0:
            vertexdistances = []
            closestvertdict = {}
            for v in finalpath:
                distdict = {}

                for w in GraphVertices:
                    if w not in finalpath:
                        distdict[w] = GraphObj.GetDistance(v, w, False)
                    
                vertexdistances.append(distdict)
                SortedDistances = dict(sorted(distdict.items(), key=lambda item: item[1]))

                closestvert = min(SortedDistances, key=SortedDistances.get)
                closestvertdict[closestvert] = distdict[closestvert]

            mindist = min(closestvertdict, key=SortedDistances.get)
            print(vertexdistances, mindist)
            UnvisitedVertices.pop(0)


    
    return finalpath

test()
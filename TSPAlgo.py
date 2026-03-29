# James P. Kumpulanian ~ 2025 @James-K-WNEU

import math
import turtle
import random
import TSP
import ParseTSP
import itertools
import time

smallgraphverts = ["α", "β", "γ", "δ", "ε", "ζ"]
mediumgraphverts = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
largegraphverts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

def singletest(algoname, GraphObj, StartVertName, CycleBool, CompTimeRound):
    # Method intended to test the accuracy/reliability of TSP algorithms and heuristics.
    print("Running test. Please wait. \n")
    #BFP = BruteForce(GraphObj, StartVertName, CycleBool)
    #BFPCost  = GraphObj.PathWeight(BFP, False)
    AlgoP = None
    AlgoCost = 0
    starttime = None
    endtime = None
    HeuristicUsed= ""

    # Run the specified algorithm and measure the time it takes to compute an answer for the given graph.
    # Print a summary of the graph used, the heuristic used, and the solution generated. Return a tuple
    # containing these values.

    if str(algoname).lower() == "nn" or str(algoname).lower() == "nearest neighbor":
        HeuristicUsed= "Nearest Neighbor"
        starttime = time.perf_counter()
        AlgoP = NearestNeighbor(GraphObj, StartVertName, CycleBool)
        endtime = time.perf_counter()
        AlgoCost = GraphObj.PathWeight(AlgoP, False)

    if str(algoname).lower() == "ni" or str(algoname).lower() in ["nearest insertion", "nearest insert"]:
        HeuristicUsed= "Nearest Insertion"
        starttime = time.perf_counter()
        AlgoP = NearestInsert(GraphObj, StartVertName, CycleBool)
        endtime = time.perf_counter()
        AlgoCost = GraphObj.PathWeight(AlgoP, False)

    if str(algoname).lower() == "bf" or str(algoname).lower() == "brute-force":
        HeuristicUsed= "Brute Force"
        starttime = time.perf_counter()
        AlgoP = BruteForce(GraphObj, StartVertName, CycleBool)
        endtime = time.perf_counter()
        AlgoCost = GraphObj.PathWeight(AlgoP, False)
    
    elapsedtime = endtime-starttime

    if CompTimeRound > 0:
        # if N = CompTimeRound is greater than zero, round elapsedtime to the Nth decimal place
        elapsedtime = round(elapsedtime, CompTimeRound)

    print("Heuristic used:", HeuristicUsed)
    print("Name of graph:", GraphObj.GetName())
    print("Heuristic answer computed in", elapsedtime, "seconds.")
    print("Length of heuristic-generated tour:", AlgoCost)

    return (GraphObj.GetName(), elapsedtime, AlgoCost)

def algotest(graphvertices, startvert, cyclebool):
    # Method intended to test if each algorithm is working properly.

    # Generate a randomized graph with vertex names as follows:
    R = RandomGraph(graphvertices)
    # Print the cost/distance matrix for the randomized graph. We can use this to
    # represent our "distance function"
    print("Cost matrix for randomized graph R:")
    for r in R.CostMatrix(True):
        print(str(r))

    BFP = BruteForce(R, startvert, cyclebool)
    print("\n Brute Force Path Result:", BFP)
    print("Total Path Weight:", R.PathWeight(BFP, True))

    NNP = NearestNeighbor(R, startvert, cyclebool)
    print("\n Nearest Neighbor Path Result:", NNP)
    print("Total Path Weight:", R.PathWeight(NNP, True))

    NIP = NearestInsert(R, startvert, cyclebool)
    print("\n Nearest Insertion Path Result:", NIP)
    print("Total Path Weight:", R.PathWeight(NIP, True))

    PathDict = {"Brute Force": BFP, "Nearest Neighbor": NNP, "Nearest Insertion": NIP}

    TSP.TracePaths(R, PathDict, False, True, True)

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
    GraphVertexNames.remove(StartVertName)

    for p in itertools.permutations(GraphVertexNames):
        # Get every unique path in the graph starting at the specified vertex.
        # Add the starting vertex to the end of the path if neccessary to make it a cycle.
        patharray = [StartVertName]
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

    # Return the path with the shortest length as our finalpath
    finalpath = pathlist[min(pathdict, key=pathdict.get)]

    return finalpath

def Genetic(GraphObj, StartVertName, CycleBool, MaxCycle):
    # Implementation of a basic genetic algorithm for solving TSP
    # Generates an initial "chromosome" which is just the list of the graph's vertices
    # For each iteration in MaxCycle, generate mutations using Mutate(), evaluate
    # each mutation's fitness using FitEval(), and select the most fit mutations via
    # the Select() function. 

    def Mutate(pathlist, mutnum):
        # For each P in pathlist we generate M = mutnum mutations, so a total
        # of PxM mutations will be generated

        outputlist = []
        for p in pathlist:
            # We mutate a path by swapping the position of two random vertices in the path.
            # For example, if we have a path {a, b, c, d, e} and mutnum = 2, we will get 2 paths 
            # which are mutations of the original: maybe {a, b, d, c, e} and {a, b, c, e, d}
            plen = len(p)
            mutset = []
            for i in range(0, mutnum):
                
                mutpath = p
                SwapIndA = None
                SwapIndB = None
                
                while SwapIndA == SwapIndB:
                    SwapIndA = random.randint(0, plen-1)
                    SwapIndB = random.randint(0, plen-1)

                SwapElementA = mutpath[SwapIndA]
                SwapElementB = mutpath[SwapIndB]
                mutpath[SwapIndA] = SwapElementB
                mutpath[SwapIndB] = SwapElementA
                SwapIndA = None
                SwapIndB = None
                print(mutpath)

        
        return outputlist
    
    def FitEval(path):
        # Evaluate the total weight for the given path. Then, return a double consisting of
        # the path itself and the path weight. For the sake of keeping things simple, our
        # only measure of fit will be the path weight.

        outputdoub = (path, GraphObj.PathWeight(path, False))

        return outputdoub
    
    def Select(doublist, selnum):
        # sort each of the doubles based on path weight in ascended order, then select the paths
        # from index 0 to index N = selum - 1. That way, we select the N "best" paths to proceed with.
        selected = []

        return selected

    Gen = 0
    GenOptimality = 0 
    numverts = GraphObj.NumVertices()
    print(numverts)
    starterpath = []

    if GraphObj.NameInGraph(StartVertName) == True:
        starterpath = GraphObj.GetVertexNames()
        
        mutations = Mutate([starterpath], numverts)
        print(mutations)
            


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
        # Each time we visit a vertex, we remove it from our list of unvisited vertices. Do the following
        # until no vertices are unvisited:
            for v in finalpath:
                distdict = {}
        # Construct dictionaries for each vertex in our final path using the distance between said vertec
        # and every other vertex in the graph.
                for w in GraphVertices:
                    if w not in finalpath:
                        distdict[w] = GraphObj.GetDistance(v, w, False)
                    
                vertexdistances.append(distdict)
        # Take the vertex which is closest to any vertex in our "final path" and add it to our path.
        # Remove it from the list of unvisited vertices
                closestvert = min(distdict, key=distdict.get)
                closestvertdict[closestvert] = distdict[closestvert]

            mindist = min(closestvertdict, key=distdict.get)

            UnvisitedVertices.remove(mindist)
            finalpath.append(mindist)

    if CycleBool == True:
        finalpath.append(StartVertName)

    return finalpath

def GenMinTree(GraphObj, StartVertName, drawtree):
    # Generates a minimum spanning tree for a given graph starting from a given vertex.
    # The tree generation algorithm used is an implementation of Prim's algorithm.
    MinTree = None
    NameString = "MinTree-",GraphObj.GetName(),"-",StartVertName
    if GraphObj.SearchByName(StartVertName) != None:
        MinTree = TSP.MinSpanningTree(GraphObj, StartVertName, NameString)
        MinTree.GenerateMinTree()

        if drawtree:
            TSP.DrawMinTree(GraphObj, MinTree, True, True, "orange")
        
    return MinTree

def TwoOpt(GraphObj, StartVertName, CycleBool, StartCond, NaiveBool):
    # Start with an arbitary path through the graph. Then, for every two unique pairings of vertices,
    # consider the cost of "swapping" edges between them. If the cost of this "swapping"
    # results in less costly path, change the order of the vertices to reflect new arrangement.

    finalpath = []
    workingpath = []
    workingpathcost = 0

    def PathSwap(originallist, swapA, swapB):
        # Swap element "swapA" in the given list with element "swapB"
        newpath = originallist.copy()
        AInd = originallist.index(swapA)
        BInd = originallist.index(swapB)
        newpath[AInd], newpath[BInd] = newpath[BInd], newpath[AInd]
        return newpath
            

    GraphVertices = GraphObj.GetVertexNames()
    
    # Start by generating an arbitary path through the graph.
    # If StartCond = 1, then this will be computed by the nearest neighbor algorithm.
    # If StartCond = 2, then this will be computed by nearest insertion algorithm.
    if StartCond == 1:
        workingpath = NearestNeighbor(GraphObj, StartVertName, CycleBool)
    if StartCond == 2:
        workingpath = NearestInsert(GraphObj, StartVertName, CycleBool)
    else:
        workingpath = GraphVertices

    # Get the total cost of this initial path.
    workingpathcost = GraphObj.PathWeight(workingpath, False)
    #print("Initial path:", workingpath, "with cost", workingpathcost)

    # Consider every unique pairing of verticies with those in our initial path
    # We do this by changing the ordering of vertices in our workingpath list. 
    # We only check disjoint edges (edges which do not share a vertex)
    for i in range (1, len(workingpath)):
        CurrentA = workingpath[i-1]
        CurrentB = workingpath[i]
        workingpathcost = GraphObj.PathWeight(workingpath, False)

        for j in range (1, len(workingpath)):
            CurrentC = GraphVertices[j-1]
            CurrentD = GraphVertices[j]
            # Check to make sure the edges are disjoint
            if CurrentA not in [CurrentC, CurrentD] and CurrentB not in [CurrentC, CurrentD]:
                # Check the costs of the swapped paths. Pick the lowest one among these,
                # then swap the edges.
                inprogpath = workingpath.copy()
                MinCostPath = None
                UnSwappedPath = [CurrentA, CurrentB, CurrentC, CurrentD]
                UnSwappedPathCost = GraphObj.PathWeight(UnSwappedPath, False)
                # Swap the second and third elements
                SwappedPath1 = [CurrentA, CurrentC, CurrentB, CurrentD]
                SwappedPath1Cost = GraphObj.PathWeight(SwappedPath1, False)
                # Swap the second and last elements
                SwappedPath2 = [CurrentA, CurrentD, CurrentC, CurrentB]
                SwappedPath2Cost = GraphObj.PathWeight(SwappedPath2, False)

                if SwappedPath1Cost <= UnSwappedPathCost and SwappedPath1Cost <= SwappedPath2Cost:
                    MinCostPath = SwappedPath1
                if SwappedPath2Cost <= UnSwappedPathCost and SwappedPath2Cost <= SwappedPath1Cost:
                    MinCostPath = SwappedPath2
                else:
                    MinCostPath = UnSwappedPath

                
                if MinCostPath != None and MinCostPath != UnSwappedPath:
                    # if a lower-cost arrangement is found, perform the neccessary swap
                    # operations.
                    print(UnSwappedPath, "=>" , MinCostPath)
                    if SwappedPath1 == MinCostPath:
                        inprogpath = PathSwap(workingpath, MinCostPath[1], MinCostPath[2])
                    if SwappedPath2 == MinCostPath:
                        inprogpath = PathSwap(workingpath, MinCostPath[1], MinCostPath[3])
                    
                    #print(inprogpath, GraphObj.PathWeight(inprogpath, False))

                    # If NaiveBool != True, only change the workingpath if the entire path with
                    # the swapped vertices has a lower overall cost than the current working path.
                    if NaiveBool == True:
                        workingpath = inprogpath
                    if NaiveBool != True and GraphObj.PathWeight(inprogpath, False) < workingpathcost:
                        workingpath = inprogpath

        # update finalpath
        finalpath = workingpath

    if CycleBool == True:
        finalpath.append(StartVertName)

    #print("Final 2-opt path:", finalpath, "with cost", GraphObj.PathWeight(finalpath, False))

    return finalpath

# test
RandMed = RandomGraph(mediumgraphverts)
#TwoOpt(RandMed, "A", False, 1, False)
#TwoOpt(RandMed, "A", False, 2, False)

#berlin52 = ParseTSP.GenFromFile("D:/tsplib-master/Berlin52.tsp", "berlin52")
#burma14 = ParseTSP.GenFromFile("D:/tsplib-master/burma14.tsp", "burma14")
#bier127 = ParseTSP.GenFromFile("D:/tsplib-master/bier127.tsp", "bier127")
#ch130 = ParseTSP.GenFromFile("D:/tsplib-master/ch130.tsp", "ch130")
#d198 = ParseTSP.GenFromFile("D:/tsplib-master/d198.tsp", "d198")
#eil51 = ParseTSP.GenFromFile("D:/tsplib-master/eil51.tsp", "eil51")
#lin105 = ParseTSP.GenFromFile("D:/tsplib-master/lin105.tsp", "lin105")
#pr76 = ParseTSP.GenFromFile("D:/tsplib-master/pr76.tsp", "pr76")
#rd100 = ParseTSP.GenFromFile("D:/tsplib-master/rd100.tsp", "rd100")
#rat99 = ParseTSP.GenFromFile("D:/tsplib-master/rat99.tsp", "rat99")
#st70 = ParseTSP.GenFromFile("D:/tsplib-master/st70.tsp", "st70")
#ulysses16 = ParseTSP.GenFromFile("D:/tsplib-master/ulysses16.tsp", "ulysses16")
#usa13509 = ParseTSP.GenFromFile("D:/tsplib-master/usa13509.tsp", "usa13509")

#testarray = [berlin52, burma14, bier127, ch130, d198, eil51, lin105, pr76, rd100, rat99, st70, ulysses16]

#for t in testarray:
#   singletest("ni", t, "1", "False", 8)

#print(ST.PathWeight(NearestNeighbor(ST, "1", "False"), False))
#print(timertest(ST, "1", "False", 0))
#singletest("nn", ST70, "1", "False", 0)
#singletest("ni", ST70, "1", "False", 0)

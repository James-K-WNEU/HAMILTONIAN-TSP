import math
import turtle
import random
import time

# This file contains the classes for Travelling Salesman graphs (TSP graphs) and their vertices.
# It also contains methods for drawing TSP graphs using the turtle module.

class TSPVertex:
    # Class for objects representing the vertices of a TSP graph.
    # Each TSP vertex has a tuple value representing its position in a 2D Euclidean space.
    # The bounds of the vertex position is determined by the "bound" value of its parent graph.
    def __init__(self, MyName):
        self.position = (None, None)
        self.parentgraph = None
        self.name = MyName
        
    def GetGraph(self):
        return self.parentgraph
    
    def GetPosition(self):
        return self.position
    
    def GetName(self):
        return self.name
    
    def SetParentGraph(self, newGraph):
        if newGraph != None:
            self.parentgraph = newGraph
            # print("Added vertex " + self.name + " to graph " + newGraph.GetName())

    def SetPosition(self, NewX, NewY):
        if NewX >= 0 and NewY >= 0:

            if self.parentgraph == None or self.parentgraph.GetBounds() == None:
                self.position = (NewX, NewY)
            # print("Set position of vertex " + self.name + " to ()" + NewX + "," + NewY + "). ")

            if self.parentgraph != None:
                if NewX <= self.parentgraph.GetBounds() and NewY <= self.parentgraph.GetBounds():
                    self.position = (NewX, NewY)
                    # print("Set position of vertex " + self.name + " to" + (NewX, NewY))
                else:
                    print("The coordinates are not within the bounds of graph " + self.parentgraph.GetName())
                
            
        else:
            print("The coordinate values must be non-negative reals within the bounds of the graph.")
    
    def SetName(self, newName):
        self.name = newName
        # print("Set name of vertex to " + newName)

    def GetDistance(self, OtherVert, RoundBool):
        APos = self.GetPosition()
        BPos = OtherVert.GetPosition()
        Distance = None
        if self.parentgraph == OtherVert.GetGraph():
            DeltaX = APos[0] - BPos[0]
            DeltaY = APos[1] - BPos[1]
            DeltaXSquare = math.pow(DeltaX, 2)
            DeltaYSquare = math.pow(DeltaY, 2)
            RealDist = math.sqrt(DeltaXSquare + DeltaYSquare)

            if RoundBool == True:
                Distance = math.ceil(RealDist)
            else:
                Distance = RealDist

            
        
        else:
            print("Vertices " + self.name + " and ", OtherVert.GetName() + " are not in the same graph.")

        return Distance
    
class TSPGraph:
    # Class for objects representing a TSP graph.
    # Each TSP graph lay in a BxB Euclidian space, where B is the "bound" value of the graph.
    # Each vertex in the graph occupies a unique position within this Euclidian space.
    # This guarentees that the distance between any two distinct vertices will satisfy the triangle inequality.
    def __init__(self, MyBounds, MyName):
        self.vertices = []
        self.bound = math.floor(MyBounds)
        self.name = MyName

    def GetBounds(self):
        return self.bound
    
    def GetVertices(self):
        return self.vertices
    
    def GetName(self):
        return self.name
    
    def GetVertexNames(self):
        VertexNames = []
        for V in self.vertices:
            VertexNames.append(V.GetName())

        return VertexNames
    
    def SetName(self, newName):
        self.name = newName
        # print("Set name of graph to " + newName)

    def SetBounds(self, newBounds):
        self.bound = math.floor(newBounds)
        # print("Set bounds of graph to " + math.floor(newBounds))

    def GetVertexNames(self):
        NamesList = []

        for V in self.vertices:
            NamesList.append(V.GetName())

        return NamesList

    def NameInGraph(self, SearchName):
        # Search the graph for a vertex with the given name and return a true or false value.
        FoundVert = False
        for V in self.vertices:
            if V.GetName() == SearchName:
                FoundVert = True
        
        return FoundVert

    def VertexDict(self):
        # Returns the vertices and their positions in the form of a dictionary/associative array.
        VertDict = {}
        for V in self.vertices:
            VertDict[V.GetName()] = V.GetPosition()

        return VertDict

    def GetVertex(self, VertX, VertY):
        # Search for a vertex based on its position coordinates. If found, return said vertex.
        FoundVert = None
        for V in self.vertices:
            CVPos = V.GetPosition()
            if CVPos[0] == VertX and CVPos[1] == VertY:
                FoundVert = V
            
        if FoundVert != None:
            print ("Found vertex", FoundVert.GetName(), "with position", (VertX, VertY))

        return FoundVert
    
    def PositionOccupied(self, VertX, VertY):
        # Returns whether or not an (x, y) position in the graph is occupied by a vertex.
        VertInPos = self.GetVertex(VertX, VertY)

        if VertInPos == None:
            return False
        
        if VertInPos != None:
            return True
    
    def GetVertexPosition(self, Vert):
        # Search the graph for a specific vertex. If found, return its position.
        FoundVertPos = (None, None)
        for V in self.vertices:
            if V == Vert:
                FoundVertPos = V.GetPosition()

        return FoundVertPos
    
    def SearchByName(self, VertName):
        # Search for a vertex by name. Return the vertex if it exists in the graph.
        FoundVert = None
        for V in self.vertices:
            if V.GetName() == VertName:
                FoundVert = V

        return FoundVert

    
    def GenerateVertex(self,  NewName, VertX, VertY,):
        # Create a new vertex in the graph with the specified parameters if such a vertex does not already exist.
        # The position and name for each vertex in the graph must be unique.
        FoundVert = self.GetVertex(VertX, VertY)
        if FoundVert != None:
            print("There is already a vertex in graph ", self.name, " with position", (VertX, VertY), " or name ", NewName)
        if FoundVert == None:
            if 0 <= VertX and VertX < self.bound and 0 <= VertY and VertY < self.bound:
                NewVert = TSPVertex(NewName)
                NewVert.SetPosition(math.floor(VertX), math.floor(VertY))
                NewVert.SetParentGraph(self)
                self.vertices.append(NewVert)
            else:
                ("Could not create vertex with the given coordinates. Coordinates must be positive integers"
                "between zero and", self.bound)
            
        
    def AddVertex(self, NewVert):
        # Add an existing vertex into the graph if there does not already exist a vertex in the graph
        # with the specified position or name.
        NewVertPos = NewVert.GetPosition()
        FoundVert = self.GetVertex(NewVertPos[0], NewVertPos[1])
        FoundVertPos = self.GetVertexPosition(NewVert)
        if FoundVert != None or FoundVertPos != (None, None):
            print("There is already a vertex in graph", self.name, "with position", NewVertPos, "or name", NewVert.GetName())

        if FoundVert == None and FoundVertPos == (None, None):
            NewVert.SetParentGraph(self)
            self.vertices.append(NewVert)
            print("Added vertex", NewVert.GetName(), "to", self.GetName())

    def RemoveVertex(self, VertName):
        FoundVert = self.SearchByName(VertName)
        
        if FoundVert == None or FoundVert not in self.vertices:
            print ("Could not find vertex", VertName, "in graph", self.name)
        else:
            FoundVert.SetParentGraph(None)
            self.vertices.remove(FoundVert)
            print ("Removed vertex", VertName, "from", self.name)
        
    def GetDistance(self, VertAName, VertBName, RoundBool):
        # Get the distance between any two vertices in the graph.
        # If RoundBool is True, then round up to the nearest integer value
        AInGraph = self.NameInGraph(VertAName)
        BInGraph = self.NameInGraph(VertAName)
        VertDist = None

        if AInGraph == True and BInGraph == True:
            VertA = self.SearchByName(VertAName)
            VertB = self.SearchByName(VertBName)
            VertDist = VertA.GetDistance(VertB, RoundBool)
        
        return VertDist
    
    def PopulateRandom(self, NameSet):
        # Populate the graph with random vertices with names drawn from the NameSet.
        if len(NameSet) > 0:
            for N in NameSet:
                VertInGraph = None
                while VertInGraph == None:
                    VertXPos = random.randint(0, self.GetBounds())
                    VertYPos = random.randint(0, self.GetBounds())
                    self.GenerateVertex(N, VertXPos, VertYPos)
                    VertInGraph = self.SearchByName(N)
                
            
        else:
            print("Could not generate vertices from the list of names provided.")

    def PathWeight(self, VertexNames, RoundBool):
        # Returns the total weight of a path or walk within the graph.
        # The order of the vertex names determines the order in which the vertices are visited.
        # If RoundBool == True, round up to the nearest integer value.
        TotalWeight = 0
        CurrentVert = None
        PreviousVert = None
        for i in range(0, len(VertexNames)):
            if i > 0:
                CurrentVert = self.SearchByName(VertexNames[i])
                PreviousVert = self.SearchByName(VertexNames[i-1])
                if PreviousVert != None and CurrentVert != None:
                   TotalWeight += self.GetDistance(VertexNames[i-1], VertexNames[i], False)
            
        if RoundBool == True:
            TotalWeight = math.ceil(TotalWeight)

        return TotalWeight
    
    def CostMatrix(self, RoundBool):
        # Generate the cost matrix for the graph. The "cost" refers to the distance between
        # two vertices. The distance between any vertex and itself is 0.
        CostMat = []

        for V in self.vertices:
            VertRow = []
            for W in self.vertices:
                VertDist = 0
                if V != W:
                    VertDist = V.GetDistance(W, RoundBool)
                VertRow.append(VertDist)
            
            CostMat.append(VertRow)
        
        #print("Cost matrix for graph", self.name, ":")
        #for C in CostMat:
            #print("|", C, "|")

        return CostMat
    
    def GenSubgraph(self, vertexlist):
        # Generate a subgraph of the current graph using the vertices listed in vertexlist.
        subgraphname = ""
        newGraph = TSPGraph(self.GetBounds(), subgraphname)

        for v in vertexlist:
            if self.NameInGraph(v) == True:
                subgraphname+=v
                newGraph.SetName(subgraphname)
                currentvert = self.SearchByName(v)
                currentvertpos = self.GetVertexPosition(currentvert)
                newGraph.GenerateVertex(v, currentvertpos[0], currentvertpos[1])
            
        print("Generated subgraph", subgraphname, "of graph", self.GetName())
        return newGraph

def ConvertVertexPos(GraphObj):
        # Create a dictionary of modified vertex positions to be used when drawing
        # graphs.
        GraphBounds = GraphObj.GetBounds()
        VertexPosDict = {}
        for V in GraphObj.GetVertices():
        
            VPos = V.GetPosition()
            ModifiedVertexPos = (52*((VPos[0])-(GraphBounds*0.5)), 52*((VPos[1])-(GraphBounds*0.5)))
            VertexPosDict[V.GetName()] = (ModifiedVertexPos[0], (ModifiedVertexPos[1]+(200/GraphBounds)))
        
        return VertexPosDict

def DrawGraph(GraphObj, ShowEdges, ShowVertPos):
    # Draw a graph with its vertices and edges.
    # Note: Tends to get messy as the number of vertices increases.
    VertexPosDict = ConvertVertexPos(GraphObj)
    DrawComplete = []
    GraphBounds = GraphObj.GetBounds()
    GraphVertices = GraphObj.VertexDict()
    VertexSize = 100/GraphBounds

    MyScreen = turtle.Screen()
    MyScreen.title(GraphObj.GetName())

    Cursor = turtle.Turtle()
    Cursor.speed("fastest")
    Cursor.penup()
    Cursor.pensize(math.floor(VertexSize/10))

    Cursor.hideturtle()

    for V in GraphObj.GetVertices():
        # Plot the vertices
        ModifiedVertexPos = VertexPosDict[V.GetName()]

        Cursor.goto((ModifiedVertexPos[0], ModifiedVertexPos[1]-VertexSize))
        Cursor.pendown()
        Cursor.circle(VertexSize)
        Cursor.penup()
        Cursor.goto((ModifiedVertexPos[0]-VertexSize*1.50), (ModifiedVertexPos[1]-VertexSize*2.0))
        Cursor.pendown()

        # Write the names of the vertices and, if specified, their positions
        if ShowVertPos == False:
            Cursor.write(V.GetName(), ("Arial", VertexSize*3, "normal"))

        if ShowVertPos == True:
            VertPosString = str(V.GetPosition())
            VertNameString = V.GetName()
            VertString = VertNameString + " " + VertPosString
            Cursor.write(VertString, ("Arial", VertexSize*4, "normal"))


        Cursor.penup()

    if ShowEdges == True:
        # If specified, draw the edges with their weights. The weight of an edge
        # is the distance between the starting and ending vertices.
        for E in GraphVertices:
                CurrentVertPos = VertexPosDict[E]
                Cursor.penup()
                Cursor.goto(CurrentVertPos)
                for F in GraphVertices:
                    OtherVertPos = VertexPosDict[F]
                    Cursor.pendown()
                    if E != F and F not in DrawComplete:
                        VertDist = GraphObj.GetDistance(E, F, True)
                        Midpoint = ((VertexPosDict[E][0] + VertexPosDict[F][0])/2, (VertexPosDict[E][1] + VertexPosDict[F][1])/2)
                        Cursor.goto(Midpoint)
                        Cursor.penup()
                        Cursor.goto((5+Midpoint[0], 5+Midpoint[1]))
                        Cursor.pendown()
                        Cursor.color("Red")
                        Cursor.write(str(VertDist), ("Arial", VertexSize*4, "normal"))
                        Cursor.penup()
                        Cursor.color("Black")
                        Cursor.goto(Midpoint)
                        Cursor.pendown()
                        Cursor.goto(OtherVertPos)
                        Cursor.penup()
                        Cursor.goto(CurrentVertPos)
                        Cursor.pendown()
                    
                DrawComplete.append(E)
                    
    print("Finished drawing graph.")

    return MyScreen

def TracePath(GraphObj, VertNamesList, PathName, ShowVertPos, ShowAllEdges, ShowPathWeight, PathColor):
    # Draw the graph, then draw the graph specified in the "VertNamesList" array.
    PossibleColors = ["blue", "red", "green", "orange", "purple", "cyan"]
    VertexPosDict = ConvertVertexPos(GraphObj)
    GraphBounds = GraphObj.GetBounds()
    VertexSize = 100/GraphBounds

    MyScreen = DrawGraph(GraphObj, ShowAllEdges, ShowVertPos)
    MyScreen.title(GraphObj.GetName())

    Cursor = turtle.Turtle()
    Cursor.penup()
    Cursor.pensize(math.floor(1+(VertexSize/10)))
    if str(PathColor).lower() in PossibleColors:
        Cursor.color(PathColor)
    else:
        Cursor.color("blue")

    Cursor.hideturtle()

    CurrentVert = None
    PreviousVert = None

    for n in range (0, len(VertNamesList)-1):
        PreviousVert = VertexPosDict[VertNamesList[n]]
        CurrentVert = VertexPosDict[VertNamesList[n+1]]
        if ShowAllEdges == True:
            Cursor.goto((PreviousVert[0], PreviousVert[1]))
            Cursor.pendown()
            Cursor.goto((CurrentVert[0], CurrentVert[1]))
            Cursor.penup()
        
        else:
            VertDist = GraphObj.GetDistance(VertNamesList[n], VertNamesList[n+1], True)
            Midpoint = ((CurrentVert[0] + PreviousVert[0])/2, (CurrentVert[1] + PreviousVert[1])/2)
            Cursor.goto((PreviousVert[0], PreviousVert[1]))
            Cursor.pendown()
            Cursor.goto(Midpoint)
            Cursor.penup()
            Cursor.goto((5+Midpoint[0], 5+Midpoint[1]))
            Cursor.pendown()
            Cursor.write(str(VertDist), ("Arial", VertexSize*4, "normal"))
            Cursor.penup()
            Cursor.goto(Midpoint)
            Cursor.pendown()
            Cursor.goto((CurrentVert[0], CurrentVert[1]))
            Cursor.penup()

    WriteString = str(PathName) + ": " + str(VertNamesList)
    Cursor.goto(-325.0, 270)
    Cursor.pensize(math.floor(VertexSize/10))
    Cursor.write(WriteString, ("Arial", "left", 20, "bold"))
    Cursor.penup()

    if ShowPathWeight == True:
        TotalWeight = GraphObj.PathWeight(VertNamesList, True)
        WeightString = "Total path weight: "+str(TotalWeight)
        Cursor.goto(-325.0, 255)
        Cursor.pendown()
        Cursor.write(WeightString, ("Arial", "left", 20, "bold"))
        Cursor.penup()

    Cursor.pencolor("Black")
    print("Finished tracing path.")

    Cursor.goto(-325, -275)
    Cursor.pendown()
    Cursor.write("Click anywhere in the window to exit", ("Arial", "left", 18, "bold"))
    Cursor.penup()
    MyScreen.exitonclick()

    return MyScreen

def TracePaths(GraphObj, PathDict, ShowVertPos, ShowAllEdges, ShowPathWeight):
    # Trace a set of paths listed in a dictionary format. The dictionary should be formated so that
    # Each key is the name of the path and each key is the array which defines the order in which vertices
    # are visited.
    UndrawnPaths = list(PathDict.keys())
    PossibleColors = ["blue", "red", "green", "orange", "purple", "cyan"]
    VertexPosDict = ConvertVertexPos(GraphObj)
    GraphBounds = GraphObj.GetBounds()
    VertexSize = 100/GraphBounds

    MyScreen = DrawGraph(GraphObj, ShowAllEdges, ShowVertPos)
    MyScreen.title(GraphObj.GetName())

    while len(UndrawnPaths) > 0:
        CurrentPath = UndrawnPaths[0]
        VertNamesList = PathDict[CurrentPath]
        pathcolor = PossibleColors[random.randint(0, len(PossibleColors)-1)]
        
        NewCursor = turtle.Turtle()
        NewCursor.penup()
        NewCursor.pensize(math.floor(1+(VertexSize/10)))
        NewCursor.color(pathcolor)
        NewCursor.hideturtle()

        CurrentVert = None
        PreviousVert = None

        for n in range (0, len(VertNamesList)-1):
            PreviousVert = VertexPosDict[VertNamesList[n]]
            CurrentVert = VertexPosDict[VertNamesList[n+1]]
            if ShowAllEdges == True:
                NewCursor.goto((PreviousVert[0], PreviousVert[1]))
                NewCursor.pendown()
                NewCursor.goto((CurrentVert[0], CurrentVert[1]))
                NewCursor.penup()
        
            else:
                VertDist = GraphObj.GetDistance(PreviousVert, CurrentVert, True)
                Midpoint = ((CurrentVert[0] + PreviousVert[0])/2, (CurrentVert[1] + PreviousVert[1])/2)
                NewCursor.goto((PreviousVert[0], PreviousVert[1]))
                NewCursor.pendown()
                NewCursor.goto(Midpoint)
                NewCursor.penup()
                NewCursor.goto((5+Midpoint[0], 5+Midpoint[1]))
                NewCursor.pendown()
                NewCursor.write(str(VertDist), ("Arial", VertexSize*4, "normal"))
                NewCursor.penup()
                NewCursor.goto(Midpoint)
                NewCursor.pendown()
                NewCursor.goto((CurrentVert[0], CurrentVert[1]))
                NewCursor.penup()

        WriteString = str(CurrentPath) + ": " + str(VertNamesList)
        NewCursor.goto(-325.0, 270)
        NewCursor.pensize(math.floor(VertexSize/10))
        NewCursor.write(WriteString, ("Arial", "left", 20, "bold"))
        NewCursor.penup()

        if ShowPathWeight == True:
            TotalWeight = GraphObj.PathWeight(VertNamesList, True)
            WeightString = "Total path weight: "+str(TotalWeight)
            NewCursor.goto(-325.0, 255)
            NewCursor.pendown()
            NewCursor.write(WeightString, ("Arial", "left", 20, "bold"))
            NewCursor.penup()

            NewCursor.pencolor("Black")

            NewCursor.goto(-325, -275)
            NewCursor.penup()

            # Wait 3 seconds before clearing the path drawn and moving on to the next one.
            time.sleep(3)
            MyScreen.onclick(NewCursor.reset())
            NewCursor.hideturtle()

        UndrawnPaths.pop(0)

   


    

        
    

    





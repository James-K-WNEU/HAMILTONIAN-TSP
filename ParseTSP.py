# James P. Kumpulanian ~ 2025

# This file contains functions for parsing data from .TSP (Concorde File Format) files
# and using the data inside to create graphs that can used and analyzed by the functions
# in TSPAlgo.py

import TSP

def FileReadTest(path):
    # Make sure the file we want to read from is readable and in the right format.
    CorrectFormat = False
    CanRead = False

    TestPass = False
    
    if isinstance(path, str) == True:
        filename = path.lower()
        if filename[-4:(len(filename))] == ".tsp":
            CanRead = True
            with open(path, "r") as File:
                contents = File.read()
                #print(contents)
                if "node_coord_section" in contents.lower():
                    CorrectFormat = True
                else:
                    print("File is not in the correct format.")
        else:
            print("File is not a .tsp file.")
        
    else:
        print("File path is either incorrect or the indicated file does not exist.")
    
    if CanRead == True and CorrectFormat == True:
        TestPass = True

    return TestPass

def ParseTSPFile(path):
    # Takes a file name / path as input returns the data from the file as a list of tuples.
    datalist = []
    tuplelist = []

    CanRead = FileReadTest(path)
    delim = " "
    # These characters are used to format the data in .tsp files but do not encode data itself.
    specialchars = ["EOF", "", " ", "  ", "\n", "\t"]

    if CanRead == True:
        startind = None
        lineind = 0
        # Read the data in the file and put it into datalist, only adding the data after the "Node_Coord_Section".
        with open(path, "r") as File:
            for line in File:
                lineind += 1
                linestring = line[0:len(line)-1]
                if "node_coord_section" in linestring.lower():
                    startind = lineind

                if startind != None and lineind > startind:
                    #print(linestring)
                    datalist.append(linestring)
                    #if "EOF" in linestring or linestring == "\n":
                        #print("End of file at line", str(lineind))
                
        for i in range(0, len(datalist)):
        # Convert the data read from the files into tuples.
            tupleparts = []
            currentline = datalist[i]
            #print(currentline)
            if "EOF" not in datalist[i] and datalist[i] not in specialchars:
                for s in currentline.split(delim):
                    if s not in specialchars:
                        tupleparts.append(s)
                #print(s)
                tupleparts[1] = float(tupleparts[1])
                tupleparts[2] = float(tupleparts[2])
            
                tuplelist.append(tuple(tupleparts))
                #print(tuplelist)
    else:
        print("File not found or could not be read.")
    
    return tuplelist

def GenFromFile(filepath, graphname):
    # Parses data from a .TSP file. If successful, the data is used to generate
    # a TSP graph with corresponding bounds, vertex positions, and vertex names.

    CanRead = FileReadTest(filepath)
    upperbound = 0
    newgraph = None

    if CanRead == True:
        filedata = ParseTSPFile(filepath)
        for f in filedata:
            if f[1] > upperbound:
                upperbound = f[1]
            if f[2] > upperbound:
                upperbound = f[2]
            
        newgraph = TSP.TSPGraph(upperbound, graphname)
        for f in filedata:
            newgraph.GenerateVertex(f[0], f[1], f[2])

    if CanRead == False:
        print("File data could not be parsed or is in the wrong format.")
            
    return newgraph

def test(filename):
    # Tests opening files, reading data from files, then transcribing the data into graphs.
    ReadFile = False
    CorrectTrans = False
    print("Running tests for "+str(filename)+"...")
    FileRead = FileReadTest(filename)
    if FileRead == True:
        ReadFile = True
        print("Successfully read data.")

        FileData = ParseTSPFile(filename)
        TestGraph = GenFromFile(filename, "test")
        TestVerts = TestGraph.VertexDict()
        #print(TestGraph.VertexDict())
        if TestVerts["1"] == (FileData[0][1], FileData[0][2]):
            CorrectTrans = True
            print("File data transcribed correctly.")

    if CorrectTrans == True and ReadFile == True:
        print("All tests successful for", str(filename),"\n")

test("C:/Users/My Laptop/Documents/PythonProjects/GraphStuff/tsplib-master/usa13509.tsp")
test("C:/Users/My Laptop/Documents/PythonProjects/GraphStuff/tsplib-master/vm1748.tsp")
test("C:/Users/My Laptop/Documents/PythonProjects/GraphStuff/tsplib-master/ulysses16.tsp")

test("C:/Users/My Laptop/Documents/PythonProjects/GraphStuff/tsplib-master/swiss42.tsp")

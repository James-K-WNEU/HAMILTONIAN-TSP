# James P. Kumpulanian ~ 2025

# This file contains functions for parsing data from .TSP (Concorde File Format) files
# and using the data inside to create graphs that can used and analyzed by the functions
# in TSPAlgo.py

import TSP

def FileReadTest(path):
    # Make sure the file we want to read from is readable and in the right format.
    CanRead = False
    
    if isinstance(path, str) == True:
        filename = path.lower()
        if filename[-4:(len(filename))] == ".tsp":
            CanRead = True
        else:
            print("File is not in .tsp format.")
        
    else:
        print("File path is either incorrect or the indicated file does not exist.")
    
    return CanRead

def ParseTSPFile(path):
    # Takes a file name / path as input returns the data from the file as a list of tuples.
    datalist = []
    tuplelist = []

    CanRead = FileReadTest(path)
    delim = " "

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
                    datalist.append(linestring)
                
            
        for i in range(0, len(datalist)-2):
        # Convert the data read from the files into tuples.
            tupleparts = []
            currentline = datalist[i]
            for s in currentline.split(delim):
                if delim not in s and s != "":
                    tupleparts.append(s)

            tupleparts[1] = float(tupleparts[1])
            tupleparts[2] = float(tupleparts[2])
            

            tuplelist.append(tuple(tupleparts))
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

def test():
    print("Running tests...")
    FileRead = FileReadTest("berlin52.tsp")
    if FileRead == True:
        print("Successfully read data.")
        FileData = ParseTSPFile("berlin52.tsp")
        BerlinGraph = GenFromFile("berlin52.tsp", "berlin")
        BerlinVerts = BerlinGraph.VertexDict()

        if BerlinVerts["1"] == (FileData[0][1], FileData[0][2]):
            print("File data transcribed correctly.")

#test()
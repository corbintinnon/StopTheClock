from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import vtk
import os.path
import sys
import numpy as np
from vtk.util import numpy_support as vn

def readFile(inputPath,fileName):
    inputFile = os.path.join(inputPath, fileName)
    if not os.path.exists(inputFile):
        print("Could not find file %s" %fileName)
        return fileName
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(inputFile)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata


### Visualization Packages

def createWindow():
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(4000, 1000)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    return renWin, iren

def addActors(ren,polydata,colors=[0.6,0.8,0.9],op=1, pos=(0,1,1)):
    map1 = vtk.vtkPolyDataMapper()
    map1.SetInputData(polydata)
    Actor1 = vtk.vtkActor()
    Actor1.SetMapper(map1)
    Actor1.GetProperty().SetDiffuseColor(colors[0],colors[1],colors[2])
    Actor1.GetProperty().SetOpacity(op)
    ren.AddActor(Actor1)
    ren.GetActiveCamera().SetPosition(pos)
    ren.ResetCamera()

def addLabels(ren,text):
    textActor = vtk.vtkTextActor()
    textActor.SetInput(text)
    textActor.SetTextScaleModeToViewport()
    textActor.GetTextProperty().SetFontSize(20)
    textActor.GetTextProperty().SetColor(0, 0, 0)
    ren.AddActor2D(textActor)

def startVis(renWin,iren):
    iren.Initialize()
    renWin.Render()
    iren.Start()

def createRen(renWin, xPos1,xPos2):
    ren = vtk.vtkRenderer()
    renWin.AddRenderer(ren)
    ren.SetBackground(1, 1, 1)
    ren.SetViewport(xPos1, 0, xPos2, 1)
    return ren

def createRenArray(renWin, array,xPos1,xPos2):
    ren = vtk.vtkRenderer()
    renWin.AddRenderer(ren)
    actors = []
    for i in range(np.size(array)):
        color = i/np.size(array)
        r = 1
        g = 1-color
        b = color
        actors.append(store(addActors(ren,array[i].number,[r,g,b],1)))
    ren.SetBackground(1, 1, 1)
    ren.SetViewport(xPos1, 0.0, xPos2, 1.0)
    ren.GetActiveCamera().SetPosition(1, -1, 0)
    ren.ResetCamera()

class store(object):
    def __init__(self, number):
        self.number = number
        
def getColors():
    darkGreen = [0,0.4,0.2]
    brightMarine = [0,0.9,0.5]
    teal = [0,1,0.9]
    babyBlue = [0.1,0.9,1]
    orange = [1,0.6,0.3]
    pink = [0.9,0.1,0.7]
    darkRed = [0.8,0,0]
    greyBlue = [0.6,0.8,0.9]
    purple = [0.4,0.1,0.6]
    limeGreen = [0.4,1,0.5]
    marionberry = [0.4,0,0.4]
    brown = [0.3,0.1,0]
    yellow = [0.9,1,0.2]
    scarlet = [1,0,0.3]
    indigo = [0.6,0.3,1]
    blue = [0,0.1,0.8]
    green = [0.1,0.8,0.3]
    red = [1,0.1,0]
    salmon = [1,0.5,0.5]
    white = [1,1,1]
    black = [0.2,0.2,0.2]
    grey = [0.5,0.5,0.5]
    khaki = [0.9,0.7,0.5]
    violet = [0.7,0.1,1]
    colorList = [darkGreen, brightMarine, teal, babyBlue, orange, pink, darkRed, greyBlue, purple, limeGreen, marionberry, brown, yellow, scarlet, indigo, blue, green, red, salmon, white, black, grey, khaki, violet]
    return colorList

def getColor(x):
    if (x=="darkGreen"): y = [0,0.4,0.2]
    elif (x=="brightMarine"): y = [0,0.9,0.5]
    elif (x=="teal"): y = [0,1,0.9]
    elif (x=="babyBlue"): y = [0.1,0.9,1]
    elif (x=="orange"): y = [1,0.6,0.3]
    elif (x=="pink"): y = [0.9,0.1,0.7]
    elif (x=="darkRed"): y = [0.8,0,0]
    elif (x=="greyBlue"): y = [0.6,0.8,0.9]
    elif (x=="purple"): y = [0.4,0.1,0.6]
    elif (x=="limeGreen"): y = [0.4,1,0.5]
    elif (x=="marionberry"): y = [0.4,0,0.4]
    elif (x=="brown"): y = [0.3,0.1,0]
    elif (x=="yellow"): y = [0.9,1,0.2]
    elif (x=="scarlet"): y = [1,0,0.3]
    elif (x=="indigo"): y = [0.6,0.3,1]
    elif (x=="blue"): y = [0,0.1,0.8]
    elif (x=="green"): y = [0.1,0.8,0.3]
    elif (x=="red"): y = [1,0.1,0]
    elif (x=="salmon"): y = [1,0.5,0.5]
    elif (x=="white"): y = [1,1,1]
    elif (x=="black"): y = [0.2,0.2,0.2]
    elif (x=="grey"): y = [0.5,0.5,0.5]
    elif (x=="khaki"): y = [0.9,0.7,0.5]
    elif (x=="violet"): y = [0.7,0.1,1]
    else:
        print("Color name does not exist")
        y=0
    return y
    

#mapping color onto follow up image to see change
def visChangeInShapes(base, fol, dist, maxVal, colorP = "notWhite"):
    
    #using Enclosed Points
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    #mark points inside of surface
    enclosed = vtk.vtkSelectEnclosedPoints()
    enclosed.SetInputData(base)
    enclosed.SetSurfaceData(fol)
    enclosed.InsideOutOff()
    enclosed.CheckSurfaceOff()
    enclosed.Update()
    
    #set colors
    if (colorP == "white"):
        for j in range(np.size(dist)):
            scale = abs(dist[j]*255/maxVal)
            if (scale > 255):
                scale = 255
            if (enclosed.IsInside(j)):
                #red
                color = [255,255-scale,255-scale]
                colors.InsertNextTuple(color)
            else:
                #blue
                color = [255-scale,255,255]
                colors.InsertNextTuple(color)
    
    else:
        for j in range(np.size(dist)):
            scaleBig = 0
            scale = abs(dist[j]*510/maxVal)
            if (scale > 510):
                scaleBig = 255
                scale = 255
            elif (scale > 255):
                scaleBig = scale-255
                scale=255
            if (enclosed.IsInside(j)):
                color = [scaleBig,255,255-scale]
                colors.InsertNextTuple(color)
            else:
                color = [scaleBig,255-scale,255]
                colors.InsertNextTuple(color)

    #change change from fol to base to map it on base
    base.GetPointData().SetScalars(colors)
    
def resetColors(base):
    base.GetPointData().RemoveArray("Colors")
    

if __name__ == '__main__':
    darkGreen = [0,0.4,0.2]
    brightMarine = [0,0.9,0.5]
    teal = [0,1,0.9]
    babyBlue = [0.1,0.9,1]
    orange = [1,0.6,0.3]
    pink = [0.9,0.1,0.7]
    darkRed = [0.8,0,0]
    greyBlue = [0.6,0.8,0.9]
    purple = [0.4,0.1,0.6]
    limeGreen = [0.4,1,0.5]
    marionberry = [0.4,0,0.4]
    brown = [0.3,0.1,0]
    yellow = [0.9,1,0.2]
    scarlet = [1,0,0.3]
    indigo = [0.6,0.3,1]
    blue = [0,0.1,0.8]
    green = [0.1,0.8,0.3]
    red = [1,0.1,0]
    salmon = [1,0.5,0.5]
    white = [1,1,1]
    black = [0.2,0.2,0.2]
    grey = [0.5,0.5,0.5]
    khaki = [0.9,0.7,0.5]
    violet = [0.7,0.1,1]
    useless = "Useless"
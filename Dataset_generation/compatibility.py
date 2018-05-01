from RubiksCube_TwophaseSolver import solver as sv
from RubiksCube_TwophaseSolver import cubie
from RubiksCube_TwophaseSolver.enums import Color
from MagicCube.code import cube as renderer

import numpy as np

#To make things awful, the render and solver disagree on cube orientation.
#This dictionary translates Solver Faces to Renderer Faces
#faceTranslate= {"U":"D", "D":"U", "B":"R", "F":"L", "R":"B", "L":"F"}
#For reference, here is the dict used in the renderer
#facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}

#Therefore, this combines the two into a single table
fd = {Color.D:0, Color.U:1, Color.L:2, Color.R:3, Color.B:4, Color.F:5}

def cubie_to_stickers(solvercube):
    #translate the solver's representation to an array of stickers for the renderer
    fc = solvercube.to_facelet_cube()
    s = []
    for i in range(54):
        #Substitutes colors, so that the Solver's orientation is preserved (i.e. solver-up is rendered as up)
        s.append(fd[fc.f[i]])
        
#        if fc.f[i] == Color.U:
#            s.append(1)
#        elif fc.f[i] == Color.R:
#            s.append(3)
#        elif fc.f[i] == Color.F:
#            s.append(5)
#        elif fc.f[i] == Color.D:
#            s.append(0)
#        elif fc.f[i] == Color.L:
#            s.append(2)
#        elif fc.f[i] == Color.B:
#            s.append(4)

    a = np.array([
        #SolverName to RendererName
        np.rot90([s[0:3],s[3:6],s[6:9]],-1), #U
        np.rot90([s[27:30], s[30:33], s[33:36]],-1), #D
        np.rot90([s[18:21],s[21:24],s[24:27]],-1), #F
        np.rot90([s[45:48],s[48:51],s[51:54]],-1), #B
        np.rot90([s[9:12],s[12:15],s[15:18]],-1), #R
        np.rot90([s[36:39],s[39:42],s[42:45]],-1), #L
        ])
    return a





def renderCubie(cb):
    rc = renderer.Cube(3)
    rc.stickers = cubie_to_stickers(cb)
    img = rc.render()
    return img


def solveCubie(cb, animate = False):
    rc = renderer.Cube(3)
    rc.stickers = cubie_to_stickers(cb)
    if animate: img = rc.render()
    cs = cb.to_facelet_cube().__str__()
    try:
        sol = sv.solve(cs)
    except IndexError:
        pass
    if animate:
        for i in range(0,len(sol)-5,3):
            rc.move(sol[i],0,int(sol[i+1]))
            rc.render()
    return sol[:-5]

def makeData(count):
    data = np.empty((count,55) , dtype=np.str_)
    labels = np.empty(count, dtype=np.int_)
    for i in range(count):
        cb = cubie.CubieCube()
        cb.randomize()
        sol = solveCubie(cb)
        j = 0
        for char in cb.to_facelet_cube().to_string(): data[i][j] = char; j+=1
        labels[i] = hash(sol[0:2])
    return data,labels
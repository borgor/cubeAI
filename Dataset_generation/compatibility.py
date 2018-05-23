from RubiksCube_TwophaseSolver import solver as sv
from RubiksCube_TwophaseSolver import cubie
from RubiksCube_TwophaseSolver.enums import Color
from MagicCube.code import cube as renderer

import numpy as np
import itertools
import sys

#To make things awful, the render and solver disagree on cube orientation.
#This dictionary translates Solver Faces to Renderer Faces
#faceTranslate= {"U":"D", "D":"U", "B":"R", "F":"L", "R":"B", "L":"F"}
#For reference, here is the dict used in the renderer
#facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}

#Therefore, this combines the two into a single table
fd = {Color.D:0, Color.U:1, Color.L:2, Color.R:3, Color.B:4, Color.F:5,
      "D":0, "U":1, "L":2, "R":3, "B":4,"F":5}
ifd = {0:"D", 1:"U", 2:"L", 3:"R", 4:"B", 5:"F"}

def cubie_to_stickers(solvercube):
    #translate the solver's representation to an array of stickers for the renderer
    fc = solvercube.to_facelet_cube()
    s = np.empty(54,dtype = np.int_)
    for i in range(54):
        #Substitutes colors, so that the Solver's orientation is preserved (i.e. solver-up is rendered as up)
        s[i] = fd[fc.f[i]]
        
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
    return cubie_order_to_stickers_order(s)

def cubie_order_to_stickers_order(s):
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

def stickersToCubieOrder(rendererCube):
    reverse = np.array(
        [[[ 6,  3,  0],
        [ 7,  4,  1],
        [ 8,  5,  2]],

       [[33, 30, 27],
        [34, 31, 28],
        [35, 32, 29]],

       [[24, 21, 18],
        [25, 22, 19],
        [26, 23, 20]],

       [[51, 48, 45],
        [52, 49, 46],
        [53, 50, 47]],

       [[15, 12,  9],
        [16, 13, 10],
        [17, 14, 11]],

       [[42, 39, 36],
        [43, 40, 37],
        [44, 41, 38]]])

    result = np.empty(54, dtype=np.int_)
    for i,j,k in itertools.product(range(6),range(3),range(3)):
        result[reverse[i][j][k]] = rendererCube.stickers[i][j][k]
    return result
        
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
    data = np.empty((count,54) , dtype=np.int_)
    labels = np.empty(count, dtype=np.int_)
    sol = ""
    cb = cubie.CubieCube()
    rc = renderer.Cube(3)
    for i in range(count):
        if not sol:
            cb.randomize()
            sol = solveCubie(cb)
            rc.stickers = cubie_to_stickers(cb)
            
        data[i] = stickersToCubieOrder(rc)
        labels[i] = fd[sol[0]] *3 + int(sol[1])-1
        rc.move(sol[0],0,int(sol[1]))
        sol = sol[3:]
        if (not i%100):
            sys.stdout.write("Iterations complete: " + str(i) + "\r")
    return data,labels

def is_solved(renderercube):
    for face in renderercube.stickers:
        if not len(np.unique(face)) == 1:
            return False
    return True

def testAiSolver(model, maxmoves = 60):
    cb = cubie.CubieCube()
    cb.randomize()
    c = renderer.Cube(3)
    c.stickers = cubie_to_stickers(cb)
    states = np.empty((maxmoves,54) , dtype=np.int_)
    for i in range(maxmoves):
        states[i] = stickersToCubieOrder(c)
        print(states[i])
        move = model.predict_classes(states[i:i+1])
        movef = ifd[int(move/3)]
        movet = int((move%3)+1)
        ##Verify move correctness and try cycle detection
        print(movef,movet)
        c.move(movef,0,movet)
        if is_solved(c):
            print("solved")
            break
            

def nn_to_DFS_acyclic(model, maxdepth = 60, state = np.array(0), already_explored = set()):
    if state.size == 1:
        cb = cubie.CubieCube()
        cb.randomize()
        testcube = renderer.Cube(3)
        testcube.stickers = cubie_to_stickers(cb)
        state = testcube.stickers.copy()
    else:
        testcube = renderer.Cube(3)
        testcube.stickers = state
    if state.tobytes() in already_explored:
        print("Cycle, returning")
        return
    elif is_solved(testcube):
        print("Solved")
        raise Exception
        return
    elif maxdepth <= 0:
        print("Max depth reach")
        return
    already_explored.add(state.tobytes())
    predictions = model.predict(state.reshape(1,54))
    testcube = renderer.Cube(3)
    moves = list(zip(list(range(18)),predictions.reshape(18).tolist()))
    moves.sort(key = lambda e:e[1])
    for move,p in moves:
        testcube.stickers = state.copy()
        movef = ifd[int(move/3)]
        movet = int((move%3)+1)
        testcube.move(movef,0,movet)
        nn_to_DFS_acyclic(model, maxdepth-1, testcube.stickers, already_explored)
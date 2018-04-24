from RubiksCube_TwophaseSolver import solver as sv
from RubiksCube_TwophaseSolver import cubie
from RubiksCube_TwophaseSolver.enums import Color
from MagicCube.code import cube as renderer

import numpy as np

def cubie_to_stickers(solvercube):
    #translate the solver's representation to an array of stickers for the renderer
    fc = solvercube.to_facelet_cube()
    s = []
    for i in range(54):
        if fc.f[i] == Color.U:
            s.append(0)
        elif fc.f[i] == Color.R:
            s.append(4)
        elif fc.f[i] == Color.F:
            s.append(2)
        elif fc.f[i] == Color.D:
            s.append(1)
        elif fc.f[i] == Color.L:
            s.append(5)
        elif fc.f[i] == Color.B:
            s.append(3)

    a = np.array([
        [s[0:3],s[3:6],s[6:9]], #U
        [s[27:30], s[30:33], s[33:36]], #D
        [s[18:21],s[21:24],s[24:27]], #F
        [s[45:48],s[48:51],s[51:54]], #B
        [s[9:12],s[12:15],s[15:18]], #R
        [s[36:39],s[39:42],s[42:45]], #L
        ])
    return a

cubie.CubieCube.to_stickers = cubie_to_stickers



def rendercubie(self):
    rc = renderer.Cube(3)
    rc.stickers = self.to_stickers()
    img = rc.render()
    return img

cubie.CubieCube.render = rendercubie

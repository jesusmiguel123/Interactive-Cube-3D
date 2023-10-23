import pygame
import numpy as np

from lib.Wireframe import Wireframe
from lib.ProjectionViewer import ProjectionViewer

actions = {
    pygame.K_LEFT:   (lambda x: x.translateAll([-0.1, 0, 0])),
    pygame.K_RIGHT:  (lambda x: x.translateAll([ 0.1, 0, 0])),
    pygame.K_DOWN:   (lambda x: x.translateAll([0,-0.1, 0])),
    pygame.K_UP:     (lambda x: x.translateAll([0, 0.1, 0])),
    pygame.K_z:      (lambda x: x.translateAll([0, 0, -0.1])),
    pygame.K_x:      (lambda x: x.translateAll([0, 0, 0.1])),
    pygame.K_PLUS:   (lambda x: x.scaleAll(1.005)),
    pygame.K_MINUS:  (lambda x: x.scaleAll(0.995)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.005)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.005)),
    pygame.K_e:      (lambda x: x.rotateAll('Y',  0.005)),
    pygame.K_r:      (lambda x: x.rotateAll('Y', -0.005)),
    pygame.K_t:      (lambda x: x.rotateAll('Z',  0.005)),
    pygame.K_y:      (lambda x: x.rotateAll('Z', -0.005)),
    pygame.K_a:      (lambda x: x.rotateAxis('X',  0.005)),
    pygame.K_s:      (lambda x: x.rotateAxis('X', -0.005)),
    pygame.K_d:      (lambda x: x.rotateAxis('Y',  0.005)),
    pygame.K_f:      (lambda x: x.rotateAxis('Y', -0.005)),
    pygame.K_g:      (lambda x: x.rotateAxis('Z',  0.005)),
    pygame.K_h:      (lambda x: x.rotateAxis('Z', -0.005)),
    pygame.K_j:      (lambda x: x.rotateCAxis(0.005)),
    pygame.K_k:      (lambda x: x.rotateCAxis(-0.005))
}

def main(a, b, c, p_x, p_y, p_z):
    nor = (a*a + b*b + c*c)**0.5

    pv = ProjectionViewer(
        700, 700, actions,
        a/nor, b/nor, c/nor,
        p_x, p_y, p_z
    )

    cube = Wireframe()

    cube_nodes = [
        (x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)
    ]

    faces = (
        (0, 2, 6, 4),
        (1, 3, 7, 5),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 2, 3, 1),
        (4, 5, 7, 6),
    )

    cube.addNodes(np.array(cube_nodes))
    cube.addEdges(
        [(n,n+4) for n in range(0,4)] + \
        [(n,n+1) for n in range(0,8,2)] + \
        [(n,n+2) for n in (0,1,4,5)]
    )
    cube.addFaces(faces)

    pv.addWireframe(cube)
    pv.run()

if __name__ == '__main__':
    print("--- X -> Red - Y -> Green - Z -> Blue ---")
    print("Commands:")
    print("  Scale:")
    print("    Up   -> PLUS KEY")
    print("    Down -> MINUS KEY")
    print("  Translate:")
    print("    X: LEFT (<-) | RIGHT (->)")
    print("    Y: DOWN (<-) | UP    (->)")
    print("    Z:    z (<-) | x     (->)")
    print("  Rotate:")
    print("    Self:                  Axis:")
    print("      X: q (<-) | w (->)          X: a (<-) | s (->)")
    print("      Y: e (<-) | r (->)          Y: d (<-) | f (->)")
    print("      Z: t (<-) | y (->)          Z: g (<-) | h (->)")
    print("                             Custom: j (<-) | k (->)")
    print("Custom Axis Equation:")
    print("  (x, y, z) = (A*X, B*Y, C*Z) + (Px, Py, Pz)")

    a = float(input("Enter A param: "))
    b = float(input("Enter B param: "))
    c = float(input("Enter C param: "))

    p_x = float(input("Enter Px param: "))
    p_y = float(input("Enter Py param: "))
    p_z = float(input("Enter Pz param: "))

    print("Your Custom Axis Equation is:")
    print(f"  (x, y, z) = ({a}*X, {b}*Y, {c}*Z) + ({p_x}, {p_y}, {p_z})")
    main(a, b, c, p_x, p_y, p_z)
import pygame as pg
import Vectors3D as v3d

pg.init()

w = 500
h = 500
screen = pg.display.set_mode((w, h))
pg.display.set_caption(("v3d"))
clock = pg.time.Clock()
fps = 60

#create a cube
verts = [v3d.Vertice(-1, -1, 1), v3d.Vertice(-1, 1, 1), v3d.Vertice(1, 1, 1), v3d.Vertice(1, -1, 1), v3d.Vertice(1, -1, -1), v3d.Vertice(-1, -1, -1), v3d.Vertice(1, 1, -1), v3d.Vertice(-1, 1, -1)]
edges = [v3d.Edge(verts[2], verts[3]), v3d.Edge(verts[2], verts[-2]), v3d.Edge(verts[2], verts[1]), v3d.Edge(verts[1], verts[-1]), v3d.Edge(verts[-2], verts[-1]), v3d.Edge(verts[-2], verts[4]), v3d.Edge(verts[4], verts[3]), v3d.Edge(verts[4], verts[5]), v3d.Edge(verts[3], verts[0]), v3d.Edge(verts[0], verts[1]), v3d.Edge(verts[0], verts[5]), v3d.Edge(verts[5], verts[-1])]
faces = [v3d.Face([verts[0], verts[1], verts[-1], verts[5]]), v3d.Face([verts[1], verts[-1], verts[6], verts[2]]), v3d.Face([verts[2], verts[3], verts[0], verts[1]]), v3d.Face([verts[0], verts[3], verts[4], verts[5]]), v3d.Face([verts[3], verts[2], verts[6], verts[4]]), v3d.Face([verts[5], verts[-1], verts[6], verts[4]])]
cube = v3d.Mesh([0, 0, 0], [0, 0, 0], [1, 1, 1], verts, edges, faces)

#create a camera
camera = v3d.Camera([-50, 0, 0], [0, 0, 0], [1, 1, 1], w, h, 30)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    key = pg.key.get_pressed()
    if key[pg.K_w]:
        camera.set_pos([camera.position[0] + 1, camera.position[1], camera.position[2]])
    elif key[pg.K_s]:
        camera.set_pos([camera.position[0] - 1, camera.position[1], camera.position[2]])
    elif key[pg.K_a]:
        camera.set_pos([camera.position[0], camera.position[1] + 1, camera.position[2]])
    elif key[pg.K_d]:
        camera.set_pos([camera.position[0], camera.position[1] - 1, camera.position[2]])

    camera.project([cube])

    for vert in cube.vertices:
        pg.draw.circle(screen, (255, 255, 255), vert.screenPos, 2, 0)

    clock.tick(fps)
    pg.display.update()
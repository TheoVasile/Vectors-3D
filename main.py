import pygame as pg
import Vectors3D as v3d
import math

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

camera = v3d.Camera([-50, 0, 0], [0, 0, 0], [1, 1, 1], w, h, 30) #camera displays scene

objects = [cube, camera] #list of all objects in the scene
selectedObject = None
selectedCamera = camera

oldPos = pg.mouse.get_pos()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                if selectedObject:
                    if selectedObject.mode == "object":
                        selectedObject.mode = "edit"
                    elif selectedObject.mode == "edit":
                        selectedObject.mode = "object"

    screen.fill((0, 0, 0))

    if selectedObject:
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            selectedCamera.fov += 1
        elif key[pg.K_DOWN]:
            selectedCamera.fov -= 1
        if key[pg.K_w]:
            selectedCamera.set_pos([selectedCamera.position[0] + 1, selectedCamera.position[1], selectedCamera.position[2]])
        elif key[pg.K_s]:
            selectedCamera.set_pos([selectedCamera.position[0] - 1, selectedCamera.position[1], selectedCamera.position[2]])
        if key[pg.K_a]:
            selectedObject.set_rot([selectedObject.get_rot()[0] + 1, selectedObject.get_rot()[1] + 5, selectedObject.get_rot()[2] + 1])
        elif key[pg.K_d]:
            selectedObject.set_rot([selectedObject.get_rot()[0], selectedObject.get_rot()[1], selectedObject.get_rot()[2] - 5])

        if pg.mouse.get_pressed()[0]:
            selectedObject.set_pos([selectedObject.position[0], selectedObject.position[1] + (pg.mouse.get_pos()[0] - oldPos[0]) / 10, selectedObject.position[2] + (pg.mouse.get_pos()[1] - oldPos[1]) / 10])
        if key[pg.K_r]:
            selectedObject.set_rot([selectedObject.rotation[0], selectedObject.rotation[1] - (pg.mouse.get_pos()[1] - oldPos[1]), selectedObject.rotation[2] - (pg.mouse.get_pos()[0] - oldPos[0])])

    #selectedObject.set_rot([45, 45, 75])

    selectedCamera.project(objects)

    for ob in objects:
        if isinstance(ob, v3d.Mesh):
            for tri in ob.tris:
                angle = math.degrees(math.acos(v3d.dotProduct(tri.normal, selectedCamera.cameraVector) / (v3d.dist(tri.normal, [0, 0, 0]) * v3d.dist(selectedCamera.cameraVector, [0, 0, 0]))))
                angle = math.degrees(math.asin(math.sin(math.radians(angle))))
                color = [int(255 * ((90 - angle) / 90)), int(255 * ((90 - angle) / 90)), int(255 * ((90 - angle) / 90))]
                pg.draw.polygon(screen, color, [vert.screenPos for vert in tri.vertices], 0)
                edgeColor = (255, 255, 255)
                if ob == selectedObject:
                    edgeColor = (255, 200, 0)
                if ob.mode == "edit":
                    for vert in tri.vertices:
                        pg.draw.circle(screen, edgeColor, vert.screenPos, 2, 0)
                if ob.mode == "edit" or (ob.mode == "object" and ob == selectedObject):
                    for edge in tri.edges:
                        pg.draw.line(screen, edgeColor, (edge.vert1.screenPos), (edge.vert2.screenPos), 1)

        pivotPoint = selectedCamera.projectPoint(ob.position)
        pg.draw.circle(screen, (255, 200, 0), [int(pivotPoint[0]), int(pivotPoint[1])], 2, 0)

    oldPos = pg.mouse.get_pos()

    clock.tick(fps)
    pg.display.update()
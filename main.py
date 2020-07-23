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

camera = v3d.Camera([-25, 0, 0], [0, 0, 0], [1, 1, 1], w, h, 30) # camera displays scene

objects = [cube, camera] # list of all objects in the scene
selectedObject = None
selectedCamera = camera

rotate = False # indicates wether or not the selected object is in the process of being rotated
move = False # indicates wether or not the selected object is in the process of being moved

oldPos = pg.mouse.get_pos()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                if selectedObject:
                    # switches the mode of the selected object
                    if selectedObject.mode == "object":
                        selectedObject.mode = "edit"
                    elif selectedObject.mode == "edit":
                        selectedObject.mode = "object"
            # switches wether or not the selected object is in the process of moving
            elif event.key == pg.K_g and selectedObject:
                if move == True:
                    move = False
                elif move == False:
                    move = True
            # switches wether or not the selected object is in the process of rotating
            elif event.key == pg.K_r and selectedObject:
                if rotate == True:
                    rotate = False
                elif rotate == False:
                    rotate = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                # clicking while moving or rotating applies the action
                if move or rotate:
                    move = False
                    rotate = False
                # otherwise it detects which object the cursor lands on and makes it the selected object
                elif not move and not rotate:
                    selectedObject = selectedCamera.selectObject(objects, pg.mouse.get_pos())

    screen.fill((0, 0, 0))

    key = pg.key.get_pressed()
    # alter the cameras fov
    if key[pg.K_UP]:
        selectedCamera.fov += 1
    elif key[pg.K_DOWN]:
        selectedCamera.fov -= 1

    #alter the cameras position
    if key[pg.K_w]:
        selectedCamera.set_pos([selectedCamera.position[0] + 1, selectedCamera.position[1], selectedCamera.position[2]])
    elif key[pg.K_s]:
        selectedCamera.set_pos([selectedCamera.position[0] - 1, selectedCamera.position[1], selectedCamera.position[2]])

    # move or rotate object if needed
    if selectedObject:
        if move:
            selectedObject.set_pos([selectedObject.position[0], selectedObject.position[1] + (pg.mouse.get_pos()[0] - oldPos[0]) / 10, selectedObject.position[2] + (pg.mouse.get_pos()[1] - oldPos[1]) / 10])
        if rotate:
            selectedObject.set_rot([selectedObject.rotation[0], selectedObject.rotation[1] - (pg.mouse.get_pos()[1] - oldPos[1]), selectedObject.rotation[2] - (pg.mouse.get_pos()[0] - oldPos[0])])

    # project all the objects onto the camera
    selectedCamera.project(objects)

    for ob in objects:
        if isinstance(ob, v3d.Mesh):
            for tri in ob.tris:
                # displays a face
                angle = math.degrees(math.acos(v3d.dotProduct(tri.normal, selectedCamera.cameraVector) / (v3d.dist(tri.normal, [0, 0, 0]) * v3d.dist(selectedCamera.cameraVector, [0, 0, 0]))))
                angle = math.degrees(math.asin(math.sin(math.radians(angle))))
                # the closer the angle between the normal and the direction of the camera is to 90 degrees, the darker the color
                # the closer the angle between the normal and the direction of the camera is to 0 degrees, the lighter the color
                color = [int(255 * ((90 - angle) / 90)), int(255 * ((90 - angle) / 90)), int(255 * ((90 - angle) / 90))]
                pg.draw.polygon(screen, color, [vert.screenPos for vert in tri.vertices], 0)
                # selected objects have yellow edges
                edgeColor = (255, 255, 255)
                if ob == selectedObject:
                    edgeColor = (255, 200, 0)
                if ob.mode == "edit":
                    for vert in tri.vertices:
                        pg.draw.circle(screen, edgeColor, vert.screenPos, 2, 0)
                # edges should only be displayed if the object is selected or in edit mode
                if ob.mode == "edit" or (ob.mode == "object" and ob == selectedObject):
                    for edge in tri.edges:
                        pg.draw.line(screen, edgeColor, (edge.vert1.screenPos), (edge.vert2.screenPos), 1)

        pivotPoint = selectedCamera.projectPoint(ob.position)
        pg.draw.circle(screen, (255, 200, 0), [int(pivotPoint[0]), int(pivotPoint[1])], 2, 0)

    oldPos = pg.mouse.get_pos()

    clock.tick(fps)
    pg.display.update()
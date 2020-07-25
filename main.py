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
#faces = [v3d.Face([verts[0], verts[1], verts[-1], verts[5]]), v3d.Face([verts[1], verts[-1], verts[6], verts[2]]), v3d.Face([verts[2], verts[3], verts[0], verts[1]]), v3d.Face([verts[0], verts[3], verts[4], verts[5]]), v3d.Face([verts[3], verts[2], verts[6], verts[4]]), v3d.Face([verts[5], verts[-1], verts[6], verts[4]])]
#cube = v3d.Mesh([0, 0, 0], [0, 0, 0], [1, 1, 1], verts, edges, faces)

camera = v3d.Camera([-25, 0, 0], [0, 0, 0], [1, 1, 1], w, h, 30) # camera displays scene

objects = [v3d.createSphere(32, 12), camera] # list of all objects in the scene
selectedObject = objects[0]
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
            elif event.key == pg.K_z:
                if selectedCamera.displayType == "solid":
                    selectedCamera.displayType = "wireframe"
                elif selectedCamera.displayType == "wireframe":
                    selectedCamera.displayType = "solid"
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                # clicking while moving or rotating applies the action
                if move or rotate:
                    move = False
                    rotate = False

                # otherwise it detects what the cursor lands on
                elif not move and not rotate:
                    try:
                        if selectedObject.mode == "edit":
                            selectedVertice = selectedObject.selectVert(pg.mouse.get_pos())
                            if selectedVertice:
                                selectedObject.selectedVertices = [selectedVertice]
                        else:
                            raise Exception
                    except:
                        if selectedObject:
                            selectedObject.selected = False

                        selectedObject = selectedCamera.selectObject(objects, pg.mouse.get_pos())
                        if selectedObject:
                            selectedObject.selected = True

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
    selectedCamera.display(objects)

    oldPos = pg.mouse.get_pos()

    clock.tick(fps)
    pg.display.update()
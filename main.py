import pygame as pg

pg.init()

w = 500
h = 500
screen = pg.display.set_mode((w, h))
pg.display.set_caption(("v3d"))
clock = pg.time.Clock()
fps = 60

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    clock.tick(fps)
    pg.display.update()
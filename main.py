import pygame
from pygame.locals import *

from gl import Renderer
import shaders

delta_time = 0.0

pygame.init()
clock = pygame.time.Clock()

SCREEN_SIZE = (960, 540)
SCREEN = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | OPENGL)

renderer = Renderer(SCREEN)
renderer.set_shaders(shaders.vertex_shader, shaders.fragment_shader)
renderer.create_objects()

cube_x = 0
cube_z = 0

isRunning = True

while isRunning: 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        cube_x -= 2 * delta_time
    
    if keys[pygame.K_d]:
        cube_x += 2 * delta_time
    
    if keys[pygame.K_w]:
        cube_z -= 2 * delta_time
    
    if keys[pygame.K_s]:
        cube_z += 2 * delta_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                renderer.filled_mode()

            elif event.key == pygame.K_2:
                renderer.wireframe_mode      

            elif event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.translate_cube(cube_x, 0, cube_z)

    renderer.render()

    pygame.display.flip()
    clock.tick(60)
    delta_time = clock.get_time() / 1000

pygame.quit()
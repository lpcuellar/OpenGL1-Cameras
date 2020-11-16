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
camera_x = 0
camera_z = 3
camera_pitch = 0
camera_yaw = 0
camera_roll = 0


isRunning = True

while isRunning: 
    keys = pygame.key.get_pressed()
    ##  CUBE TRANSLATION
    if keys[pygame.K_a]:
        cube_x -= 2 * delta_time
    
    if keys[pygame.K_d]:
        cube_x += 2 * delta_time
    
    if keys[pygame.K_w]:
        cube_z -= 2 * delta_time
    
    if keys[pygame.K_s]:
        cube_z += 2 * delta_time

    ##  CAMERA TRANSLATION
    if keys[pygame.K_UP]:
        camera_z += 2 * delta_time
    
    if keys[pygame.K_DOWN]:
        camera_z -= 2 * delta_time
    
    if keys[pygame.K_LEFT]:
        camera_x -= 2 * delta_time
    
    if keys[pygame.K_RIGHT]:
        camera_x += 2 * delta_time

    ##  CAMERA ROTATION
    if keys[pygame.K_q]:
        camera_yaw += 20 * delta_time
    
    if keys[pygame.K_e]:
        camera_yaw -= 20 * delta_time

    if keys[pygame.K_r]:
        camera_pitch += 20 * delta_time
    
    if keys[pygame.K_f]:
        camera_pitch -= 20 * delta_time
    
    if keys[pygame.K_x]:
        camera_roll -= 20 * delta_time

    if keys[pygame.K_c]:
        camera_roll += 20 * delta_time
    
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
    renderer.translate_camera(camera_x, 0, camera_z)
    renderer.rotate_camera(camera_pitch, camera_yaw, camera_roll)

    renderer.render()

    pygame.display.flip()
    clock.tick(60)
    delta_time = clock.get_time() / 1000

pygame.quit()
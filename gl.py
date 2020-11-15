from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader

import glm
import numpy as np

rect_verts = np.array([
    #   VERTICES            #   COLOR
    0.5,    0.5,    0.5,    1, 0, 0,
    0.5,    -0.5,   0.5,    0, 1, 0, 
    -0.5,   -0.5,   0.5,    0, 0, 1,
    -0.5,   0.5,    0.5,    1, 1, 0,
    0.5,    0.5,    -0.5,   1, 0, 1,
    0.5,    -0.5,   -0.5,   0, 1, 1,
    -0.5,   -0.5,   -0.5,   1, 1, 1,
    -0.5,   0.5,    -0.5,    0, 0, 0
], dtype=np.float32)

rect_indices = np.array([
    #   FRONT
    0, 1, 3,
    1, 2, 3, 
    #   LEFT
    4, 5, 0,
    5, 1, 0,
    #   BACK
    7, 6, 4,
    6, 5, 4,
    #   RIGHT
    3, 2, 7, 
    2, 6, 7, 
    #   TOP
    1, 5, 2,
    5, 6, 2,
    #   BOTTOM 
    4, 0, 7, 
    0, 3, 7
], dtype=np.uint32)

class Renderer(object):
    def __init__(self, screen):
        self.SCREEN = screen
        _, _, self.WIDTH, self.HEIGHT = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.WIDTH, self.HEIGHT)

        self.projection = glm.perspective(glm.radians(60), self.WIDTH / self.HEIGHT, 0.1, 1000)

        self.cube_position = glm.vec3(0, 0, 0)

    def wireframe_mode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filled_mode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def translate_cube(self, x, y, z):
        self.cube_position = glm.vec3(x, y, z)

    def set_shaders(self, vertex_shader, fragment_shader):
        if vertex_shader is not None or fragment_shader is not None:
            self.active_shader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER),
            )
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    def create_objects(self):
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, rect_verts.nbytes, rect_verts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rect_indices.nbytes, rect_indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        i = glm.mat4(1)

        translate = glm.translate(i, self.cube_position)

        pitch   =   glm.rotate(i, glm.radians(0), glm.vec3(1, 0, 0))
        yaw     =   glm.rotate(i, glm.radians(0), glm.vec3(0, 1, 0))
        roll    =   glm.rotate(i, glm.radians(0), glm.vec3(0, 0, 1))

        rotate  =   pitch * yaw * roll
        scale   =   glm.scale(i, glm.vec3(1, 1, 1))
        model   =   translate * rotate * scale

        camera_translate    =   glm.translate(i, glm.vec3(0, 0, 3))
        camera_pitch        =   glm.rotate(i, glm.radians(0), glm.vec3(1, 0, 0))
        camera_yaw          =   glm.rotate(i, glm.radians(0), glm.vec3(0, 1, 0))
        camera_roll         =   glm.rotate(i, glm.radians(0), glm.vec3(0, 0, 1))
        camera_rotate       =   camera_pitch * camera_yaw * camera_roll

        view = glm.inverse(camera_translate * camera_rotate)

        if self.active_shader:
            glUniformMatrix4fv(
                glGetUniformLocation(self.active_shader, 'model'),
                1, GL_FALSE, glm.value_ptr(model)
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.active_shader, 'view'),
                1, GL_FALSE, glm.value_ptr(view)
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.active_shader, 'projection'),
                1, GL_FALSE, glm.value_ptr(self.projection)
            )

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)



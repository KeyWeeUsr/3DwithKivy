# python
from random import random

# kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation

# kivy3
from kivy3 import Renderer, Scene
from kivy3 import PerspectiveCamera

# geometry
from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh


class My3D(App):
    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def rotate_cube(self, *dt):
        for cube in self.cubes:
            cube.rotation.y += 1

    def scale_cube(self, *dt):
        for cube in self.cubes:
            factor = random()
            anim = Animation(x=factor)
            anim &= Animation(y=factor)
            anim &= Animation(z=factor)
            anim.start(cube.scale)

    def build(self):
        layout = GridLayout(cols=3)

        # create renderer
        self.renderer = Renderer(size_hint=(5, 5))
        self.renderer.set_clear_color(
            (0.1, 0.1, 0.1, 1)
        )  # rgba

        # create scene
        scene = Scene()
        self.cubes = []

        # create cubes for scene
        #
        # default pure green cube
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material(
            color=(0, 0.5, 0)  # base color
        )
        self.cubes.append(Mesh(
            geometry=cube_geo,
            material=cube_mat
        ))  # default pos == (0, 0, 0)
        self.cubes[0].pos.z = -5
        self.cubes[0].pos.x = 1
        self.cubes[0].pos.y = 0.8
        self.cubes[0].rotation.x = 45

        # black cube, red shadow, half-transparent
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material(
            transparency=0.5,
            color=(0, 0, 0),  # base color
            diffuse=(10, 0, 0),  # color of "shadows"
            specular=(0, 0, 0)  # mirror-like reflections
        )
        self.cubes.append(Mesh(
            geometry=cube_geo,
            material=cube_mat
        ))  # default pos == (0, 0, 0)
        self.cubes[1].pos.z = -5
        self.cubes[1].pos.x = -1
        self.cubes[1].pos.y = 0.8
        self.cubes[1].rotation.y = 45

        # default pure green cube with red reflections
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material(
            transparency=1,
            color=(0, 0.5, 0),  # base color
            diffuse=(0, 0, 0),  # color of "shadows"
            specular=(10, 0, 0)  # mirror-like reflections
        )
        self.cubes.append(Mesh(
            geometry=cube_geo,
            material=cube_mat
        ))  # default pos == (0, 0, 0)
        self.cubes[2].pos.z = -5
        self.cubes[2].pos.x = 1
        self.cubes[2].pos.y = -0.8
        self.cubes[2].rotation.z = 45

        # black cube with red reflections
        # and half-transparent
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material(
            transparency=0.5,
            color=(0, 0, 0),  # base color
            specular=(10, 0, 0)  # mirror-like reflections
        )
        self.cubes.append(Mesh(
            geometry=cube_geo,
            material=cube_mat
        ))  # default pos == (0, 0, 0)
        self.cubes[3].pos.z = -5
        self.cubes[3].pos.x = -1
        self.cubes[3].pos.y = -0.8
        self.cubes[3].rotation.x = 45

        # create camera for scene
        self.camera = PerspectiveCamera(
            fov=75,    # distance from the screen
            aspect=0,  # "screen" ratio
            near=1,    # nearest rendered point
            far=10     # farthest rendered point
        )

        # start rendering the scene and camera
        for cube in self.cubes:
            scene.add(cube)
        self.renderer.render(scene, self.camera)

        # set renderer ratio is its size changes
        # e.g. when added to parent
        self.renderer.bind(size=self._adjust_aspect)

        for _ in range(4):
            layout.add_widget(Label())

        layout.add_widget(self.renderer)

        for t in ['+\n\nY\n\n-', '-      X      +']:
            layout.add_widget(Label(text=t))
            layout.add_widget(Label())

        Clock.schedule_interval(self.rotate_cube, .01)
        Clock.schedule_interval(self.scale_cube, 1)
        return layout
My3D().run()

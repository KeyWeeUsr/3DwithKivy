# kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

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
        self.cube.rotation.y += 1

    def build(self):
        layout = FloatLayout()

        # create renderer
        self.renderer = Renderer()

        # create scene
        scene = Scene()

        # create default cube for scene
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material()
        self.cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )  # default pos == (0, 0, 0)
        self.cube.pos.z = -5

        # create camera for scene
        self.camera = PerspectiveCamera(
            fov=75,    # distance from the screen
            aspect=0,  # "screen" ratio
            near=1,    # nearest rendered point
            far=10     # farthest rendered point
        )

        # start rendering the scene and camera
        scene.add(self.cube)
        self.renderer.render(scene, self.camera)

        # set renderer ratio is its size changes
        # e.g. when added to parent
        self.renderer.bind(size=self._adjust_aspect)

        layout.add_widget(self.renderer)
        Clock.schedule_interval(self.rotate_cube, .01)
        return layout
My3D().run()

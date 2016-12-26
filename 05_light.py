# coding: utf-8

# fullscreen setup
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

# python
from random import random

# kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation

# kivy3
from kivy3 import Renderer, Scene
from kivy3 import PerspectiveCamera

# geometry
from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh


Builder.load_string('''
<MoveButton>:
    on_release: self.move(self.main_cube, self.text)

<CamRot@GridLayout>:
    cols: 3
    Widget:
    MoveButton:
        text: 'rup'
    Widget:
    MoveButton:
        text: 'rleft'
    Label:
        text: 'cam\\nrot'
    MoveButton:
        text: 'rright'
    Widget:
    MoveButton:
        text: 'rdown'

<CamNav@GridLayout>:
    cols: 3
    Widget:
    MoveButton:
        text: 'mup'
    MoveButton:
        text: 'mforw'
    MoveButton:
        text: 'mleft'
    Label:
        text: 'cam\\npos'
    MoveButton:
        text: 'mright'
    MoveButton:
        text: 'mback'
    MoveButton:
        text: 'mdown'

<CamStrafe@GridLayout>:
    cols: 3
    Widget:
    MoveButton:
        text: 'sup'
    Widget:
    MoveButton:
        text: 'sleft'
    Label:
        text: 'cam\\nstrafe'
    MoveButton:
        text: 'sright'
    Widget:
    MoveButton:
        text: 'sdown'

<ObjNav@GridLayout>:
    cols: 3
    MoveButton:
        text: 'z-'
    MoveButton:
        text: 'up'
    Widget:
    MoveButton:
        text: 'left'
    Label:
        text: 'cube\\npos'
    MoveButton:
        text: 'right'
    Widget:
    MoveButton:
        text: 'down'
    MoveButton:
        text: 'z+'

<LightPos@GridLayout>:
    cols: 3
    Widget:
    MoveButton:
        text: 'lup'
    MoveButton:
        text: 'l+'
    MoveButton:
        text: 'lleft'
    Label:
        text: 'light\\npos'
    MoveButton:
        text: 'lright'
    MoveButton:
        text: 'l-'
    MoveButton:
        text: 'ldown'

<LightPanel@BoxLayout>:
    Widget:
    LightPos:
    Widget:
''')


class MoveButton(Button):
    def __init__(self, **kwargs):
        super(MoveButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.main_cube = self.app.main_cube

    def move(self, cube, direc, *args):
        # move cube object
        if direc == 'up':
            cube.pos.y += .1
        elif direc == 'down':
            cube.pos.y -= .1
        elif direc == 'right':
            cube.pos.x += .1
        elif direc == 'left':
            cube.pos.x -= .1
        elif direc == 'z+':
            cube.pos.z += .1
        elif direc == 'z-':
            cube.pos.z -= .1

        # rotate camera
        elif direc == 'rup':
            # rotation _around_ the axis,
            # not in the _direction_ of the axis
            #        →
            #       / \
            # - - - |- - - - X
            #       \_/
            #
            self.app.camera.rot.x -= 10
            self.app.camera.look_at(cube.pos)
        elif direc == 'rdown':
            self.app.camera.rot.x += 10
            self.app.camera.look_at(cube.pos)
        elif direc == 'rright':
            self.app.camera.rot.y += 1
            self.app.camera.look_at(cube.pos)
        elif direc == 'rleft':
            self.app.camera.rot.y -= 1
            self.app.camera.look_at(cube.pos)

        # move camera, but still look at cube
        elif direc == 'mforw':
            self.app.camera.pos.z -= .1
        elif direc == 'mback':
            self.app.camera.pos.z += .1
        elif direc == 'mup':
            self.app.camera.pos.y += 1
            self.app.camera.look_at(cube.pos)
        elif direc == 'mdown':
            self.app.camera.pos.y -= 1
            self.app.camera.look_at(cube.pos)
        elif direc == 'mright':
            self.app.camera.pos.x += 1
            self.app.camera.look_at(cube.pos)
        elif direc == 'mleft':
            self.app.camera.pos.x -= 1
            self.app.camera.look_at(cube.pos)

        # strafe camera
        elif direc == 'sup':
            self.app.camera.pos.y += 1
            self.app.camera.look_at(
                self.app.camera.pos.x,
                self.app.camera.pos.y,
                self.app.camera.pos.z -1
            )  # look in front of the camera
        elif direc == 'sdown':
            self.app.camera.pos.y -= 1
            self.app.camera.look_at(
                self.app.camera.pos.x,
                self.app.camera.pos.y,
                self.app.camera.pos.z -1
            )
        elif direc == 'sleft':
            self.app.camera.pos.x -= 1
            self.app.camera.look_at(
                self.app.camera.pos.x,
                self.app.camera.pos.y,
                self.app.camera.pos.z -1
            )
        elif direc == 'sright':
            self.app.camera.pos.x += 1
            self.app.camera.look_at(
                self.app.camera.pos.x,
                self.app.camera.pos.y,
                self.app.camera.pos.z -1
            )

        # move main light
        elif direc == 'lup':
            self.app.renderer.main_light.pos[1] += 10
        elif direc == 'ldown':
            self.app.renderer.main_light.pos[1] -= 10
        elif direc == 'lleft':
            self.app.renderer.main_light.pos[0] -= 10
        elif direc == 'lright':
            self.app.renderer.main_light.pos[0] += 10
        elif direc == 'lforw':
            self.app.renderer.main_light.pos[2] -= 10
        elif direc == 'lback':
            self.app.renderer.main_light.pos[2] += 10
        elif direc == 'l+':
            self.app.renderer.main_light.intensity += 10
        elif direc == 'l-':
            self.app.renderer.main_light.intensity -= 10


class Listener(Widget):
    def __init__(self, **kwargs):
        super(Listener, self).__init__(**kwargs)
        app = App.get_running_app()
        self.cube = app.main_cube
        self.movebutton = MoveButton()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # camera rotation
        if keycode[1] == 'w':
            self.movebutton.move(self.cube, 'rup')
        elif keycode[1] == 'a':
            self.movebutton.move(self.cube, 'rleft')
        elif keycode[1] == 's':
            self.movebutton.move(self.cube, 'rdown')
        elif keycode[1] == 'd':
            self.movebutton.move(self.cube, 'rright')

        # camera strafe
        elif keycode[1] == 't':
            self.movebutton.move(self.cube, 'sup')
        elif keycode[1] == 'f':
            self.movebutton.move(self.cube, 'sleft')
        elif keycode[1] == 'g':
            self.movebutton.move(self.cube, 'sdown')
        elif keycode[1] == 'h':
            self.movebutton.move(self.cube, 'sright')

        # camera move
        elif keycode[1] == 'i':
            self.movebutton.move(self.cube, 'mup')
        elif keycode[1] == 'j':
            self.movebutton.move(self.cube, 'mleft')
        elif keycode[1] == 'k':
            self.movebutton.move(self.cube, 'mdown')
        elif keycode[1] == 'l':
            self.movebutton.move(self.cube, 'mright')
        elif keycode[1] == 'u':
            self.movebutton.move(self.cube, 'mforw')
        elif keycode[1] == 'o':
            self.movebutton.move(self.cube, 'mback')

        # object move
        elif keycode[1] == 'up':
            self.movebutton.move(self.cube, 'up')
        elif keycode[1] == 'left':
            self.movebutton.move(self.cube, 'left')
        elif keycode[1] == 'down':
            self.movebutton.move(self.cube, 'down')
        elif keycode[1] == 'right':
            self.movebutton.move(self.cube, 'right')
        elif keycode[1] == '.':
            self.movebutton.move(self.cube, 'z-')
        elif keycode[1] == '-':
            self.movebutton.move(self.cube, 'z+')

        # main light move
        elif keycode[1] == 'numpad8':
            self.movebutton.move(self.cube, 'lup')
        elif keycode[1] == 'numpad4':
            self.movebutton.move(self.cube, 'lleft')
        elif keycode[1] == 'numpad2':
            self.movebutton.move(self.cube, 'ldown')
        elif keycode[1] == 'numpad6':
            self.movebutton.move(self.cube, 'lright')
        elif keycode[1] == 'numpadsubstract':
            self.movebutton.move(self.cube, 'l-')
        elif keycode[1] == 'numpadadd':
            self.movebutton.move(self.cube, 'l+')
        elif keycode[1] == 'numpad9':
            self.movebutton.move(self.cube, 'lforw')
        elif keycode[1] == 'numpad1':
            self.movebutton.move(self.cube, 'lback')


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
        cube_geo = BoxGeometry(.3, .3, .3)
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
        cube_geo = BoxGeometry(.3, .3, .3)
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
        cube_geo = BoxGeometry(.3, .3, .3)
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
        cube_geo = BoxGeometry(.3, .3, .3)
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

        cube_geo = BoxGeometry(.3, .3, .3)
        cube_mat = Material(
            transparency=0.5,
            color=(0, 0, 0),  # base color
            specular=(10, 0, 0)
        )
        self.main_cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )  # default pos == (0, 0, 0)
        self.main_cube.rotation.x = 45
        self.main_cube.rotation.y = 45
        self.main_cube.pos.z = -5
        scene.add(self.main_cube)

        planes = [
            ((0, 0, -10), (0, 0, 0)),
            ((-10, 0, 0), (0, -90, 0)),
            ((10, 0, 0), (0, 90, 0)),
            ((0, 0, 10), (0, 180, 0))
        ]  # position and rotation changes
        for plane in planes:
            geo = BoxGeometry(5, 5, .1)
            mat = Material(
                color=(1, 1, 1)
            )
            mesh = Mesh(
                geometry=geo,
                material=mat
            )
            mesh.pos.x += plane[0][0]
            mesh.pos.y += plane[0][1]
            mesh.pos.z += plane[0][2]
            mesh.rot.x += plane[1][0]
            mesh.rot.y += plane[1][1]
            mesh.rot.z += plane[1][2]
            scene.add(mesh)

        # create camera for scene
        self.camera = PerspectiveCamera(
            fov=75,    # distance from the screen
            aspect=0,  # "screen" ratio
            near=.1,    # nearest rendered point
            far=1000     # farthest rendered point
        )

        # start rendering the scene and camera
        for cube in self.cubes:
            scene.add(cube)
        self.renderer.render(scene, self.camera)

        # set renderer ratio is its size changes
        # e.g. when added to parent
        self.renderer.bind(size=self._adjust_aspect)

        layout.add_widget(Factory.CamRot())
        layout.add_widget(Factory.LightPanel())
        layout.add_widget(Factory.CamStrafe())
        layout.add_widget(Widget())

        layout.add_widget(self.renderer)

        layout.add_widget(Label(text='+\n\nY\n\n-'))
        layout.add_widget(Factory.CamNav())
        layout.add_widget(Label(text='-      X      +'))
        layout.add_widget(Factory.ObjNav())

        Clock.schedule_interval(self.rotate_cube, .01)
        Clock.schedule_interval(self.scale_cube, 1)

        # keyboard listener
        Listener()
        return layout
My3D().run()

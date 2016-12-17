# 3DwithKivy
![3D with Kivy](https://raw.github.com/KeyWeeUsr/3DwithKivy/master/3wk.png)

In this repository is code and other stuff from my YouTube tutorial
`3D with Kivy`.

The tutorial is done mainly in Python 2.7, but I try to make the code
as compatible as possible with Python 3.

### Installation

You'll need three main components:

* [Python(2.7, 3.x)](https://www.python.org/downloads/)
* [Kivy](https://kivy.org/docs/installation/installation.html) (preferably
   the latest one)
* [Kivy3](https://github.com/nskrypnik/kivy3)

However, there are still pending some of my pull requests for Kivy3, therefore
until they're merged I made a temporary branch `root` in
[my fork](https://github.com/KeyWeeUsr/kivy3) of Kivy3, which you might want
to use instead, otherwise you'll need to _clone_ the original Kivy3 and patch
some stuff yourself.

Easier path is just using pip and `root` branch.

    $ pip install https://github.com/KeyWeeUsr/kivy3/zipball/root

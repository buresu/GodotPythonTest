from godot import exposed, export
from godot.bindings import *
from godot.globals import *


@exposed
class main(Node):

    def _ready(self):
        print("Hello Godot Python!")
        pass

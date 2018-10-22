from godot import exposed, export
from godot.bindings import *
from godot.globals import *
import cv2
import numpy as np
import cffi

ffi = cffi.FFI()

@exposed
class WebCamSurface(Control):

    image = Image()
    texture = ImageTexture()

    def _ready(self):

        self.cap = cv2.VideoCapture(0)
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.texture.create(int(w), int(h), Image.FORMAT_RGB8, Texture.FLAG_VIDEO_SURFACE)

        pass

    def _process(self, delta):

        ret, frame = self.cap.read()

        if ret:
            h, w = frame.shape[:2]

            # BGR to RGB
            frame = frame[:, :, ::-1]

            # Copy Data
            array = PoolByteArray()
            array.resize(w * h * 3)

            with array.raw_access() as ptr:
                np.frombuffer(ffi.buffer(ptr, w * h * 3), dtype=np.uint8).reshape(h, w, 3)[:] = frame[:]

            self.image.lock()
            self.image.create_from_data(w, h, False, Image.FORMAT_RGB8, array)
            self.image.unlock()

            # Upload Texture
            self.texture.set_data(self.image)

        pass

    def _draw(self):
        self.draw_texture(self.texture, Vector2(0, 0), Color(1, 1, 1, 1), Texture())
        pass

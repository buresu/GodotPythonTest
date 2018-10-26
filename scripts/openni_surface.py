from godot import exposed, export
from godot.bindings import *
from godot.globals import *
from openni import openni2
import numpy as np
import cffi

ffi = cffi.FFI()

@exposed
class OpenNISurface(Control):

    depth_image = Image()
    depth_texture = ImageTexture()

    is_frame_new = False

    def _ready(self):
        openni2.initialize()
        dev = openni2.Device.open_any()
        print(dev.get_device_info())
        print(dev.get_sensor_info(openni2.SENSOR_DEPTH).videoModes)
        depth_stream = dev.create_depth_stream()
        depth_stream.configure_mode(640, 480, 30, openni2.PIXEL_FORMAT_DEPTH_1_MM)
        depth_stream.register_new_frame_listener(self.frame_new)
        depth_stream.start()

        self.depth_texture.create(640, 480, Image.FORMAT_L8, Texture.FLAG_VIDEO_SURFACE)

        pass

    def _process(self, delta):
        if self.is_frame_new == True:
            # Upload Texture
            self.depth_texture.set_data(self.depth_image)
            self.is_frame_new = False
        pass

    def _draw(self):
        self.draw_texture(self.depth_texture, Vector2(0, 0), Color(1, 1, 1, 1), Texture())
        pass

    def frame_new(self, frame):

        # Read Frame
        f = frame.read_frame()

        # Depth to Image
        depth = np.frombuffer(f.get_buffer_as_uint16(), dtype=np.uint16)
        pix = np.multiply(depth.astype(np.float32), 255.0 / 9870.0).astype(np.uint8)

        # Copy Data
        array = PoolByteArray()
        array.resize(f.width * f.height)

        with array.raw_access() as ptr:
            np.frombuffer(ffi.buffer(ptr, f.width * f.height), dtype=np.uint8)[:] = pix[:]

        self.depth_image.lock()
        self.depth_image.create_from_data(f.width, f.height, False, Image.FORMAT_L8, array)
        self.depth_image.unlock()
        self.is_frame_new = True

        pass

    def __eq__(self, other):
        return (self == other)

    def __hash__(self):
        return id(self)

import ctypes
import threading
import time

import hid
from PIL import Image
from event_emitter import events

KEYS = {
    (1, 0): 0,
    (2, 0): 1,
    (4, 0): 2,
    (8, 0): 3,
    (16, 0): 4,

    (32, 0): 5,
    (64, 0): 6,
    (128, 0): 7,
    (0, 1): 8,
    (0, 2): 9,

    (0, 4): 10,
    (0, 8): 11,
    (0, 16): 12,
    (0, 32): 13,
    (0, 64): 14,
}

NUM_KEYS = 15
PAGE_PACKET_SIZE = 8017
ICON_SIZE = 72
NUM_TOTAL_PIXELS = 72 * 72

PAGE_1_HEADER = bytearray(
    [0x02, 0x00, 0x00, 0x00, 0x00, 0x40, 0x1f, 0x00, 0x00, 0x55, 0xaa, 0xaa, 0x55, 0x11, 0x22, 0x33,
     0x44, 0x42, 0x4d, 0xf6, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28,
     0x00, 0x00, 0x00, 0x48, 0x00, 0x00, 0x00, 0x48, 0x00, 0x00, 0x00, 0x01, 0x00, 0x18, 0x00, 0x00,
     0x00, 0x00, 0x00, 0xc0, 0x3c, 0x00, 0x00, 0x13, 0x0b, 0x00, 0x00, 0x13, 0x0b, 0x00, 0x00, 0x00,
     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
PAGE_2_HEADER = bytearray(
    [0x02, 0x40, 0x1f, 0x00, 0x00, 0xb6, 0x1d, 0x00, 0x00, 0x55, 0xaa, 0xaa, 0x55, 0x11, 0x22, 0x33, 0x44])


class InvalidValueException(Exception):
    pass


class Infinitton(threading.Thread, events.EventEmitter):

    @staticmethod
    def check_rgb_value(value: int) -> None:
        if value < 0 or 255 < value:
            raise InvalidValueException

    @staticmethod
    def check_valid_key_index(key_index: int) -> None:
        if key_index < 0 or 14 < key_index:
            raise InvalidValueException

    @staticmethod
    def _pad_to_length(buffer, pad_length):
        return buffer + bytearray([0] * (pad_length - len(buffer)))

    @classmethod
    def is_present(cls, vid=0xffff, pid=0x1f40) -> bool:
        for device in hid.enumerate(vid=vid, pid=pid):
            return True
        return False

    def __init__(self, vid=0xffff, pid=0x1f40):
        threading.Thread.__init__(self, daemon=True)
        events.EventEmitter.__init__(self)
        self._vid = vid
        self._pid = pid
        self._device = None
        self._listening = False
        self._key_states = [False] * 15

        self.connect()

    def connect(self) -> bool:
        try:
            self._device = hid.Device(vid=self._vid, pid=self._pid)
            print('connected')
            self._listening = True
            self._start_listening()

            return True
        except hid.HIDException as hide:
            print(hide)
            return False

    def disconnect(self) -> None:
        if self._device is not None:
            self._listening = False
            self._device.close()
            print('disconnected')
            self._device = None

    def _start_listening(self) -> None:
        self.start()

    def run(self) -> None:
        if self._device is not None:
            while self._listening:
                r = self._device.read(3)
                for key_signature, key_index in KEYS.items():
                    if key_signature[1] == 0 and r[2] == 0:
                        # first 8
                        self._press(key_index, key_signature[0] & r[1])

                    elif key_signature[0] == 0 and r[1] == 0:
                        # last 7
                        self._press(key_index, key_signature[1] & r[2])

    def _press(self, key_index: int, key_pressed: bool):
        if self._key_states[key_index] != key_pressed:
            self._key_states[key_index] = key_pressed
            if key_pressed:
                self.emit('down', key_index)
            else:
                self.emit('up', key_index)

    def fill_color(self, key_index: int, r: int, g: int, b: int) -> None:
        Infinitton.check_valid_key_index(key_index)

        Infinitton.check_rgb_value(r)
        Infinitton.check_rgb_value(g)
        Infinitton.check_rgb_value(b)

        # self._device.
        pixel = bytearray([b, g, r])
        self._send_image(key_index, pixel * NUM_TOTAL_PIXELS)

    def fill_image_path(self, key_index, image_path) -> None:
        self.fill_image(key_index, Image.open(image_path))

    def fill_image(self, key_index, image: Image) -> None:
        Infinitton.check_valid_key_index(key_index)

        if image.width != ICON_SIZE or image.height != ICON_SIZE:
            image = image.resize((ICON_SIZE, ICON_SIZE))

        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        data = bytearray()
        for r in range(ICON_SIZE):
            row_data = bytearray(ICON_SIZE * 3)

            for c in range(ICON_SIZE):
                pixel = image.getpixel((r, c))
                pixel_data_start = 3 * c

                row_data[pixel_data_start] = pixel[0]
                row_data[pixel_data_start + 1] = pixel[1]
                row_data[pixel_data_start + 2] = pixel[2]

            row_data.reverse()
            data += row_data
        self._send_image(key_index, data)

    def _send_image(self, key_index: int, data: bytearray):
        self._send_data_page(PAGE_1_HEADER, data[:7946])
        self._send_data_page(PAGE_2_HEADER, data[7946:])
        self._device.send_feature_report(Infinitton._to_c_char_p(
            bytearray([0x00, 0x12, 0x01, 0x00, 0x00, key_index + 1, 0x00, 0x00,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0x00, 0xf6, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])))
        # delay is required, faster update corrupts shown images
        time.sleep(.001)

    def clear_key(self, key_index) -> None:
        self.fill_color(key_index, 0, 0, 0)

    def clear_all_keys(self) -> None:
        for key in range(NUM_KEYS):
            self.clear_key(key)

    def _send_data_page(self, header: bytearray, data: bytearray) -> None:
        actual_data = Infinitton._pad_to_length(header + data, PAGE_PACKET_SIZE)
        self._device.write(Infinitton._to_c_char_p(actual_data))

    @staticmethod
    def _to_c_char_p(data: bytearray):
        return (ctypes.c_char * (len(data))).from_buffer(data)


if __name__ == '__main__':
    INTERVAL = int(255 / 4)
    COLOR_VALUES = [0, INTERVAL, INTERVAL*2, INTERVAL*3, 255]

    def down(button):
        print('down: %s' % button)


    def up(button):
        print('up: %s' % button)


    Infinitton.is_present(0, 0)
    infinitton = Infinitton()

    infinitton.on('down', down)
    infinitton.on('up', up)

    infinitton.clear_all_keys()
    #time.sleep(.005)
    #infinitton.fill_color(0, 255, 0, 0)

    infinitton.fill_image_path(0, 'test/folder.png')

    #for key in range(NUM_KEYS):
    #    infinitton.fill_color(key, COLOR_VALUES[int(key / 5)], COLOR_VALUES[int(key % 5)], COLOR_VALUES[key % 5])
    #    time.sleep(.005)

    time.sleep(60)

    infinitton.disconnect()

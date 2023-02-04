import ctypes
import ctypes.wintypes
import logging
from contextlib import contextmanager
from ctypes import Array, c_char
from typing import Tuple, Generator, Callable

import numpy as np

logger = logging.getLogger(__name__)


def find_window_by_name(window_name: str) -> int:
    """
    Finds a window by its name.

    :param window_name: The name of the window to find.
    :return: Handle to the found window.
    """
    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
    if not hwnd:
        raise Exception("Failed to find window")
    return hwnd


def get_window_size(hwnd: int) -> Tuple[int, int]:
    """
    Gets the size of the window.

    :param hwnd: Handle to the window.
    :return: The width and height of the window.
    """
    rect = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    return width, height


def create_compatible_dc(hdc: int) -> int:
    """
    Creates a compatible device context.

    :param hdc: Handle to the device context.
    :return: Handle to the created device context.
    """
    return ctypes.windll.gdi32.CreateCompatibleDC(hdc)


def create_bitmap(hdc: int, width: int, height: int) -> int:
    """
    Creates a bitmap.

    :param hdc: Handle to the device context.
    :param width: Width of the bitmap.
    :param height: Height of the bitmap.
    :return: Handle to the created bitmap.
    """
    return ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, width, height)


def select_bitmap(compatible_dc: int, bitmap: int) -> None:
    """
    Select the specified bitmap into the specified device context.

    :param compatible_dc: A handle to the device context into which the bitmap is to be selected.
    :param bitmap: A handle to the bitmap to be selected.
    """
    ctypes.windll.gdi32.SelectObject(compatible_dc, bitmap)


def copy_dc(compatible_dc: int, hdc: int, width: int, height: int) -> None:
    """
    Perform a bit-block transfer of the color data corresponding to a rectangle
    of pixels from the specified source device context into a destination device context.

    :param compatible_dc: A handle to the destination device context.
    :param hdc: A handle to the source device context.
    :param width: The width, in pixels, of the source and destination rectangles.
    :param height: The height, in pixels, of the source and destination rectangles.
    """
    ctypes.windll.gdi32.BitBlt(compatible_dc, 0, 0, width, height, hdc, 0, 0, 0x00CC0020)


def get_bitmap_data(bitmap: int, width: int, height: int) -> Array[c_char]:
    """
    Retrieve the bits of the specified device-independent bitmap.

    :param bitmap: A handle to the device-independent bitmap.
    :param width: The width, in pixels, of the bitmap.
    :param height: The height, in pixels, of the bitmap.
    :return: The bits of the specified bitmap.
    """
    data = ctypes.create_string_buffer(width * height * 4)
    ctypes.windll.gdi32.GetBitmapBits(bitmap, width * height * 4, data)
    return data


def buffer_to_numpy_array(data: Array[c_char], width: int, height: int) -> np.ndarray:
    """
    Convert a string buffer to a numpy array.

    :param data: The string buffer to be converted.
    :param width: The width, in pixels, of the image represented by the string buffer.
    :param height: The height, in pixels, of the image represented by the string buffer.
    :return: The numpy array representation of the string buffer.
    """
    dc_memory = np.frombuffer(data, np.uint8)
    dc_memory = dc_memory.reshape((height, width, 4))
    return dc_memory


def cleanup(compatible_dc: int, bitmap: int, hwnd: int, hdc: int) -> None:
    """
    Cleanup function to delete compatible device context, bitmap, window handle, and device context.

    :param compatible_dc: Handle to the compatible device context to be deleted. Defaults to None.
    :param bitmap: Handle to the bitmap to be deleted. Defaults to None.
    :param hwnd: Handle to the window to be deleted. Defaults to None.
    :param hdc: Handle to the device context to be released. Defaults to None.
    """

    ctypes.windll.gdi32.DeleteDC(compatible_dc)
    ctypes.windll.gdi32.DeleteObject(bitmap)
    ctypes.windll.user32.ReleaseDC(hwnd, hdc)


@contextmanager
def window_context(window_name: str) -> Callable[[float], Generator[np.ndarray, None, None]]:
    """
    Context manager to capture the buffer of a window as a generator of numpy arrays.

    :param window_name: Name of the window to capture the buffer of.
    :return Generator[np.ndarray, None, None]: Generator that yields the buffer of the window as numpy arrays.
    """
    compatible_dc = 0
    bitmap = 0
    hwnd = 0
    hdc = 0

    try:
        hwnd = find_window_by_name(window_name)
        hdc = ctypes.windll.user32.GetDC(hwnd)
        compatible_dc = create_compatible_dc(hdc)
        width, height = get_window_size(hwnd)
        bitmap = create_bitmap(hdc, width, height)
        select_bitmap(compatible_dc, bitmap)

        def frame_buffer():
            """
            Generator function to yield the buffer of the window as numpy arrays.
            """
            while True:
                copy_dc(compatible_dc, hdc, width, height)
                data = get_bitmap_data(bitmap, width, height)
                dc_memory = buffer_to_numpy_array(data, width, height)
                yield dc_memory

        yield frame_buffer
    finally:
        cleanup(compatible_dc, bitmap, hwnd, hdc)

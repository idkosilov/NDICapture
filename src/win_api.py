import ctypes
import ctypes.wintypes
import logging
from contextlib import contextmanager
from ctypes import Array, c_char
from typing import Tuple, Generator, Callable

import numpy as np

logger = logging.getLogger(__name__)


class FailedToFindWindow(Exception):
    ...


class FailedToGetWindowSize(Exception):
    ...


class FailedToGetDeviceContext(Exception):
    ...


class FailedCreateCompatibleDC(Exception):
    ...


class FailedCreateBitmap(Exception):
    ...


class FailedSelectBitmap(Exception):
    ...


class FailedCopyDC(Exception):
    ...


class FailedGetBitmapData(Exception):
    ...


def find_window_by_name(window_name: str) -> int:
    """
    Finds a window by its name.

    :param window_name: the name of the window to find.
    :return: handle to the found window.
    """
    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
    if not hwnd:
        raise FailedToFindWindow(f"Failed to find a window by name = {window_name!r}")
    logger.info(f"Window with name = {window_name!r} found, hwnd = {hwnd}.")
    return hwnd


def get_window_size(hwnd: int) -> Tuple[int, int]:
    """
    Gets the size of the window.

    :param hwnd: handle to the window.
    :return: the width and height of the window.
    """
    rect = ctypes.wintypes.RECT()
    result = ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect))

    if result != 0:
        raise FailedToGetWindowSize("Failed to get window size.")

    width = rect.right - rect.left
    height = rect.bottom - rect.top

    logger.info(f"Window width = {width!r}, height = {height!r}.")

    return width, height


def get_device_context(hwnd: int) -> int:
    """
    Retrieve the device context of the specified window handle.

    :param hwnd: the handle of the device context.
    :return: the handle of the device context.
    """
    hdc = ctypes.windll.user32.GetDC(hwnd)

    if hdc == 0:
        raise FailedToGetDeviceContext("Could not retrieve device context.")

    logger.info(f"Device context was retrieved {hdc!r}.")

    return hdc


def create_compatible_dc(hdc: int) -> int:
    """
    Creates a compatible device context.

    :param hdc: handle to the device context.
    :return: handle to the created device context.
    """
    compatible_dc = ctypes.windll.gdi32.CreateCompatibleDC(hdc)

    if compatible_dc == 0:
        raise FailedCreateCompatibleDC("Failed to create a compatible device context.")

    logger.info(f"Compatible device context was created {compatible_dc}.")

    return compatible_dc


def create_bitmap(hdc: int, width: int, height: int) -> int:
    """
    Creates a bitmap.

    :param hdc: handle to the device context.
    :param width: width of the bitmap.
    :param height: height of the bitmap.
    :return: handle to the created bitmap.
    """
    bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, width, height)

    if bitmap == 0:
        raise FailedCreateBitmap("Failed to create a bitmap.")

    logger.info(f"Bitmap was created {bitmap}.")

    return bitmap


def select_bitmap(compatible_dc: int, bitmap: int) -> None:
    """
    Select the specified bitmap into the specified device context.

    :param compatible_dc: a handle to the device context into which the bitmap is to be selected.
    :param bitmap: a handle to the bitmap to be selected.
    """
    result = ctypes.windll.gdi32.SelectObject(compatible_dc, bitmap)
    if result == 0:
        raise FailedSelectBitmap("Failed to select the specified bitmap into specified device context.")

    logger.info(f"Bitmap was selected into the specified device context.")


def copy_dc(compatible_dc: int, hdc: int, width: int, height: int) -> None:
    """
    Perform a bit-block transfer of the color data corresponding to a rectangle
    of pixels from the specified source device context into a destination device context.

    :param compatible_dc: a handle to the destination device context.
    :param hdc: a handle to the source device context.
    :param width: the width, in pixels, of the source and destination rectangles.
    :param height: the height, in pixels, of the source and destination rectangles.
    """
    result = ctypes.windll.gdi32.BitBlt(compatible_dc, 0, 0, width, height, hdc, 0, 0, 0x00CC0020)
    if result == 0:
        raise FailedCopyDC("Failed to perform a bit-block transfer of the color data corresponding to a rectangle of "
                           "pixels from the specified source device context into a destination device context.")

    logger.info(f"Bitmap was copied to destination device context.")


def get_bitmap_data(bitmap: int, width: int, height: int) -> Array[c_char]:
    """
    Retrieve the bits of the specified device-independent bitmap.

    :param bitmap: a handle to the device-independent bitmap.
    :param width: the width, in pixels, of the bitmap.
    :param height: the height, in pixels, of the bitmap.
    :return: the bits of the specified bitmap.
    """
    data = ctypes.create_string_buffer(width * height * 4)
    result = ctypes.windll.gdi32.GetBitmapBits(bitmap, width * height * 4, data)
    if result == 0:
        raise FailedGetBitmapData("Failed to retrieve the bits of the specified device-independent bitmap")

    logger.info(f"Bitmap was copied to data buffer.")

    return data


def buffer_to_numpy_array(data: Array[c_char], width: int, height: int) -> np.ndarray:
    """
    Convert a string buffer to a numpy array.

    :param data: the string buffer to be converted.
    :param width: the width, in pixels, of the image represented by the string buffer.
    :param height: the height, in pixels, of the image represented by the string buffer.
    :return: the numpy array representation of the string buffer.
    """
    dc_memory = np.frombuffer(data, np.uint8)
    dc_memory = dc_memory.reshape((height, width, 4))
    return dc_memory


def cleanup(compatible_dc: int, bitmap: int, hwnd: int, hdc: int) -> None:
    """
    Cleanup function to delete compatible device context, bitmap, window handle, and device context.

    :param compatible_dc: handle to the compatible device context to be deleted.
    :param bitmap: handle to the bitmap to be deleted.
    :param hwnd: handle to the window to be deleted.
    :param hdc: handle to the device context to be released.
    """

    if ctypes.windll.gdi32.DeleteDC(compatible_dc) != 0:
        logger.info("Compatible device context was deleted")
    if ctypes.windll.gdi32.DeleteObject(bitmap) != 0:
        logger.info("Bitmap was deleted")
    if ctypes.windll.user32.ReleaseDC(hwnd, hdc) != 0:
        logger.info("Device context was released")


@contextmanager
def window_context(window_name: str) -> Callable[[float], Generator[np.ndarray, None, None]]:
    """
    Context manager to capture the buffer of a window as a generator of numpy arrays.

    :param window_name: name of the window to capture the buffer of.
    :return Generator[np.ndarray, None, None]: generator that yields the buffer of the window as numpy arrays.
    """
    hwnd = find_window_by_name(window_name)
    hdc = get_device_context(hwnd)
    compatible_dc = create_compatible_dc(hdc)
    width, height = get_window_size(hwnd)
    bitmap = create_bitmap(hdc, width, height)
    select_bitmap(compatible_dc, bitmap)

    def frame_buffer():
        """
        Generator function to yield the buffer of the window as numpy arrays.
        """
        try:
            while True:
                copy_dc(compatible_dc, hdc, width, height)
                data = get_bitmap_data(bitmap, width, height)
                dc_memory = buffer_to_numpy_array(data, width, height)
                yield dc_memory
        except (FailedCopyDC, FailedGetBitmapData):
            cleanup(compatible_dc, bitmap, hwnd, hdc)
            raise
        finally:
            yield None

    yield frame_buffer


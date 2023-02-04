from contextlib import contextmanager
from typing import Generator

import NDIlib


@contextmanager
def context(ndi_output_name: str) -> Generator:
    """
    A context manager that sets up an NDI sender and yields a coroutine for sending video frames.

    :param ndi_output_name: The name of the NDI output.
    :return: a coroutine that can be used to send video frames to NDI.
    """
    ndi_send = None

    try:
        if not NDIlib.initialize():
            raise Exception("Can't initialize NDI context.")

        send_settings = NDIlib.SendCreate()
        send_settings.ndi_name = ndi_output_name

        ndi_send = NDIlib.send_create(send_settings)

        video_frame = NDIlib.VideoFrameV2(FourCC=NDIlib.FOURCC_VIDEO_TYPE_BGRA)

        def ndi_output() -> Generator:
            """
            A coroutine for sending video frames to NDI.
            """
            while True:
                video_frame.data = yield
                NDIlib.send_send_video_v2(ndi_send, video_frame)

        ndi_output_coroutine = ndi_output()
        ndi_output_coroutine.send(None)
        yield ndi_output_coroutine

    finally:
        if ndi_send is not None:
            NDIlib.send_destroy(ndi_send)
        NDIlib.destroy()

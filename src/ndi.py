from contextlib import contextmanager
from typing import Generator

import NDIlib as ndi_lib


class FailedInitializeNDI(Exception):
    ...


@contextmanager
def context(ndi_output_name: str) -> Generator:
    """
    A context manager that sets up an NDI sender and yields a coroutine for sending video frames.

    :param ndi_output_name: The name of the NDI output.
    :return: a coroutine that can be used to/ send video frames to NDI.
    """
    ndi_send = None

    try:
        if not ndi_lib.initialize():
            raise FailedInitializeNDI("Can't initialize NDI context.")

        send_settings = ndi_lib.SendCreate()
        send_settings.ndi_name = ndi_output_name

        ndi_send = ndi_lib.send_create(send_settings)

        video_frame = ndi_lib.VideoFrameV2(FourCC=ndi_lib.FOURCC_VIDEO_TYPE_BGRA)

        def ndi_output() -> Generator:
            """
            A coroutine for sending video frames to NDI.
            """
            while True:
                video_frame.data = yield
                ndi_lib.send_send_video_v2(ndi_send, video_frame)

        ndi_output_coroutine = ndi_output()
        ndi_output_coroutine.send(None)
        yield ndi_output_coroutine

    finally:
        if ndi_send is not None:
            ndi_lib.send_destroy(ndi_send)
        ndi_lib.destroy()

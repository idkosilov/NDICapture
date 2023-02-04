import argparse
from typing import Tuple

import NDIlib as ndi

import win_api


def handle_command_line() -> Tuple[str, str]:
    """
    Handle the command line arguments and parse them into a tuple of window name and NDI output name.

    :return: Tuple of window name and NDI output name.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--window", type=str, default="Graphics Window",
                        help="the name of the window for capturing graphics")
    parser.add_argument("-n", "--ndi_output", type=str, default="SG Graphics NDI",
                        help="the name of the NDI output")
    args = parser.parse_args()

    return args.window, args.ndi_output


def capture_frames_and_send_to_ndi(window_name: str, ndi_output_name) -> None:
    """
    Capture the frames from the specified window and send it to NDI.

    :param window_name: the name of the window to be captured
    :param ndi_output_name: the name of the NDI output
    """
    ndi.initialize()
    send_settings = ndi.SendCreate()
    send_settings.ndi_name = ndi_output_name

    ndi_send = ndi.send_create(send_settings)

    video_frame = ndi.VideoFrameV2(FourCC=ndi.FOURCC_VIDEO_TYPE_BGRA)

    try:
        with win_api.window_context(window_name) as frame_buffer:
            for frame in frame_buffer():
                video_frame.data = frame
                ndi.send_send_video_v2(ndi_send, video_frame)
    finally:
        ndi.send_destroy(ndi_send)
        ndi.destroy()


def main() -> None:
    window_name, ndi_output_name = handle_command_line()
    capture_frames_and_send_to_ndi(window_name, ndi_output_name)


if __name__ == "__main__":
    main()

import argparse
import logging.config
from time import sleep
from typing import Tuple

import win_api
import ndi
import logging_config

logger = logging.getLogger()


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
    with win_api.window_context(window_name) as frame_buffer:
        with ndi.context(ndi_output_name) as ndi_output:
            for frame in frame_buffer():
                if frame is not None:
                    ndi_output.send(frame)


def main() -> None:
    window_name, ndi_output_name = handle_command_line()

    while True:
        try:
            capture_frames_and_send_to_ndi(window_name, ndi_output_name)
        except Exception as err:
            logger.error(f"Error occurred: {err}")
            logger.info("Trying to recreate context in 5 seconds...")
            sleep(5)


if __name__ == "__main__":
    main()

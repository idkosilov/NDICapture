Window Capture to NDI
=====================

Window Capture to NDI is a simple software that allows you to capture and stream a specific window or desktop to an NDI (Network Device Interface) source.

Features
--------

*   Capture and stream a specific window or desktop.
*   Easy to use command-line interface.
*   Compatible with NDI-enabled software and hardware.
*   Supports capture of windows with alpha channel.

Requirements
------------

*   Windows 7 or higher.
*   NDI runtime libraries.

Installation
------------

1.  Download the latest release from the [releases page](https://github.com/idkosilov/window_capture_to_ndi/releases).
2.  Install the NDI runtime libraries if you haven't already. You can download them from the [NewTek website](https://www.newtek.com/ndi/tools/#download-section).
3.  Run the `WindowCaptureToNDI.exe` file.

Usage
-----

1.  Select the window or desktop you want to capture and stream.
2.  Open terminal and run the app:

        WindowCaptureToNDI.exe --window "Graphics Window" --ndi_output "Graphics NDI"

3.  For help, run:

        WindowCaptureToNDI.exe -h

Support
-------

For any questions or issues, please open a new issue on the [issues page](https://github.com/idkosilov/window_capture_to_ndi/issues) or send an email to [idkosilov@gmail.com](mailto:idkosilov@gmail.com).

License
---------

This software is released under the MIT license. See the LICENSE file for more information.

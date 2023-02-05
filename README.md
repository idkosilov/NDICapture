NDI Capture
=====================

NDI Capture is a simple software that allows you to capture and stream a specific window or desktop to an NDI (Network Device Interface) source.

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

1.  Download the latest release from the [releases page](https://github.com/idkosilov/NDICapture/releases).
2.  Install the NDI runtime libraries if you haven't already. You can download them from the [NewTek website](https://www.newtek.com/ndi/tools/#download-section).
3.  Run the `NDICapture.exe` file.

Usage
-----

1.  Select the window or desktop you want to capture and stream.
2.  Open terminal and run the app:

        NDICapture.exe --window "Graphics Window" --ndi_output "Graphics NDI"

3.  For help, run:

        NDICapture.exe.exe -h

Support
-------

For any questions or issues, please open a new issue on the [issues page](https://github.com/idkosilov/NDICapture/issues) or send an email to [idkosilov@gmail.com](mailto:idkosilov@gmail.com).

License
---------

This software is released under the MIT license. See the [LICENSE](https://github.com/idkosilov/NDICapture/blob/master/LICENSE.md) file for more information.

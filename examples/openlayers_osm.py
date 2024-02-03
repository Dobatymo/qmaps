import logging
import os
import sys
from argparse import ArgumentParser
from functools import partial

from PySide2.QtWidgets import QApplication

from qmaps.openlayers import QOpenLayersOSM


def main():
    JS_LOG_FORMAT = "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s [%(sourceID)s:%(lineNumber)s]"
    handler = logging.StreamHandler()
    formatter = logging.Formatter(JS_LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger("javascript").addHandler(handler)

    app = QApplication(sys.argv)

    window = QOpenLayersOSM(25, 121)

    for name, signal in vars(window).items():
        if name in ("map_dblclick", "map_singleclick", "map_movestart", "map_moveend"):
            signal.connect(partial(print, name))

    window.wait_until_ready()
    window.show()

    window.add_overlay_text(10, 10, "test text")
    window.add_layer_point(20, 20)

    print(window.get_center())
    print(window.get_zoom())

    return app.exec_()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--qt-remote-debugging-port",  # don't use `--remote-debugging-port` since this clashes with Qt
        type=int,
        help="The developer tools are accessed as a local web page using a Chromium or Qt WebEngine based browser, such as the Chrome browser.",
    )
    parser.add_argument("--disable-web-security", action="store_true")
    args = parser.parse_args()

    if args.qt_remote_debugging_port:
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(args.qt_remote_debugging_port)

    sys.exit(main())

import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


BASE_DIR = Path(__file__).resolve().parent
QML_DIR = BASE_DIR / "qml"


def main():
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(QML_DIR / "main.qml")

    if not engine.rootObjects():
        del engine
        sys.exit(-1)

    return_code = app.exec()

    del engine
    sys.exit(return_code)


if __name__ == "__main__":
    main()

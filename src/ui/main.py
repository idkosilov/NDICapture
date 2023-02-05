import logging
import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from ui.models.ndi_outputs_model import NdiOutputsModel
from ui.models.windows_model import WindowsModel


BASE_DIR = Path(__file__).resolve().parent
QML_DIR = BASE_DIR / "qml"


def main():
    app = QApplication(sys.argv)
    
    windows_model = WindowsModel()
    ndi_outputs_model = NdiOutputsModel()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("windowsModel", windows_model)
    engine.rootContext().setContextProperty("ndiOutputsModel", ndi_outputs_model)
    engine.load(QML_DIR / "main.qml")

    if not engine.rootObjects():
        del engine
        sys.exit(-1)

    return_code = app.exec()

    del engine
    sys.exit(return_code)


if __name__ == "__main__":
    main()

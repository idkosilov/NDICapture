import subprocess
import sys
from typing import Union, Any

from PySide6.QtCore import QAbstractListModel, QObject, QPersistentModelIndex, QModelIndex, Qt, QByteArray, Slot, Signal


class NdiOutput:

    def __init__(self, window_name: str, name: str) -> None:
        self.window = window_name
        self.name = name

        self._worker = None
        self._logs_parser = None
        self.is_running = False

    def start(self) -> None:
        self.is_running = True

        self._worker = subprocess.Popen([sys.executable, "../core/main.py", "-w", self.window, "-n", self.name],
                                        stderr=subprocess.PIPE)
        self._worker.daemon = True

    def stop(self) -> None:
        self.is_running = False
        self._worker.terminate()
        self._worker = None


class NdiOutputsModel(QAbstractListModel):
    windowName = Qt.UserRole + 1
    ndiOutputName = Qt.UserRole + 2
    isRunning = Qt.UserRole + 3

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.ndi_outputs = []

    @Slot(str, str)
    def add(self, window_name: str, ndi_output_name: str) -> None:
        if window_name != '' and ndi_output_name != '':
            ndi_output = NdiOutput(window_name, ndi_output_name)
            self.ndi_outputs.append(ndi_output)
            self.layoutChanged.emit()

    @Slot(int)
    def remove(self, row: int) -> None:
        if self.ndi_outputs[row].is_running:
            self.ndi_outputs[row].stop()
        del self.ndi_outputs[row]
        self.layoutChanged.emit()

    @Slot(int)
    def startStop(self, row: int) -> None:
        ndi_output = self.ndi_outputs[row]

        if ndi_output.is_running:
            ndi_output.stop()
        else:
            ndi_output.start()

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()) -> int:
        return len(self.ndi_outputs)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = windowName) -> Any:
        if index.isValid():
            ndi_output = self.ndi_outputs[index.row()]
            if role == NdiOutputsModel.windowName:
                return ndi_output.window
            elif role == NdiOutputsModel.ndiOutputName:
                return ndi_output.name
            elif role == NdiOutputsModel.isRunning:
                return ndi_output.is_running

    def roleNames(self):
        default = super().roleNames()
        default[NdiOutputsModel.windowName] = QByteArray(b'windowName')
        default[NdiOutputsModel.ndiOutputName] = QByteArray(b'ndiOutputName')
        default[NdiOutputsModel.isRunning] = QByteArray(b'isRunning')
        return default

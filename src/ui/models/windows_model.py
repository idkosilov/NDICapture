from typing import Union, Any

from PySide6.QtCore import QAbstractListModel, QObject, QPersistentModelIndex, QModelIndex, Qt, QTimer, QByteArray

from core import win_api


class WindowsModel(QAbstractListModel):
    windowName = Qt.UserRole + 1

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.windows = []

        self._windows_observer = QTimer()
        self._windows_observer.setInterval(1000)
        self._windows_observer.timeout.connect(self._update_windows_titles)
        self._windows_observer.start()

    def _update_windows_titles(self) -> None:
        windows = win_api.get_windows_titles()
        if set(windows) != set(self.windows):
            self.windows = win_api.get_windows_titles()
            self.layoutChanged.emit()

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()) -> int:
        return len(self.windows)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = windowName) -> Any:
        if index.isValid():
            return self.windows[index.row()]

    def roleNames(self):
        default = super().roleNames()
        default[WindowsModel.windowName] = QByteArray(b'windowName')
        return default



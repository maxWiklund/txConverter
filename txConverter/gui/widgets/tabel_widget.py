# -*- coding: utf-8 -*-
# Copyright (C) 2020  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# IMPORT STANDARD LIBRARIES
import sys

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtWidgets, QtGui

# IMPORT LOCAL LIBRARIES
from txConverter.elements import image_element
from txConverter.gui import model
from txConverter.gui.widgets import delegates


COLUMN_RESIZED = [model.NAME_COLUMN_INDEX, model.OUTPUT_NAME_COLUMN_INDEX]
"""list[int]: Columns to automatically resize."""


class TableView(QtWidgets.QTableView):
    """Custom QTableView with delete signal.

    Attributes:
        delete_signal (<QtCore.Signal>): Delete event.

    """

    delete_signal = QtCore.Signal(object)

    def __init__(self, parent=None, *args, **kwargs) -> None:
        """Initialize class and setup custom context menu.

        Args:
            parent (:obj: `<QtWidgets.QWidget>`, optional): Parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super(TableView, self).__init__(parent, *args, **kwargs)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

    def open_menu(self, position: QtCore.QPoint) -> None:
        """Create custom context menu.

        Args:
            position: Mouse position.

        """
        menu = QtWidgets.QMenu()
        remove = menu.addAction("Remove selected")
        action = menu.exec_(self.mapToGlobal(position))
        if action == remove:
            self._delete_event()  # Delete selected rows.

    def _get_selected_items(self) -> [QtCore.QModelIndex]:
        """Get selected model indexes.

        Returns:
            Selected model indexes.

        """
        return [QtCore.QPersistentModelIndex(model_index) for model_index in self.selectionModel().selectedRows()]

    def _delete_event(self) -> None:
        """Emit signal for rows to be deleted."""
        self.delete_signal.emit(self._get_selected_items())  # Selected rows to be deleted.

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """ Handel key press events.

        Args:
            event: Key event.

        """
        key = event.key()
        if key == QtCore.Qt.Key_Delete or key == QtCore.Qt.Key_Backspace:
            self._delete_event()
        else:
            super(TableView, self).keyPressEvent(event)


class TxTableWidget(QtWidgets.QWidget):
    """Custom widget with table view."""

    def __init__(self, parent=None) -> None:
        """Initialize class and do nothing.

        Args:
            parent (:obj: `<QtCore.QObject>`, optional): Parent widget.

        """
        super(TxTableWidget, self).__init__(parent)
        self._initialise()
        self._connect()
        self.setAcceptDrops(False)

    def _initialise(self) -> None:
        """Build gui."""
        self.model = model.TxTableModel()
        self.table = TableView()

        self.filter_model = QtCore.QSortFilterProxyModel()
        self.filter_model.setSourceModel(self.model)
 
        self.table.setModel(self.filter_model)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setItemDelegateForColumn(model.OUTPUT_NAME_COLUMN_INDEX, delegates.LineEditDelegate(self))

        for column in COLUMN_RESIZED:
            self.table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        for column, settings in model.COLUMN_HEADER.items():
            self.table.setColumnWidth(column, settings["width"])

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def _connect(self) -> None:
        """Connect signals."""
        self.table.delete_signal.connect(self._remove_items)

    @QtCore.Slot()
    def _remove_items(self, items: [QtCore.QPersistentModelIndex]) -> None:
        """Remove items from table view and model.

        Args:
            items: Items to remove.

        """
        for index in items:
            element = self.model.get_element(index)
            self.model.remove_element(element)


def __test() -> None:
    import PyImageSequence

    app = QtWidgets.QApplication(sys.argv)
    window = TxTableWidget()
    for x in range(10):
        window.model.add_element(
            image_element.ReleasableImageElement(PyImageSequence.ImageElement("/mock/path/file.1001.exr"))
        )
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    __test()

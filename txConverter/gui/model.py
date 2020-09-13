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
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtWidgets, QtGui

# IMPORT LOCAL LIBRARIES
from txConverter.elements import image_element
from txConverter.log import LOG


ENABLED_COLUMN_INDEX = 0
NAME_COLUMN_INDEX = 1
OUTPUT_NAME_COLUMN_INDEX = 2
GAMMA_COLUMN_INDEX = 3

COLUMN_HEADER = {
    ENABLED_COLUMN_INDEX: {"name": "Convert", "width": 150},
    NAME_COLUMN_INDEX: {"name": "File name", "width": 200},
    OUTPUT_NAME_COLUMN_INDEX: {"name": "Output Name", "width": 100},
    GAMMA_COLUMN_INDEX: {"name": "Gamma", "width": 200},
}


class TxTableModel(QtCore.QAbstractTableModel):
    """Model for custom table view."""

    def __init__(self, parent=None) -> None:
        """Initialize model.

        Args:
            parent (:obj: `<QtCore.QObject>`, optional): Parent widget.

        """
        super(TxTableModel, self).__init__(parent)
        self.elements = []
        self.header = COLUMN_HEADER

    def get_element(self, index: QtCore.QModelIndex) -> image_element.ReleasableImageElement:
        """Get element from index.

        Args:
            index: Model index.

        Returns:
            Row element.

        """
        return self.elements[index.row()]

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        """Get number of columns.

        Args:
            parent: Parent index.

        Returns:
            Number of columns.

        """
        return len(self.header)

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        """Get number of rows.

        Args:
            parent (:obj: `<QtCore.QModelIndex>`, optional): Parent index.

        Returns:
            Number of rows.

        """
        return len(self.elements)

    def _get_item_data(self, index: QtCore.QModelIndex) -> str:
        """Get data from column, row.

        Args:
            index: Model index to query.

        Returns:
            Data to render as text.

        """
        column = index.column()
        element = self.get_element(index)
        if column == NAME_COLUMN_INDEX:
            return element.name
        elif column == OUTPUT_NAME_COLUMN_INDEX:
            return element.output
        return ""

    def _get_item_tooltip(self, index: QtCore.QModelIndex) -> str:
        """Query element for specific tooltip data.

        Args:
            index: Model index to query.

        Returns:
            Element specific tooltip.

        """
        element = self.get_element(index)
        return element.tool_tip

    def _is_checked(self, value: bool) -> QtCore.Qt.Checked:
        """Convert bool value into check state.

        Args:
            value: Value to evaluate.

        Returns:
            Converted check state.

        """
        return QtCore.Qt.Checked if value else QtCore.Qt.Unchecked

    def _get_item_checked(self, index: QtCore.QModelIndex) -> QtCore.Qt.Checked:
        """Query if model index is checked.

        Args:
            index: Model index to query.

        Returns:
            Element check state.

        """
        element = self.get_element(index)
        column = index.column()
        if column == ENABLED_COLUMN_INDEX:
            return self._is_checked(element.enabled)
        elif column == GAMMA_COLUMN_INDEX:
            return self._is_checked(element.gamma)

    def add_element(self, element: image_element.ReleasableImageElement) -> None:
        """Add element to model.

        Args:
            element: New element to add.

        """
        last_row = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), last_row, last_row)
        self.elements.append(element)
        self.endInsertRows()
        self.check_for_duplicated_data()

    def remove_element(self, element: image_element.ReleasableImageElement) -> None:
        """Remove element from model.

        Args:
            element: Element to remove.

        """
        index = self.elements.index(element)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.elements.pop(index)
        self.endRemoveRows()
        self.check_for_duplicated_data()

    def check_for_duplicated_data(self) -> None:
        """Check for duplicate elements."""
        existing_elements = {}
        for element in self.elements:
            if existing_elements.get(element.name):
                element.enabled = False
                element.duplicated = True
            else:
                existing_elements[element.name] = 1  # Placeholder.
                element.duplicated = False  # Reset duplicate.

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        """Returns the item flags for the given index.

        Args:
            index: Model index to query.

        Returns:
            Flags for given index.

        """
        flags = super(TxTableModel, self).flags(index)
        column = index.column()
        if column == ENABLED_COLUMN_INDEX:
            flags |= QtCore.Qt.ItemIsUserCheckable
        elif column == OUTPUT_NAME_COLUMN_INDEX:
            flags |= QtCore.Qt.ItemIsEditable
        elif column == GAMMA_COLUMN_INDEX:
            flags |= QtCore.Qt.ItemIsUserCheckable

        flags |= QtCore.Qt.ItemIsDragEnabled
        return flags

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        """Returns the data for the given role and section in the header with the specified orientation."""
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header[section]["name"]

    def _color_row(self, index: QtCore.QModelIndex) -> QtGui.QColor:
        """Set row color.
        
        Args:
            index: Model index to query.

        Returns:
            Row color.

        """
        element = self.get_element(index)
        if element.duplicated:
            return QtGui.QColor(190, 40, 0)

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """Request data from model.

        Args:
            index: Model index to query.
            role: Role enum (number).

        Returns:
            any: Data from model index.

        """

        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return self._get_item_data(index)  # Get data to render as text.

        elif role == QtCore.Qt.CheckStateRole:
            return self._get_item_checked(index)

        elif role == QtCore.Qt.ToolTipRole:  # Get tooltip data.
            return self._get_item_tooltip(index)
        elif role == QtCore.Qt.ForegroundRole:
            return self._color_row(index)

    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """Sets the role data for the item at index to value.

        Args:
            index: Model index to modify.
            value: New value to set.
            role: Role type.

        Returns:
            bool: Returns true if successful; otherwise returns false.

        """
        element = self.get_element(index)
        column = index.column()
        if element.duplicated:
            return False
        if column == ENABLED_COLUMN_INDEX:
            element.enabled = value
        elif column == OUTPUT_NAME_COLUMN_INDEX:
            element.output = value
        elif column == GAMMA_COLUMN_INDEX:
            element.gamma = value

        self.dataChanged.emit(index, index)

        return True

    def clear(self) -> None:
        """Clear model from data."""
        LOG.debug("Clear model.")
        self.beginResetModel()
        self.elements = []
        self.endResetModel()

    def __iter__(self):
        """Model data to iterate over."""
        return iter(self.elements)

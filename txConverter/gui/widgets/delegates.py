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

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtWidgets


class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    """QLineEdit delegate class."""

    def createEditor(
        self, parent: QtWidgets.QWidget, option: "QtWidgets.QStyleOptionViewItem", index: QtCore.QModelIndex
    ) -> QtWidgets.QLineEdit:
        """Renders the delegate using the given painter and style option for the item specified by index.

        Args:
            parent: Table view widget.
            option: Style option.
            index: Model index.

        Returns:
            Editor to use.

        """
        return QtWidgets.QLineEdit(parent)

    def setEditorData(self, editor: QtWidgets.QWidget, index: QtCore.QModelIndex) -> None:
        """Sets the data to be displayed and edited by the editor from the data model item specified by the model index.

        Args:
            editor: Editor widget.
            index: Model index.

        """
        editor.setText(index.data())

    def setModelData(
        self, editor: QtWidgets.QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex
    ) -> None:
        """Sets the data to be displayed and edited by the editor from the data model item specified by the model index.

        Args:
            editor: Editor widget.
            model: Model to set editor text to.
            index: Model index.

        """
        text = editor.text()
        model.setData(index, text, QtCore.Qt.DisplayRole)

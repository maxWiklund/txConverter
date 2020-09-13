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
import subprocess
import os

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtWidgets, QtGui

# IMPORT LOCAL LIBRARIES
from txConverter.gui.widgets import tabel_widget
from txConverter.log import LOG
from txConverter import load_elements
from txConverter.gui import style


class LoadElementThread(QtCore.QThread):
    """Thread class to scan directory for elements and add them to table view.

    Attributes:
        add_element (<QtCore.Signal>): Signal for adding new element to table view.
        message_event (<QtCore.Signal>): Signal for sending messages to user.

    """

    add_element = QtCore.Signal(object)
    message_event = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget, file_path: str) -> None:
        """Initialize class and do nothing.

        Args:
            parent: Parent widget.
            file_path: File path to scan.

        """
        super(LoadElementThread, self).__init__(parent)
        self.file_path = file_path

    def run(self) -> None:
        """Scan directory path for images."""
        self.message_event.emit("Start scanning directory:")
        for element in load_elements.get_elements(self.file_path):
            self.add_element.emit(element)

        self.message_event.emit("Scanning done:")


class ConvertThread(QtCore.QThread):
    """Thread class for converting images.

    Attributes:
        message_event (<QtCore.Signal>): Signal for sending messages to user.

    """

    message_event = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget, elements) -> None:
        """Initialize class and do nothing.

        Args:
            parent: Parent widget.
            elements: Elements to process.

        """
        super(ConvertThread, self).__init__(parent)
        self.elements = elements

    def run(self) -> None:
        """Convert images to tx."""
        status = True
        self.message_event.emit("Start converting images:")
        for element in self.elements:
            for command in element.get_command_list():
                try:
                    subprocess.run([command], shell=True, check=True)
                except subprocess.CalledProcessError:
                    LOG.warning('Failed to execute command: "{}"'.format(command))
                    status = False
        if status:
            self.message_event.emit("All images converted:")
        else:
            self.message_event.emit("Conversion of images failed.")


class GroupWidget(QtWidgets.QGroupBox):
    """Custom Group widget with layout."""

    def __init__(self, layout=None, *args, **kwargs) -> None:
        """Create QGroupBox with layout.

        Args:
            layout (:obj: `<QtWidgets.QLayout>`, optional): Custom layout.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super(GroupWidget, self).__init__(*args, **kwargs)
        self.main_layout = layout if layout else QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)


class DirectoryPathLineEdit(QtWidgets.QLineEdit):
    """Custom line edit to loading elements.

    Attributes:
        enter (<QtCore.Signal>): Signal for hitting enter key.

    """

    enter = QtCore.Signal()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """ Handel key press events.

        Args:
            event: Key event.

        """
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            self.enter.emit()
        else:
            super(DirectoryPathLineEdit, self).keyPressEvent(event)


class MaketxWidget(QtWidgets.QWidget):
    """Class for converting images to tx dialog."""

    def __init__(self, parent=None) -> None:
        """Initialize class and do nothing.

        Args:
            parent (:obj: `<QtCore.QWidget>`, optional): Parent widget.

        """
        super(MaketxWidget, self).__init__(parent)
        self._initialise()
        self.populate()
        self._connect()

        self.setAcceptDrops(True)
        self.resize(1200, 800)
        self.setStyleSheet(style.QT_STYLE)

    def _initialise(self) -> None:
        """Build gui."""
        self.scan_dir_pushbutton = QtWidgets.QPushButton("Scan Directory")
        self.directory_path_lineedit = DirectoryPathLineEdit()

        load_images_layout = QtWidgets.QHBoxLayout()
        load_images_layout.addWidget(self.scan_dir_pushbutton)
        load_images_layout.addWidget(self.directory_path_lineedit, 2)
        load_images_group = GroupWidget(load_images_layout)

        self.table_widget = tabel_widget.TxTableWidget()
        table_group = GroupWidget()
        table_group.main_layout.addWidget(self.table_widget)

        self.convert_button = QtWidgets.QPushButton("Convert Textures")
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.convert_button)
        button_group = GroupWidget(button_layout)

        info_layout = QtWidgets.QHBoxLayout()
        self.info_label = QtWidgets.QLabel("Done:")
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(load_images_group)
        layout.addWidget(table_group, 2)
        layout.addWidget(button_group)
        layout.addLayout(info_layout)

        self.setLayout(layout)

    def populate(self) -> None:
        """Populate gui."""
        self.directory_path_lineedit.setText(os.getcwd())
        self.load_images()

    def _connect(self) -> None:
        """Connect signals."""
        self.scan_dir_pushbutton.clicked.connect(self.load_images)
        self.directory_path_lineedit.enter.connect(self.load_images)
        self.convert_button.clicked.connect(self.convert_images)

    @QtCore.Slot()
    def load_images(self) -> None:
        """Scan directory for images and add them."""
        self.update_info("Start scanning directory:")
        file_path = self.directory_path_lineedit.text()
        if not os.path.isdir(file_path):
            LOG.info('File path "{}" does not exist.'.format(file_path))
            self.update_info("Scanning aborted file path does not exist:")
            return

        self.directory_path_lineedit.setText("")  # Reset widget.
        self._scan_directories_for_elements(file_path)

    def _scan_directories_for_elements(self, file_path: str) -> None:
        """Scan directory for images.

        Args:
            file_path: Directory path to scan.

        """
        load_tread = LoadElementThread(self, file_path)
        load_tread.add_element.connect(self.table_widget.model.add_element)
        load_tread.message_event.connect(self.update_info)
        load_tread.start()

    @QtCore.Slot()
    def convert_images(self) -> None:
        """Convert selected image elements to tx."""
        elements_to_convert = [element for element in self.table_widget.model if element.enabled]
        if not elements_to_convert:
            self.update_info("No images to convert:")
            return

        convert_thread = ConvertThread(self, elements_to_convert)
        convert_thread.message_event.connect(self.update_info)
        convert_thread.start()

    @QtCore.Slot(str)
    def update_info(self, message: str) -> None:
        """Display message to user.

        Args:
            message: Message to display.

        """
        self.info_label.setText(message)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """Accept directory paths dropped.

        Args:
            event: Drag event.

        """
        if event.mimeData().hasUrls():
            LOG.debug("Drop event accepted")
            event.accept()
        else:
            LOG.debug("Drop event rejected")
            self.update_info("Drop event rejected")
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """Load directory paths.

        Args:
            event: Drop event.

        """
        for path in event.mimeData().urls():
            self._scan_directories_for_elements(path.path())


def run() -> None:
    """Start tool. """
    app = QtWidgets.QApplication(sys.argv)
    window = MaketxWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()

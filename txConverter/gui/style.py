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

"""Qt application style sheet template."""

STYLE_SHEET_TEMPLATE = """
QWidget
{{
    color: white;
    background: {DISABLED_WIDGET_COLOR};
    border-color: {BORDER_COLOR};
}}


QWidget::disabled
{{
    color: grey;
    background: {FOREGROUND_COLOR};
    border-color: {DISABLED_WIDGET_COLOR};
}}


QWidget[transparent=true]
{{
    background: transparent;
}}


QLabel
{{
    background: transparent;
    border-radius: 2px;
}}


QLabel::disabled, QCheckBox:disabled
{{
    background: transparent;
}}


QCheckBox
{{
    background: {FOREGROUND_COLOR};
}}


QCheckBox::indicator:disabled
{{
    border-radius: 3px;
    border: 1px solid {DISABLED_WIDGET_COLOR};
    background: {FOREGROUND_COLOR};
}}


QPushButton, QComboBox, QLineEdit
{{
    border-radius: 2px;
    border-style: solid;
    border-width: 1px;
    background: {WIDGET_COLOR_INPUT};
}}


QPushButton
{{
    padding: 1 5px;
}}


QPushButton::hover
{{
    background: {SELECTED_COLOR};
}}


QPushButton::pressed
{{
    background: {CLICKED_COLOR};
}}


QGroupBox
{{
    border: 1px solid rgb(28, 28, 28);
    border-radius: 7px;
    margin-top: 9px;
    padding-top: 8px;
    padding-right: 4px;
    padding-bottom: 0px;
    padding-left: 4px;
    background: rgb(60, 60, 60);
}}


QGroupBox::title
{{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    background: transparent;
    padding-left: 4px;
    padding-right: 4px;
    position: absolute;
    left: 7px;
}}


QTableView, QListView, QPlainTextEdit
{{
    background: {DARK_BACKGROUND_COLOR};
    border-width: 1px;
    border-style: solid;
    border-radius: 3px;
}}


QTableView::item
{{
    background: {FOREGROUND_COLOR};
    border-bottom: 1px dashed {BORDER_COLOR};
    border-left: 1px dashed {BORDER_COLOR};
}}


QTableView::item:selected, QTreeView::item:selected
{{
    background: {SELECTED_COLOR};
}}


QHeaderView::down-arrow
{{
    width: 0;
    height: 0;
    border-left: 4px solid rgba(132, 132, 132, 0);
    border-right: 4px solid rgba(132, 132, 132, 0);
    border-top: 7px solid rgb(132, 132, 132);
    margin-right: 7px;
}}


QHeaderView::section
{{
    border: 1px solid rgb(25, 25, 25);
    border-right: 0;
    padding: 5px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 rgb(58, 58, 58), stop: 1.0 rgb(39, 39, 39) );
}}


QHeaderView::up-arrow
{{
    width: 0;
    height: 0;
    border-left: 4px solid rgba(86, 86, 86, 0);
    border-right: 4px solid rgba(86, 86, 86, 0);
    border-bottom: 7px solid rgb(132, 132, 132);
    margin-right: 7px;
}}
"""

_BORDER_COLOR = "hsv(0, 0%,  5%)"
_DARK_BACKGROUND_COLOR = "hsv(0, 0%, 11%)"
_DISABLED_WIDGET_COLOR = "hsv(0, 0%, 19%)"
_FOREGROUND_COLOR = "hsv(0, 0%, 30%)"
_WIDGET_COLOR_INPUT = "hsv(0, 0%, 50%)"
_SELECTED_COLOR = "hsv(217, 65%, 100%)"
_CLICKED_COLOR = "hsv(217, 39%, 92%)"

QT_STYLE = STYLE_SHEET_TEMPLATE.format(
    BORDER_COLOR=_BORDER_COLOR,
    FOREGROUND_COLOR=_FOREGROUND_COLOR,
    DISABLED_WIDGET_COLOR=_DISABLED_WIDGET_COLOR,
    DARK_BACKGROUND_COLOR=_DARK_BACKGROUND_COLOR,
    WIDGET_COLOR_INPUT=_WIDGET_COLOR_INPUT,
    CLICKED_COLOR=_CLICKED_COLOR,
    SELECTED_COLOR=_SELECTED_COLOR,
)

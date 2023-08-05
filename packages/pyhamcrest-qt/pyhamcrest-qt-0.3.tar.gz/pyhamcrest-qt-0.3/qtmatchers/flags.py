# pyhamcrest-qt - PyHamcrest extensions for use with Qt (either pyside2 or PyQt5)
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from Qt5 import QtCore


class HasFlags(BaseMatcher):
    def __init__(self, names, expected):
        self.names = names
        self.expected = expected

    def _matches(self, item) -> bool:
        return item == self.expected

    def describe_to(self, description: Description) -> None:
        description.append_text(f"flags: {self._qt_flags_to_str(self.expected)}")

    def describe_mismatch(self, item, mismatch_description: Description) -> None:
        mismatch_description.append_text(f"was {self._qt_flags_to_str(item)}")

    def _qt_flags_to_str(self, flags):
        str_list = []
        for flag, name in self.names.items():
            if flag & flags:
                str_list.append(name)
        return "( {} )".format(" | ".join(str_list))


def has_item_flags(flags: QtCore.Qt.ItemFlags) -> HasFlags:
    names = {
        QtCore.Qt.NoItemFlags: "NoItemFlags",
        QtCore.Qt.ItemIsSelectable: "ItemIsSelectable",
        QtCore.Qt.ItemIsEditable: "ItemIsEditable",
        QtCore.Qt.ItemIsDragEnabled: "ItemIsDragEnabled",
        QtCore.Qt.ItemIsDropEnabled: "ItemIsDropEnabled",
        QtCore.Qt.ItemIsUserCheckable: "ItemIsUserCheckable",
        QtCore.Qt.ItemIsEnabled: "ItemIsEnabled",
        QtCore.Qt.ItemIsAutoTristate: "ItemIsAutoTristate",
        QtCore.Qt.ItemNeverHasChildren: "NeverHasChildren",
        QtCore.Qt.ItemIsUserTristate: "ItemIsUSerTristate",
    }
    return HasFlags(names, flags)


def has_window_type(window_type: QtCore.Qt.WindowType) -> HasFlags:
    names = {
        QtCore.Qt.Widget: "Widget",
        QtCore.Qt.Window: "Window",
        QtCore.Qt.Dialog: "Dialog",
        QtCore.Qt.Sheet: "Sheet",
        QtCore.Qt.Drawer: "Drawer",
        QtCore.Qt.Popup: "Popup",
        QtCore.Qt.Tool: "Tool",
        QtCore.Qt.ToolTip: "ToolTip",
        QtCore.Qt.SplashScreen: "Splashscreen",
        QtCore.Qt.Desktop: "Desktop",
        QtCore.Qt.SubWindow: "SubWindow",
        QtCore.Qt.ForeignWindow: "ForeignWindow",
        QtCore.Qt.CoverWindow: "CoverWindow"
    }
    return HasFlags(names, window_type)

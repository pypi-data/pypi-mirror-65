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


class HasProperty(BaseMatcher):
    def __init__(self, function, expected, desc_true, desc_false):
        self.function = function
        self.expected = expected
        self.desc = {
            True: desc_true,
            False: desc_false
        }

    def _matches(self, item) -> bool:
        return getattr(item, self.function)() == self.expected

    def describe_to(self, description: Description) -> None:
        description.append_text(f"widget to be {self.desc[self.expected]}.")

    def describe_mismatch(self, item, mismatch_description: Description) -> None:
        mismatch_description.append_text(f"was {self.desc[not self.expected]}.")


def enabled():
    return HasProperty("isEnabled", True, "enabled", "disabled")


def disabled():
    return HasProperty("isEnabled", False, "enabled", "disabled")

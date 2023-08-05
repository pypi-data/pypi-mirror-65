# appteka - helpers collection

# Copyright (C) 2018-2020 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Implementation of the tool for visual testing of widgets."""

import sys
from warnings import warn

from PyQt5 import QtWidgets

from appteka.pyqt import gui


class TestDialog(QtWidgets.QDialog):
    """Dialog for running unit tests of any widget when human tester
    answers to questions (ok or error)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__make_gui()
        self.widget = None
        self.tests = []
        self.test_num = 0

    def __make_gui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # description of test (test name)
        self.descr_layout = gui.add_sublayout(main_layout, "h")
        self.label_descr = gui.add_label("", self.descr_layout)
        self.label_descr.setWordWrap(True)

        # text
        self.assert_layout = gui.add_sublayout(main_layout, "h")
        self.label_assert = gui.add_label("", self.assert_layout)
        self.label_assert.setWordWrap(True)

        # place for widget to be tested
        self.widget_layout = gui.add_sublayout(main_layout, "h")

        # buttons
        self.button_layout = gui.add_sublayout(main_layout, "h")
        self.button_err = gui.add_button(
            "ERROR", self.__on_button_err, self.button_layout)
        self.button_ok = gui.add_button(
            "OK", self.__on_button_ok, self.button_layout)

    def __on_button_ok(self):
        self.tests[self.test_num - 1]['result'] = "OK"
        self.__run_next_test()

    def __on_button_err(self):
        self.tests[self.test_num - 1]['result'] = "ERROR"
        self.__run_next_test()

    def set_widget(self, widget):
        """Sets widget to be tested."""
        if self.widget is not None:
            self.widget_layout.removeWidget(self.widget)
            self.widget.deleteLater()

        self.widget = gui.add_widget(widget, self.widget_layout)

    def set_text(self, value):
        """Deprecated."""
        warn('TestDialog.set_text() deprecated. Use add_assertion.')
        self.label_assert.setText(value)

    def add_assertion(self, line):
        """Add assertion."""
        lines = self.label_assert.text()
        if lines:
            lines += "\n"
        lines += "- {}".format(line)
        self.label_assert.setText(lines)

    def __run_next_test(self):
        if self.test_num == len(self.tests):
            self.__report()
            self.close()
            return

        self._clear_asserts()
        self._set_test_name(self.tests[self.test_num]['name'])

        self.tests[self.test_num]['func']()
        self.test_num += 1

    def run(self):
        """Run all tests."""
        self.__add_tests()

        self.show()

        if not self.tests:
            return

        self.test_num = 0
        self.__run_next_test()

    def _clear_asserts(self):
        self.label_assert.setText("")

    def _set_test_name(self, text):
        self.label_descr.setText("<b>{}</b>".format(text))

    def __report(self):
        print('-----------------------------')
        print(self.__class__.__name__)
        print()
        verdict = 'PASSED'
        for test in self.tests:
            print("{}... {}".format(test['name'], test['result']))
            if test['result'] == 'ERROR':
                verdict = 'NOT PASSED'

        print('-----------------------------')
        print(verdict)
        print()

    def __add_test(self, name):
        test = {
            'func': getattr(self, name),
            'name': name,
            'result': 'ERROR',
        }
        self.tests.append(test)

    def __add_tests(self):
        for fname in dir(self):
            if fname[:5] == "test_":
                if not callable(getattr(self, fname)):
                    continue
                self.__add_test(fname)

    def disable_buttons(self):
        """Disable buttons. For example, for waiting some process
        during the test."""
        self.button_ok.setEnabled(False)
        self.button_err.setEnabled(False)

    def enable_buttons(self):
        """Enable buttons."""
        self.button_ok.setEnabled(True)
        self.button_err.setEnabled(True)


def run(class_name, *args, **kwargs):
    """Run tests.

    Examples
    --------
    >>> class TestSomeWidget(testing.TestDialog):
    >>>     def __init__(self):
    >>>         ...
    >>>     ...
    >>>
    >>> testing.run(TestSomeWidget)

    """
    app = QtWidgets.QApplication(sys.argv)
    class_name(*args, **kwargs).run()
    return app.exec()

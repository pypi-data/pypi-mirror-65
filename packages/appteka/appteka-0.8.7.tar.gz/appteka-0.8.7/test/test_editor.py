import sys
import os

sys.path.insert(0, os.path.abspath("."))
from appteka.pyqt import testing
from appteka.pyqt.codetextedit import CodeTextEdit


class TestCodeTextEdit(testing.TestDialog):
    """Tests for CodeTextEdit"""
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

    def test_text(self):
        e = CodeTextEdit()
        self.set_widget(e)

        code = ""
        code += '{\n'
        code += '  "a": 1,\n'
        code += '  "b": 2\n'
        code += '}'
        e.set_text(code)

        self.add_assertion("Some text is printed")
        self.add_assertion("Lines numbered")
        self.add_assertion("Current line is highlighted")
        self.add_assertion("Font is monospace")


testing.run(TestCodeTextEdit)

from PyQt5.QtCore import QProcess, Qt, QIODevice, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit

import sys
from Vision import TaskExecution

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buffer_size = 10000
        self.output_buffer = b''
        self.readyReadStandardOutput.connect(self.handle_output)
        self.readyReadStandardError.connect(self.handle_error)
        self.finished.connect(self.handle_finished)

        # Create a dock widget
        dock = QDockWidget("Terminal Content", self)
        console_output = QTextEdit(dock)
        console_output.setReadOnly(True)

        # Set the floating property of the dock widget
        dock.setFloating(True)

        # Add the console text edit to the dock widget
        dock.setWidget(self.console_text_edit)

        # Add the dock widget to the main window
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def run_task_execution(self):
        # Create and start the subprocess
        process = QProcess(self)
        process.readyReadStandardOutput.connect(lambda: self.handle_output(process))
        process.start('python', ['Vision.py'])

    def handle_output(self, process):
        output = process.readAllStandardOutput()
        self.output_buffer += output
        if len(self.output_buffer) > self.buffer_size:
            self.output_buffer = self.output_buffer[-self.buffer_size:]
        self.parent().console_text_edit.moveCursor(QTextCursor.End)
        self.parent().console_text_edit.insertPlainText(str(output, 'utf-8'))

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    window.run_task_execution()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
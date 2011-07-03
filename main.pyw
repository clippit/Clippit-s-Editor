#!/usr/bin/env python


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import sys

from PyQt4 import QtCore, QtGui

import editor

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainWindows = []
    for fn in sys.argv[1:] or [None]:
        textEdit = editor.Editor(fn)
        textEdit.resize(800, 600)
        textEdit.show()
        mainWindows.append(textEdit)

    sys.exit(app.exec_())

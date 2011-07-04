#!/usr/bin/env python


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import sys

from PyQt4 import QtCore, QtGui

import editor

if __name__ == '__main__':
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("Clippit")
    app.setApplicationName("Clippit's Editor")
    
    i18n = QtCore.QSettings()
    if i18n.value("lang").toString() == "zh_CN":
        appTrans = QtCore.QTranslator()
        appTrans.load('zh_CN')
        sysTrans = QtCore.QTranslator()
        sysTrans.load('qt_zh_CN')
        app.installTranslator(appTrans)
        app.installTranslator(sysTrans)

    mainWindows = []
    for fn in sys.argv[1:] or [None]:
        editor = editor.Editor(fn)
        editor.resize(960, 600)
        editor.show()
        mainWindows.append(editor)

    sys.exit(app.exec_())

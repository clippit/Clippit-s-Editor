# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Actions(QObject):
    def __init__(self, parent):
        super(Actions, self).__init__()
        self.main = parent
        self.textEdit = parent.textEdit
        

    def init(self):
        self.textEdit.currentCharFormatChanged.connect(
                self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.textEdit.setFocus()
        self.textEdit.document().modificationChanged.connect(
                self.main.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(
                self.main.setWindowModified)
        self.textEdit.document().contentsChanged.connect(
                self.main.navWidget.updatePreview)
        self.textEdit.document().undoAvailable.connect(
                self.main.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(
                self.main.actionRedo.setEnabled)
        self.textEdit.copyAvailable.connect(self.main.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.main.actionCopy.setEnabled)
        self.setCurrentFileName()
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
    
    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()
    
    def load(self, f):
        '''Load File'''
        
        if not QFile.exists(f):
            return False

        fh = QFile(f)
        if not fh.open(QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if Qt.mightBeRichText(unistr):
            self.textEdit.setHtml(unistr)
        else:
            self.textEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        '''Ask if want to save the current file'''
        
        if not self.textEdit.document().isModified():
            return True

        if self.fileName.startswith(':/'):
            return True

        ret = QMessageBox.warning(self.main, self.tr("Clippit's Editor"),
                self.tr("The document has been modified.\nDo you want to save your changes?"),
                QMessageBox.Save | QMessageBox.Discard |
                        QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.fileSave()

        if ret == QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        '''Set current filename in title bar'''
        
        self.fileName = fileName
        self.textEdit.document().setModified(False)

        if not fileName:
            shownName = 'untitled.txt'
        else:
            shownName = QFileInfo(fileName).fileName()

        self.main.setWindowTitle("%s[*] - %s" % (shownName, self.tr("Clippit's Editor")))
        self.main.setWindowModified(False)

    def fileNew(self):
        '''New File'''
        
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        '''Open File'''
        
        fn = QFileDialog.getOpenFileName(self.main, self.tr("Open File..."), None,
                self.tr("HTML-Files (*.htm *.html);;All Files (*)"))

        if fn:
            self.load(fn)

    def fileSave(self):
        '''Save File'''
        
        if not self.fileName:
            return self.fileSaveAs()

        writer = QTextDocumentWriter(self.fileName)
        success = writer.write(self.textEdit.document())
        if success:
            self.textEdit.document().setModified(False)

        return success

    def fileSaveAs(self):
        '''Save as'''
        
        fn = QFileDialog.getSaveFileName(self.main, self.tr("Save as..."), None,
                self.tr("ODF files (*.odt);;HTML-Files (*.htm *.html);;All Files (*)"))

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.odt', '.htm', '.html')):
            # Default formart
            fn += '.odt'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def filePrintPdf(self):
        fn = QFileDialog.getSaveFileName(self.main, self.tr("Export PDF"), None,
                self.tr("PDF files (*.pdf);;All Files (*)"))

        if fn:
            if QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fileName)
            self.textEdit.document().print_(printer)

    def insertImage(self):
        fn = QFileDialog.getOpenFileName(self.main, self.tr("Insert An Image"), None, 
                self.tr("Images (*.jpg *.png);;All Files (*)"))
        
        if fn:
            image = QImage(fn)
            self.textEdit.textCursor().insertImage(image)
                

    def textBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.main.actionTextBold.isChecked() else QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.main.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.main.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    def normalText(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Normal)
        fmt.setFontUnderline(False)
        fmt.setFontItalic(False)
        fmt.setFontPointSize(float(11))
        fmt.setForeground(Qt.black)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(Qt.black)
        self.textEdit.setAlignment(Qt.AlignJustify)
    
    def title1(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setFontUnderline(False)
        fmt.setFontItalic(False)
        fmt.setFontPointSize(float(26))
        self.mergeFormatOnWordOrSelection(fmt)
        self.textEdit.setAlignment(Qt.AlignHCenter)
        
    def title2(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setFontUnderline(False)
        fmt.setFontItalic(False)
        fmt.setFontPointSize(float(18))
        self.mergeFormatOnWordOrSelection(fmt)
    
    def title3(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setFontUnderline(False)
        fmt.setFontItalic(True)
        fmt.setFontPointSize(float(14))
        self.mergeFormatOnWordOrSelection(fmt)
        
    def textStyle(self, styleIndex):
        # Table Driven
        styleDict = {
            0: self.normalText, 
            1: self.title1,
            2: self.title2,
            3: self.title3,
        }

        styleDict.get(styleIndex, self.normalText)()

    def textColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.main.actionAlignLeft:
            self.textEdit.setAlignment(
                    Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.main.actionAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif action == self.main.actionAlignRight:
            self.textEdit.setAlignment(
                    Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.main.actionAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self):
        self.main.actionPaste.setEnabled(
                len(QApplication.clipboard().text()) != 0)

    def about(self):
        QMessageBox.about(self.main, self.tr("About"), 
                self.tr("This is a student project of Software Construction course.\n\n2011 Software Institution, Nanjing University"))

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.main.comboFont.setCurrentIndex(
                self.main.comboFont.findText(QFontInfo(font).family()))
        self.main.comboSize.setCurrentIndex(
                self.main.comboSize.findText("%s" % font.pointSize()))
        self.main.actionTextBold.setChecked(font.bold())
        self.main.actionTextItalic.setChecked(font.italic())
        self.main.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QPixmap(32, 32)
        pix.fill(color)
        self.main.actionTextColor.setIcon(QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & Qt.AlignLeft:
            self.main.actionAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.main.actionAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.main.actionAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.main.actionAlignJustify.setChecked(True)

    def language(self, action):
        i18n = QSettings()
        if action == self.main.actionEnglish:
            i18n.setValue("lang", "en_US")
        elif action == self.main.actionChinese:
            i18n.setValue("lang", "zh_CN")
        QMessageBox.information(self.main, self.tr("Language Changed"), 
                                self.tr("Your language will be changed when you run the application next time."))
    
    def printPreview(self, printer):
        self.textEdit.print_(printer)

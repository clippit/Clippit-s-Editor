# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import editor_rc

class Editor(QMainWindow):
    def __init__(self, fileName=None, parent=None):
        super(Editor, self).__init__(parent)
        
        self.setWindowIcon(QIcon(':/images/logo.png'))
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        
        # Setup Menu and Toolbar
        self.setupFileActions()
        self.setupEditActions()
        self.setupFormatActions()
        self.setupI18nActions()
        self.setupHelpActions()
 
        self.textEdit = QTextEdit(self)
        self.textEdit.currentCharFormatChanged.connect(
                self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFocus()
        self.setCurrentFileName()
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
        self.textEdit.document().modificationChanged.connect(
                self.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(
                self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(
                self.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(
                self.actionRedo.setEnabled)
        self.setWindowModified(self.textEdit.document().isModified())
        self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        QApplication.clipboard().dataChanged.connect(
                self.clipboardDataChanged)
        
        i18n = QSettings()
        if i18n.value("lang").toString() == "zh_CN":
            self.actionChinese.setChecked(True)
        else:
            self.actionEnglish.setChecked(True)


        if fileName is None:
            fileName = ':/example.html'

        if not self.load(fileName):
            self.fileNew()

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

    def setupFileActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle(self.tr("File Actions"))
        self.addToolBar(tb)
        tb.setIconSize(QSize(48, 48))

        menu = QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(menu)

        self.actionNew = QAction(
                QIcon.fromTheme('document-new',
                        QIcon(':/images/document-new.png')),
                self.tr("&New"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(':/images/document-open.png')),
                self.tr("&Open..."), self, shortcut=QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QAction(
                QIcon.fromTheme('document-save',
                        QIcon(':/images/document-save.png')),
                self.tr("&Save"), self, shortcut=QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QAction(
                QIcon.fromTheme('document-save-as',
                        QIcon(':/images/document-save-as.png')),
                self.tr("Save &As..."), self,
                priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.fileSaveAs)
        tb.addAction(self.actionSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 
        self.actionPrintPdf = QAction(
                QIcon(':/images/gnome-mime-application-pdf.png'),
                self.tr("&Export PDF..."), self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_D,
                triggered=self.filePrintPdf)
        tb.addAction(self.actionPrintPdf)
        menu.addAction(self.actionPrintPdf)
        menu.addSeparator()

        self.actionQuit = QAction(self.tr("&Quit"), self,
                shortcut=QKeySequence.Quit, triggered=self.close)
        menu.addAction(self.actionQuit)

    def setupEditActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle(self.tr("Edit Actions"))
        self.addToolBar(tb)
        tb.setIconSize(QSize(48, 48))

        menu = QMenu(self.tr("&Edit"), self)
        self.menuBar().addMenu(menu)

        self.actionUndo = QAction(
                QIcon.fromTheme('edit-undo',
                        QIcon(':/images/edit-undo.png')),
                self.tr("&Undo"), self, shortcut=QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QAction(
                QIcon.fromTheme('edit-redo',
                        QIcon(':/images/edit-redo.png')),
                self.tr("&Redo"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        tb.addSeparator()
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QAction(
                QIcon.fromTheme('edit-cut',
                        QIcon(':/images/edit-cut.png')),
                self.tr("Cu&t"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QAction(
                QIcon.fromTheme('edit-copy',
                        QIcon(':/images/edit-copy.png')),
                self.tr("&Copy"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QAction(
                QIcon.fromTheme('edit-paste',
                        QIcon(':/images/edit-paste.png')),
                self.tr("&Paste"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Paste,
                enabled=(len(QApplication.clipboard().text()) != 0))
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)

    def setupFormatActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle(self.tr("Format Actions"))
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(tb)
        tb.setIconSize(QSize(48, 48))

        menu = QMenu(self.tr("F&ormat"), self)
        self.menuBar().addMenu(menu)

        self.actionTextBold = QAction(
                QIcon.fromTheme('format-text-bold',
                        QIcon(':/images/format-text-bold.png')),
                self.tr("&Bold"), self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_B,
                triggered=self.textBold, checkable=True)
        bold = QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        tb.addAction(self.actionTextBold)
        menu.addAction(self.actionTextBold)

        self.actionTextItalic = QAction(
                QIcon.fromTheme('format-text-italic',
                        QIcon(':/images/format-text-italic.png')),
                self.tr("&Italic"), self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_I,
                triggered=self.textItalic, checkable=True)
        italic = QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        tb.addAction(self.actionTextItalic)
        menu.addAction(self.actionTextItalic)

        self.actionTextUnderline = QAction(
                QIcon.fromTheme('format-text-underline',
                        QIcon(':/images/format-text-underline.png')),
                self.tr("&Underline"), self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_U,
                triggered=self.textUnderline, checkable=True)
        underline = QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        tb.addAction(self.actionTextUnderline)
        menu.addAction(self.actionTextUnderline)

        menu.addSeparator()
        tb.addSeparator()

        grp = QActionGroup(self, triggered=self.textAlign)

        self.actionAlignLeft = QAction(
                QIcon.fromTheme('format-justify-left',
                        QIcon(':/images/format-justify-left.png')),
                self.tr("&Left"), grp)
        self.actionAlignCenter = QAction(
                QIcon.fromTheme('format-justify-center',
                        QIcon(':/images/format-justify-center.png')),
                self.tr("C&enter"), grp)
        self.actionAlignRight = QAction(
                QIcon.fromTheme('format-justify-right',
                        QIcon(':/images/format-justify-right.png')),
                self.tr("&Right"), grp)
        self.actionAlignJustify = QAction(
                QIcon.fromTheme('format-justify-fill',
                        QIcon(':/images/format-justify-fill.png')),
                self.tr("&Justify"), grp)

        self.actionAlignLeft.setShortcut(Qt.CTRL + Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QAction.LowPriority)

        self.actionAlignCenter.setShortcut(Qt.CTRL + Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QAction.LowPriority)

        self.actionAlignRight.setShortcut(Qt.CTRL + Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QAction.LowPriority)

        self.actionAlignJustify.setShortcut(Qt.CTRL + Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QAction.LowPriority)

        tb.addActions(grp.actions())
        tb.addSeparator()
        menu.addActions(grp.actions())
        menu.addSeparator()

        pix = QPixmap(32, 32)
        pix.fill(Qt.black)
        self.actionTextColor = QAction(QIcon(pix), self.tr("&Color..."),
                self, triggered=self.textColor)
        tb.addAction(self.actionTextColor)
        menu.addAction(self.actionTextColor)

        tb = QToolBar(self)
        tb.setAllowedAreas(
                Qt.TopToolBarArea | Qt.BottomToolBarArea)
        tb.setWindowTitle(self.tr("Font & Paragraph Actions"))
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(tb)

        comboStyle = QComboBox(tb)
        tb.addWidget(comboStyle)
        comboStyle.addItem("Standard")
        comboStyle.addItem("Bullet List (Disc)")
        comboStyle.addItem("Bullet List (Circle)")
        comboStyle.addItem("Bullet List (Square)")
        comboStyle.addItem("Ordered List (Decimal)")
        comboStyle.addItem("Ordered List (Alpha lower)")
        comboStyle.addItem("Ordered List (Alpha upper)")
        comboStyle.addItem("Ordered List (Roman lower)")
        comboStyle.addItem("Ordered List (Roman upper)")
        comboStyle.activated.connect(self.textStyle)

        self.comboFont = QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))

        self.comboSize.activated[str].connect(self.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QApplication.font().pointSize())))

    def setupHelpActions(self):
        helpMenu = QMenu(self.tr("Help"), self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction(self.tr("About"), self.about)
        helpMenu.addAction(self.tr("About &Qt"), qApp.aboutQt)
    
    def setupI18nActions(self):
        
        menu = QMenu(self.tr("&Language"), self)
        self.menuBar().addMenu(menu)
        
        grp = QActionGroup(self, triggered=self.language)
        
        self.actionEnglish = QAction(
                QIcon.fromTheme('flag-us',
                        QIcon(':/images/flag-us.png')),
                self.tr("&English"), grp)
        self.actionChinese = QAction(
                QIcon.fromTheme('flag-cn',
                        QIcon(':/images/flag-cn.png')),
                self.tr("&Chinese"), grp)
        self.actionEnglish.setCheckable(True)
        self.actionEnglish.setPriority(QAction.LowPriority)
        self.actionChinese.setCheckable(True)
        self.actionChinese.setPriority(QAction.LowPriority)
        
        menu.addActions(grp.actions())
        
    
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

        ret = QMessageBox.warning(self, self.tr("Clippit's Editor"),
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

        self.setWindowTitle("%s[*] - %s" % (shownName, self.tr("Clippit's Editor")))
        self.setWindowModified(False)

    def fileNew(self):
        '''New File'''
        
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        '''Open File'''
        
        fn = QFileDialog.getOpenFileName(self, self.tr("Open File..."), None,
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
        
        fn = QFileDialog.getSaveFileName(self, self.tr("Save as..."), None,
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
        fn = QFileDialog.getSaveFileName(self, self.tr("Export PDF"), None,
                self.tr("PDF files (*.pdf);;All Files (*)"))

        if fn:
            if QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fileName)
            self.textEdit.document().print_(printer)

    def textBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
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

    def textStyle(self, styleIndex):
        cursor = self.textEdit.textCursor()
        if styleIndex:
            styleDict = {
                1: QTextListFormat.ListDisc,
                2: QTextListFormat.ListCircle,
                3: QTextListFormat.ListSquare,
                4: QTextListFormat.ListDecimal,
                5: QTextListFormat.ListLowerAlpha,
                6: QTextListFormat.ListUpperAlpha,
                7: QTextListFormat.ListLowerRoman,
                8: QTextListFormat.ListUpperRoman,
            }

            style = styleDict.get(styleIndex, QTextListFormat.ListDisc)
            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()
            else:
                listFmt.setIndent(blockFmt.indent() + 1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()
        else:
            bfmt = QTextBlockFormat()
            bfmt.setObjectIndex(-1)
            cursor.mergeBlockFormat(bfmt)

    def textColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(
                    Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(
                    Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(
                len(QApplication.clipboard().text()) != 0)

    def about(self):
        QMessageBox.about(self, self.tr("About"), 
                self.tr("This is a student project of Software Construction course.\n\n2011 Software Institution, Nanjing University"))

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QPixmap(32, 32)
        pix.fill(color)
        self.actionTextColor.setIcon(QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)

    def language(self, action):
        i18n = QSettings()
        if action == self.actionEnglish:
            i18n.setValue("lang", "en_US")
        elif action == self.actionChinese:
            i18n.setValue("lang", "zh_CN")
        QMessageBox.information(self, self.tr("Language Changed"), 
                                self.tr("Your language will be changed when you run the application next time."))
                

# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import editor_rc
from actions import Actions

class Editor(QMainWindow):
    def __init__(self, fileName=None, parent=None):
        super(Editor, self).__init__(parent)
        
        self.setWindowIcon(QIcon(':/images/logo.png'))
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        
        self.textEdit = QTextEdit(self)
        self.commands = Actions(parent=self)
        
        # Setup Menu and Toolbar
        self.setupFileActions()
        self.setupEditActions()
        self.setupFormatActions()
        self.setupI18nActions()
        self.setupHelpActions()
        self.setupNavDock()
        
        self.commands.init()
        
        self.setCentralWidget(self.textEdit)
        self.setWindowModified(self.textEdit.document().isModified())

        QApplication.clipboard().dataChanged.connect(
                self.commands.clipboardDataChanged)
        
        i18n = QSettings()
        if i18n.value("lang").toString() == "zh_CN":
            self.actionChinese.setChecked(True)
        else:
            self.actionEnglish.setChecked(True)

        if fileName is None:
            fileName = ':/example.html'

        if not self.commands.load(fileName):
            self.commands.fileNew()

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
                shortcut=QKeySequence.New, triggered=self.commands.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(':/images/document-open.png')),
                self.tr("&Open..."), self, shortcut=QKeySequence.Open,
                triggered=self.commands.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QAction(
                QIcon.fromTheme('document-save',
                        QIcon(':/images/document-save.png')),
                self.tr("&Save"), self, shortcut=QKeySequence.Save,
                triggered=self.commands.fileSave, enabled=self.textEdit.document().isModified())
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QAction(
                QIcon.fromTheme('document-save-as',
                        QIcon(':/images/document-save-as.png')),
                self.tr("Save &As..."), self,
                priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.commands.fileSaveAs)
        tb.addAction(self.actionSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 
        self.actionPrintPdf = QAction(
                QIcon(':/images/gnome-mime-application-pdf.png'),
                self.tr("&Export PDF..."), self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_D,
                triggered=self.commands.filePrintPdf)
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
                self.tr("&Undo"), self, shortcut=QKeySequence.Undo, 
                triggered=self.textEdit.undo, 
                enabled=self.textEdit.document().isUndoAvailable())
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QAction(
                QIcon.fromTheme('edit-redo',
                        QIcon(':/images/edit-redo.png')),
                self.tr("&Redo"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Redo, triggered=self.textEdit.redo, 
                enabled=self.textEdit.document().isRedoAvailable())
        tb.addAction(self.actionRedo)
        tb.addSeparator()
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QAction(
                QIcon.fromTheme('edit-cut',
                        QIcon(':/images/edit-cut.png')),
                self.tr("Cu&t"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Cut, triggered=self.textEdit.cut, 
                enabled=False)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QAction(
                QIcon.fromTheme('edit-copy',
                        QIcon(':/images/edit-copy.png')),
                self.tr("&Copy"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Copy, triggered=self.textEdit.copy, 
                enabled=False)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QAction(
                QIcon.fromTheme('edit-paste',
                        QIcon(':/images/edit-paste.png')),
                self.tr("&Paste"), self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Paste, triggered=self.textEdit.paste, 
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
                triggered=self.commands.textBold, checkable=True)
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
                triggered=self.commands.textItalic, checkable=True)
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
                triggered=self.commands.textUnderline, checkable=True)
        underline = QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        tb.addAction(self.actionTextUnderline)
        menu.addAction(self.actionTextUnderline)

        menu.addSeparator()
        tb.addSeparator()

        grp = QActionGroup(self, triggered=self.commands.textAlign)

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
                self, triggered=self.commands.textColor)
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
        comboStyle.activated.connect(self.commands.textStyle)

        self.comboFont = QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.commands.textFamily)

        self.comboSize = QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))

        self.comboSize.activated[str].connect(self.commands.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QApplication.font().pointSize())))

    def setupHelpActions(self):
        helpMenu = QMenu(self.tr("Help"), self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction(self.tr("About"), self.commands.about)
        helpMenu.addAction(self.tr("About &Qt"), qApp.aboutQt)
    
    def setupI18nActions(self):
        
        menu = QMenu(self.tr("&Language"), self)
        self.menuBar().addMenu(menu)
        
        grp = QActionGroup(self, triggered=self.commands.language)
        
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
        
    def setupNavDock(self):
        navDockWidget = QDockWidget(self.tr("Navigation"), self)
        navDockWidget.setObjectName("LogDockWidget")
        navDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)
        
        self.printer = QPrinter(QPrinter.ScreenResolution)
        self.navWidget = QPrintPreviewWidget(self.printer)
        self.navWidget.paintRequested.connect(self.commands.printPreview)
        
        navDockWidget.setWidget(self.navWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, navDockWidget)
    

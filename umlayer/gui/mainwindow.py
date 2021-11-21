import logging

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from .. import model
from . import *


class MainWindow(QMainWindow):
    """Main window of the UMLayer application
    """

    def __init__(self, project_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project_logic = project_logic
        self.readSettings()
        self.setDefaultFileName()
        self.initGUI()

        self.element_with_text = None

    @property
    def project(self):
        return self.project_logic.project

    def setDefaultFileName(self):
        self.filename = model.constants.DEFAULT_FILENAME

    def writeSettings(self):
        settings = QSettings()
        settings.beginGroup("MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        settings.endGroup()

    def readSettings(self):
        logging.info('Settings loading started')
        settings = QSettings()
        settings.beginGroup("MainWindow")
        geometry_array = settings.value("geometry", QByteArray())
        assert isinstance(geometry_array, QByteArray)

        if geometry_array.isEmpty():
            self.setGeometry(200, 200, 400, 300)
            self.center()
        else:
            self.restoreGeometry(geometry_array)

        logging.info('Geometry set: {0}'.format(self.geometry()))
        settings.endGroup()
        logging.info('Settings loading finished')

    def updateTitle(self):
        title = model.utils.build_window_title(self.filename, self.project.is_dirty)
        self.setWindowTitle(title)

    def initGUI(self):
        logging.info('GUI initialization started')
        self.setupComponents()
        self.updateTitle()
        logging.info('GUI initialization finished')

    def createToolBar(self):
        self.aToolBar: QToolBar = self.addToolBar('Main')
        self.aToolBar.addAction(self.actions.newAction)
        # self.aToolBar.addSeparator()
        # self.aToolBar.addAction(self.actions.copyAction)
        # self.aToolBar.addAction(self.actions.pasteAction)
        self.aToolBar.addSeparator()
        self.aToolBar.addAction(self.actions.addActorElementAction)
        self.aToolBar.addAction(self.actions.addEllipseElementAction)
        self.aToolBar.addAction(self.actions.addLineElementAction)
        self.aToolBar.addAction(self.actions.addRelationshipElementAction)
        self.aToolBar.addAction(self.actions.addTextElementAction)
        self.aToolBar.addAction(self.actions.addCenteredTextElementAction)
        self.aToolBar.addAction(self.actions.addNoteElementAction)
        self.aToolBar.addAction(self.actions.addSimpleClassElementAction)
        self.aToolBar.addAction(self.actions.addFatClassElementAction)
        self.aToolBar.addAction(self.actions.addPackageElementAction)
        # self.aToolBar.addAction(self.actions.addHandleItemAction)

    def createStatusBar(self):
        """Create Status Bar
        """

        self.aStatusBar = QStatusBar(self)
        self.aStatusLabel = QLabel(self.aStatusBar)
        self.aStatusBar.addWidget(self.aStatusLabel, 3)
        self.setStatusBar(self.aStatusBar)

    def createElementsWindow(self):
        elementsWindow = QDockWidget('Elements', self)
        self.elementsView = QTextEdit()
        elementsWindow.setWidget(self.elementsView)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, elementsWindow)

    def createPropertyEditor(self):
        propertyWindow = QDockWidget('Property editor', self)
        self.propertyView = QPlainTextEdit()
        self.propertyView.textChanged.connect(self.on_text_changed)
        self.propertyView.setFont(element_font)
        self.propertyView.setWordWrapMode(QTextOption.NoWrap)
        self.propertyView.setEnabled(False)
        propertyWindow.setWidget(self.propertyView)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, propertyWindow)

    def on_text_changed(self):
        if self.element_with_text is None:
            return
        text = self.propertyView.toPlainText()
        self.element_with_text.setText(text)

    def on_scene_selection_changed(self):
        elements_with_text = [item for item in self.scene.selectedItems()
                             if isinstance(item, BaseElement) and
                             Abilities.EDITABLE_TEXT in item.getAbilities()]
        if len(elements_with_text) == 1:
            self.element_with_text = elements_with_text[0]
            self.propertyView.setPlainText(self.element_with_text.text())
            self.propertyView.setEnabled(True)
        else:
            self.element_with_text = None
            self.propertyView.setPlainText(None)
            self.propertyView.setEnabled(False)

    def createCentralWidget(self):
        scene_size = 2000
        self.scene: GraphicsScene = \
            GraphicsScene(-scene_size//2, -scene_size//2, scene_size, scene_size)

        self.scene.selectionChanged.connect(self.on_scene_selection_changed)

        self.sceneView = GraphicsView(self.scene)
        self.sceneView.setRenderHints(
            QPainter.Antialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.VerticalSubpixelPositioning
        )

        vbox = QVBoxLayout()
        vbox.addWidget(self.sceneView)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(vbox)
        self.setCentralWidget(self.centralWidget)

    def setupComponents(self):
        """ Initialize visual components
        """

        self.logic = GuiLogic(self)

        self.createStatusBar()  # used in actions
        self.createProjectTree()
        self.createElementsWindow()
        self.createPropertyEditor()
        self.createCentralWidget()  # used in actions

        self.actions = Actions(self)
        self.createMenu()
        self.createToolBar()

    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.helpMenu = self.menuBar().addMenu("&Help")

        self.fileMenu.addAction(self.actions.newAction)
        self.fileMenu.addAction(self.actions.openAction)
        self.fileMenu.addAction(self.actions.saveAction)
        self.fileMenu.addAction(self.actions.saveAsAction)
        self.fileMenu.addAction(self.actions.closeAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actions.exitAction)
        self.editMenu.addAction(self.actions.copyAction)
        self.fileMenu.addSeparator()
        self.editMenu.addAction(self.actions.pasteAction)
        self.helpMenu.addAction(self.actions.aboutAction)

    def center(self):
        """Center the main window
        """

        qRect = self.frameGeometry()
        centerPoint = self.screen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def closeEvent(self, event):
        if self.logic.saveFileIfNeeded():
            self.writeSettings()
            logging.info('Main window closed')
            event.accept()
        else:
            event.ignore()

    def onTreeViewCustomContextMenuRequested(self, point):
        # show context menu
        item = self.treeView.getSelectedItem()

        if item is None:
            return

        element = self.treeView.elementFromItem(item)

        menu = QMenu(self.treeView)

        if type(element) is model.Folder:
            menu.addAction(self.actions.createDiagramAction)
            menu.addAction(self.actions.createFolderAction)
            if element.id != self.project.root.id:
                menu.addAction(self.actions.deleteElementAction)
        elif type(element) is model.Diagram:
            menu.addAction(self.actions.deleteElementAction)

        menu.exec(self.treeView.viewport().mapToGlobal(point))

    def elementFromItem(self, item):
        element_id = item.data(Qt.UserRole)
        return self.project.get(element_id)

    def createProjectTree(self):
        treeWindow = QDockWidget('Project', self)
        self.treeView: TreeView = TreeView(self.project_logic, self)
        self.treeView.customContextMenuRequested.connect(self.onTreeViewCustomContextMenuRequested)

        treeWindow.setWidget(self.treeView)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, treeWindow)

        self.sti = StandardItemModel()
        self.treeView.setModel(self.sti)
        self.treeView.updateTreeDataModel()

        self.treeView.selectionModel().selectionChanged.connect(self.logic.on_selection_changed)

        shortcut = QShortcut(QKeySequence.Delete,
                             self.treeView,
                             context=Qt.WidgetShortcut,
                             activated=self.logic.deleteElement)

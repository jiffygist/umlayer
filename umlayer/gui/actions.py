from PySide6.QtGui import *


class Actions:
    def __init__(self, window):
        self.window = window
        self.logic = window.logic
        self.createActions()

    def createActions(self):
        self.newAction = QAction(
            icon=QIcon('resources/icons/new.png'),
            text='&New',
            parent=self.window,
            shortcut=QKeySequence.New,
            statusTip='Create a New Project',
            triggered=self.logic.newProject)

        self.openAction = QAction(
            QIcon('resources/icons/open.png'), '&Open', self.window,
            shortcut=QKeySequence.Open,
            statusTip='Open a project in editor',
            triggered=self.logic.openProject)

        self.saveAction = QAction(
            QIcon('resources/icons/save.png'), '&Save', self.window,
            shortcut=QKeySequence.Save,
            statusTip='Save a project',
            triggered=self.logic.saveProject)

        self.saveAsAction = QAction(
            QIcon('resources/icons/save_as.png'), 'Save As...', self.window,
            shortcut=QKeySequence.SaveAs,
            statusTip='Save a project',
            triggered=self.logic.saveProjectAs)

        self.closeAction = QAction(
            QIcon('resources/icons/close.png'), '&Close', self.window,
            shortcut=QKeySequence.Close,
            statusTip='Close current project',
            triggered=self.logic.closeProject)

        self.exitAction = QAction(
            QIcon('resources/icons/exit.png'), '&Quit', self.window,
            shortcut=QKeySequence.Quit,
            statusTip='Quit the Application',
            triggered=self.logic.exitApp)

        self.deleteAction = QAction(
            QIcon('resources/icons/delete.png'), '&Delete', self.window,
            shortcut="Delete",
            statusTip="Delete",
            triggered=self.logic.delete)

        self.cutAction = QAction(
            QIcon('resources/icons/cut.png'), 'Cut', self.window,
            shortcut='Ctrl+X',
            statusTip='Cut (Ctrl-X)',
            triggered=self.logic.cut)

        self.copyAction = QAction(
            QIcon('resources/icons/copy.png'), 'C&opy', self.window,
            shortcut='Ctrl+C',
            statusTip='Copy (Ctrl-C)',
            triggered=self.logic.copy)

        self.pasteAction = QAction(
            QIcon('resources/icons/paste.png'), '&Paste', self.window,
            shortcut='Ctrl+V',
            statusTip='Paste (Ctrl-V)',
            triggered=self.logic.paste)

        self.aboutAction = QAction(
            QIcon('resources/icons/about.png'), 'A&bout', self.window,
            statusTip='Displays info about the app',
            triggered=self.logic.aboutHelp)

        self.printElementsAction = QAction(
            QIcon('resources/icons/cache.png'), 'Print', self.window,
            statusTip='print',
            triggered=self.logic.printElements)

        self.printSceneElementsAction = QAction(
            QIcon('resources/icons/cache.png'), 'Print', self.window,
            statusTip='print scene elements',
            triggered=self.logic.printSceneElements)

        self.createDiagramAction = QAction(
            QIcon('resources/icons/diagram.png'), 'Create diagram', self.window,
            statusTip='Create diagram',
            triggered=self.logic.createDiagram)

        self.createFolderAction = QAction(
            QIcon('resources/icons/create_folder.png'), 'Create folder', self.window,
            statusTip='Create folder',
            triggered=self.logic.createFolder)

        self.deleteElementAction = QAction(
            QIcon('resources/icons/delete.png'), 'Delete element', self.window,
            shortcut=QKeySequence.Delete,
            statusTip='Delete element',
            triggered=self.logic.deleteElement)

        self.addActorElementAction = QAction(
            QIcon('resources/icons/user_element.svg'), 'Actor', self.window,
            statusTip='Add actor',
            triggered=self.logic.addActorElement)

        self.addEllipseElementAction = QAction(
            QIcon('resources/icons/ellipse.png'), 'Ellipse', self.window,
            statusTip='Add ellipse',
            triggered=self.logic.addEllipseElement)

        self.addLineElementAction = QAction(
            QIcon('resources/icons/simple_line.png'), 'Line', self.window,
            statusTip='Add line',
            triggered=self.logic.addLineElement)

        self.addRelationshipElementAction = QAction(
            QIcon('resources/icons/arrow_triangle.png'), 'Relationship', self.window,
            statusTip='Add relationship',
            triggered=self.logic.addLineElement)

        self.addTextElementAction = QAction(
            QIcon('resources/icons/left_text.png'), 'Text', self.window,
            statusTip='Add text',
            triggered=self.logic.addTextElement)

        self.addCenteredTextElementAction = QAction(
            QIcon('resources/icons/center_text.png'), 'Centered text', self.window,
            statusTip='Add centered text',
            triggered=self.logic.addCenteredTextElement)

        self.addNoteElementAction = QAction(
            QIcon('resources/icons/note.png'), 'Note', self.window,
            statusTip='Add note',
            triggered=self.logic.addNoteElement)

        self.addPackageElementAction = QAction(
            QIcon('resources/icons/package.png'), 'Package', self.window,
            statusTip='Add package',
            triggered=self.logic.addPackageElement)

        self.addSimpleClassElementAction = QAction(
            QIcon('resources/icons/simple_class.png'), 'Simple class', self.window,
            statusTip='Add simple class',
            triggered=self.logic.addSimpleClassElement)

        self.addFatClassElementAction = QAction(
            QIcon('resources/icons/class_icon.png'), 'Fat class', self.window,
            statusTip='Add class',
            triggered=self.logic.addFatClassElement)

        self.addHandleItemAction = QAction(
            QIcon('resources/icons/miscellaneous.png'), '', self.window,
            statusTip='Add handle',
            triggered=self.logic.addHandleItem)

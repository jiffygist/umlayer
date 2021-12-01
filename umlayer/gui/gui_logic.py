import logging

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvg import QSvgGenerator
from PySide6.QtWidgets import *

from umlayer import version, model
from . import *


class GuiLogic:
    def __init__(self):
        """Do not use window here"""

    def setWindow(self, window):
        self.window = window

    def openProject(self):
        logging.info('Action: Open')
        if not self.window.closeProject():
            return

        filename = self._getFileNameFromOpenDialog('Open')

        if len(filename) == 0:
            return

        try:
            self.window.doOpenProject(filename)
        except Exception as ex:
            print(ex)
        else:
            self.window.filename = filename
            self.window.updateTitle()

        self.window.printStats()

    def saveProject(self):
        logging.info('Action: Save')
        if self._isFileNameNotSet():
            filename = self._getFileNameFromSaveDialog('Save')
        else:
            filename = self.window.filename

        if len(filename) == 0:
            return

        try:
            self._doSaveProject(filename)
        except Exception as ex:
            raise ex
        else:
            self.window.filename = filename
            self.window.updateTitle()

    def saveProjectAs(self):
        logging.info('Action: Save As')

        filename = self._getFileNameFromSaveDialog('Save as...')

        if len(filename) == 0:
            return

        try:
            self._doSaveProject(filename)
        except Exception as ex:
            pass
        else:
            self.window.filename = filename
            self.window.updateTitle()

    def saveFileIfNeeded(self) -> bool:
        logging.info('Try to save file if needed')
        if not self.window.isDirty():
            return True

        reply = QMessageBox.question(
            self.window,
            'Warning \u2014 Umlayer',
            'The current file has been modified.\nDo you want to save it?',
            QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save,
            QMessageBox.Save)

        if reply == QMessageBox.Save:
            self.saveProject()

        return reply != QMessageBox.Cancel

    def exitApp(self):
        logging.info('Action: Exit app')
        self.window.close()

    def aboutWindow(self):
        logging.info('Action: About window')
        QMessageBox.about(
            self.window,
            'About UMLayer',
            f'<h3 align=center>UMLayer</h3>'
            f'<p align=center>{version.__version__}</p>'
            '<p align=center>UML diagram editor</p>'
            '<p align=center><a href="https://github.com/selforthis/umlayer">https://github.com/selforthis/umlayer</a></p>'
            '<p align=center>Copyright 2021 Serguei Yanush &lt;selforthis@gmail.com&gt;<p>'
            '<p align=center>MIT License</p>'
        )

    def aboutQtWindow(self):
        logging.info('Action: About Qt window')
        QMessageBox.aboutQt(self.window)

    def createDiagram(self):
        logging.info('Action: Create Diagram')
        self._createProjectItem(True)

    def createFolder(self):
        logging.info('Action: Create Folder')
        self._createProjectItem(False)

    def deleteSelectedItem(self):
        logging.info('Action: Delete selected project item')
        item: QStandardItem = self.window.treeView.getSelectedItem()
        if item is None:
            return
        id = item.data(Qt.UserRole)
        self.window.delete_project_item(id)
        index = item.index()
        self.window.sti.removeRow(index.row(), index.parent())
        self.window.updateTitle()

    def finishNameEditing(self):
        logging.info('Finish name editing')
        item: QStandardItem = self.window.treeView.getSelectedItem()
        if item is None:
            return
        id = item.data(Qt.UserRole)
        project_item = self.window.project.get(id)
        if project_item.name() != item.text():
            project_item.setName(item.text())
            self.window.setDirty(True)
        parent_item = item.parent()
        parent_item.sortChildren(0, Qt.SortOrder.AscendingOrder)
        self.window.treeView.scrollTo(item.index())

    def on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        logging.info('Project selection changed')
        selected_project_items = self._projectItemsFromSelection(selected)
        deselected_project_items = self._projectItemsFromSelection(deselected)
        self.window.scene_logic.on_project_item_selection_changed(
            selected_project_items, deselected_project_items)

    def exportAsRasterImageHandler(self):
        filename = self._getFileNameForRasterImageDialog()

        if filename is not None and len(filename.strip()) != 0:
            self.exportAsRasterImage(filename)

    def exportAsSvgImageHandler(self):
        filename = self._getFileNameForSvgImageDialog()

        if filename is not None and len(filename.strip()) != 0:
            self.exportAsSvgImage(filename)

    def _getFileNameForRasterImageDialog(self):
        initial_filename = model.constants.DEFAULT_RASTER_FILENAME
        filename, selected_filter = \
            QFileDialog.getSaveFileName(
                parent=self.window,
                caption='Export diagram as raster image',
                dir=QDir.currentPath() + '/' + initial_filename,
                filter='PNG (*.png);;JPG (*.jpg);;JPEG (*.jpeg);;BMP (*.bmp);;PPM (*.ppm);;XBM (*.xbm);;XPM (*.xpm);;All (*)',
                selectedFilter='PNG (*.png)'
            )
        return filename

    def _getFileNameForSvgImageDialog(self):
        initial_filename = model.constants.DEFAULT_SVG_FILENAME

        filename, selected_filter = \
            QFileDialog.getSaveFileName(
                parent=self.window,
                caption='Export diagram as SVG image',
                dir=QDir.currentPath() + '/' + initial_filename,
                filter='SVG image (*.svg);;All (*)',
                selectedFilter='SVG image (*.svg)')
        return filename

    def exportViewAsRasterImage(self, filename):
        pixMap = self.window.sceneView.grab()
        pixMap.save(filename)
        logging.info('The view was exported as raster image')

    def exportAsRasterImage(self, filename):
        tempScene = self.window.scene.getTempScene()
        newSceneRect = tempScene.itemsBoundingRect()
        sceneSize = newSceneRect.size().toSize()
        image = QImage(sceneSize, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(image)
        tempScene.render(painter)
        painter.end()
        image.save(filename)
        logging.info('The scene was exported as raster image')

    def exportAsSvgImage(self, filename):
        tempScene = self.window.scene.getTempScene()
        newSceneRect = tempScene.itemsBoundingRect()
        sceneSize = newSceneRect.size().toSize()
        generator = QSvgGenerator()
        generator.setFileName(filename)
        generator.setSize(sceneSize)
        generator.setViewBox(QRect(0, 0, sceneSize.width(), sceneSize.height()))
        generator.setDescription("UML diagram")
        generator.setTitle(filename)
        painter = QPainter()
        painter.begin(generator)
        tempScene.render(painter)
        painter.end()
        tempScene.clear()
        logging.info('The scene was exported as SVG image')

    def _projectItemsFromSelection(self, selection):
        result = []
        for index in selection.indexes():
            item = self.window.sti.itemFromIndex(index)
            if item is None:
                continue
            id = item.data(Qt.UserRole)
            project_item = self.window.project.get(id)
            result.append(project_item)
        return tuple(result)

    def _createProjectItem(self, isDiagram=True):
        parent_item: QStandardItem = self.window.treeView.getSelectedItem()
        parent_index = parent_item.index()
        self.window.treeView.expand(parent_index)
        parent_id = parent_item.data(Qt.UserRole)

        if isDiagram:
            project_item = self.window.create_diagram(parent_id)
        else:
            project_item = self.window.create_folder(parent_id)

        item = StandardItemModel.makeItem(project_item)
        parent_item.insertRow(0, [item])
        self.window.treeView.startEditName(item)
        self.window.updateTitle()

    def _getFileNameFromOpenDialog(self, caption=None):
        filename, selected_filter = \
            QFileDialog.getOpenFileName(
                parent=self.window,
                caption=caption,
                dir=QDir.currentPath(),
                filter="All (*);;Umlayer project (*.ulr)",
                selectedFilter="Umlayer project (*.ulr)")
        return filename

    def _getFileNameFromSaveDialog(self, caption=None):
        initial_filename = self.window.filename or model.constants.DEFAULT_FILENAME
        filename, selected_filter = \
            QFileDialog.getSaveFileName(
                parent=self.window,
                caption=caption,
                dir=QDir.currentPath() + '/' + initial_filename,
                filter="All (*);;Umlayer project (*.ulr)",
                selectedFilter="Umlayer project (*.ulr)")
        return filename

    def _doSaveProject(self, filename):
        """Really save project"""
        self.window.scene_logic.storeScene()
        self.window.save(filename)

    def _isFileNameNotSet(self) -> bool:
        return self.window.filename is None or self.window.filename == model.constants.DEFAULT_FILENAME

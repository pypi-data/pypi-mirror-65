# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from dial_core.datasets.datatype import DataTypeContainer
from dial_core.utils import log
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QActionGroup,
    QHeaderView,
    QMenu,
    QTableView,
)

from .dataset_item_delegate import DatasetItemDelegate

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget

LOGGER = log.get_logger(__name__)


class DatasetTableView(QTableView):
    """
    The DatasetTableView class providers a view for the DatasetTableModel object, and
    implements some operations for adding and deleting objects to the model.
    """

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.__input_datatypes_menu = QMenu(self)
        self.__output_datatypes_menu = QMenu(self)
        self.__input_datatypes_actions = QActionGroup(self)
        self.__output_datatypes_actions = QActionGroup(self)
        self.__fill_datatypes_menus()

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            self.__show_header_datatype_selection_menu
        )

        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        # _See DatasetItemDelegate to see how items are displayed on the dataset.
        self.setItemDelegate(DatasetItemDelegate())

    def __fill_datatypes_menus(self):
        """For each datatype defined on DataTypeContainer, add an option on the menu.
        When clicked, the model datatype will change.
        """

        # Input actions
        for name in DataTypeContainer.providers.keys():
            action = QAction(name)
            action.triggered.connect(
                lambda _=None, name=name: self.model().set_input_datatype(name)
            )

            self.__input_datatypes_actions.addAction(action)
            self.__input_datatypes_menu.addAction(action)

        # Ouptut actions
        for name in DataTypeContainer.providers.keys():
            action = QAction(name)
            action.triggered.connect(
                lambda _=None, name=name: self.model().set_output_datatype(name)
            )

            self.__output_datatypes_actions.addAction(action)
            self.__output_datatypes_menu.addAction(action)

    def contextMenuEvent(self, event: "QContextMenuEvent"):
        """Shows a context menu with the operations for modifying the dataset rows."""
        menu = QMenu(parent=self)

        menu.popup(event.globalPos())
        menu.addAction("Remove rows", lambda: self.deleteSelectedRows())
        # menu.addAction("Insert row", lambda: self.insertRow())

    def deleteSelectedRows(self):
        """Deletes the rows that are selected on the view from the model."""
        # When a row is deleted, the new row index is the last row index - 1
        # That's why we have an i variable on this loop, which represents the amount of
        # rows that have been deleted
        chunks = []

        chunk_start = -1
        chunk_end = -1
        for index in self.selectedIndexes():
            if chunk_start == -1:
                chunk_start = index.row()
                chunk_end = chunk_start
                continue

            if (
                index.row() == chunk_end
                or index.row() - 1 == chunk_end
                or index.row() + 1 == chunk_end
            ):
                chunk_end = index.row()
                continue

            chunks.append([min(chunk_start, chunk_end), max(chunk_start, chunk_end)])
            chunk_start = index.row()
            chunk_end = chunk_start

        chunks.append([chunk_start, chunk_end])

        LOGGER.debug("Chunks to remove: %s", chunks)

        for chunks in chunks:
            self.model().removeRows(row=chunks[0], count=(chunks[1] - chunks[0] + 1))

        self.clearSelection()

    def __show_header_datatype_selection_menu(self, point: "QPoint"):
        """Displays the menu used for picking a new datatype."""
        if point.x() < self.horizontalHeader().length() / 2:
            self.__input_datatypes_menu.popup(
                self.horizontalHeader().mapToGlobal(point)
            )
        else:
            self.__output_datatypes_menu.popup(
                self.horizontalHeader().mapToGlobal(point)
            )

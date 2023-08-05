# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import qimage2ndarray
from dial_core.datasets import datatype
from PySide2.QtCore import QRect, QSize, Qt
from PySide2.QtGui import QPixmap, QPixmapCache
from PySide2.QtWidgets import QStyledItemDelegate

from .dataset_table_model import DatasetTableModel

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QStyleOptionViewItem
    from PySide2.QtWidgets import QObject


class DatasetItemDelegate(QStyledItemDelegate):
    """
    The DatasetItemDelegate class provides an implemententaion for correctly painting
    data form the Dataset depending on the datatype.
    """

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.min_image_size = QSize(100, 100)

    def paint(
        self, painter: "QPainter", option: "QStyleOptionViewItem", index: "QModelIndex"
    ):
        """Pains the element acording to its datatype."""
        if not index.isValid():
            return

        raw_data = index.data(Qt.DisplayRole)
        data_type = index.data(DatasetTableModel.TypeRole)

        try:
            # _Draw imagearrays as an image
            if isinstance(data_type, datatype.ImageArray):
                self.__paint_pixmap(raw_data, painter, option, index)

            # Draw anything else as a string
            else:
                self.__paint_string(raw_data, data_type, painter, option, index)
        except ValueError:
            self.__paint_string("<Can't Display>", data_type, painter, option, index)

    def __paint_pixmap(
        self,
        raw_data,
        painter: "QPainter",
        option: "QStyleOptionViewItem",
        index: "QModelIndex",
    ):
        """Paints a pixmap centered on the cell.

        Generated pixmaps are saved on cache by the name "dataset_row_col"
        """
        # Load Qt pixap from array
        pix = QPixmap()
        pix_name = str(id(raw_data))

        if not QPixmapCache.find(pix_name, pix):
            # Load pix from raw array
            pix = QPixmap.fromImage(qimage2ndarray.array2qimage(raw_data))

            # Save pix on cache
            QPixmapCache.insert(pix_name, pix)

        pix = pix.scaled(option.rect.width(), option.rect.height(), Qt.KeepAspectRatio)

        # Calculate central position
        x_coord = option.rect.center().x() - pix.width() / 2
        y_coord = option.rect.center().y() - pix.height() / 2

        draw_rect = QRect(x_coord, y_coord, pix.width(), pix.height())

        # Draw pixm
        painter.drawPixmap(draw_rect, pix)

    def __paint_string(
        self,
        raw_data,
        data_type,
        painter: "QPainter",
        option: "QStyleOptionViewItem",
        index: "QModelIndex",
    ):
        """Paints a value that can be converted to string."""
        alignment = Qt.AlignCenter

        # Align arrays to left
        if isinstance(data_type, datatype.NumericArray):
            alignment = Qt.AlignLeft

        # Paint it
        painter.drawText(option.rect, alignment, str(raw_data))

    def sizeHint(self, option: "QStyleOptionViewItem", index: "QModelIndex"):
        """Returns the size needed by the delegate to display its contents."""
        return self.min_image_size

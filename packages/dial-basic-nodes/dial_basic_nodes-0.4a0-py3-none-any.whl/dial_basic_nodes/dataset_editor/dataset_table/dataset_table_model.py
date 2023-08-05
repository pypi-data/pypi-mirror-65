# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import DataType, DataTypeContainer, Numeric
from dial_core.utils import log
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal
from PySide2.QtGui import QPixmapCache

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject


LOGGER = log.get_logger(__name__)


class DatasetTableModel(QAbstractTableModel):
    """
    The DatasetTableModel class provides a model for displaying the content of a
    Dataset object.

    Attributes:
        dataset: The dataset associated to this model.
        max_row_count: Maximum number of rows of data to fetch from the dataset on each
            fetch operation (Default: 100).
    """

    dataset_modified = Signal(Dataset)

    TypeRole = Qt.UserRole + 1

    class ColumnLabel(IntEnum):
        Input = 0
        Output = 1

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__cached_data: List[List[Any]] = [[], []]

        self.__types: List[Optional[DataType]] = [Numeric(), Numeric()]
        self.__loaded_types: List[Dict[str, DataType]] = [{}, {}]

        self.__dataset: Optional["Dataset"] = None

        self.max_row_count = 100

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            self.TypeRole: self.__type_role,
        }

    @property
    def dataset(self) -> "Dataset":
        """Returns the Dataset object this model is representing."""
        return self.__dataset

    def load_dataset(self, dataset: "Dataset"):
        """Loads new Dataset data to the model."""

        LOGGER.debug("Loading new dataset to DatasetTableModel...")

        self.__dataset = dataset

        self.__cached_data = [[], []]

        self.__types = [Numeric, Numeric]
        self.__loaded_types = [{}, {}]

        if self.__dataset:
            self.__types = [dataset.x_type, dataset.y_type]
            self.__loaded_types = [
                {type(dataset.x_type).__name__: dataset.x_type},
                {type(dataset.y_type).__name__: dataset.y_type},
            ]

        QPixmapCache.clear()

        # Model has been reset, redraw view
        self.modelReset.emit()

        self.dataset_modified.emit(self.__dataset)

    def set_input_datatype(self, datatype_name):
        """Changes the datatype used to visalize the data.

        Any Datatype that can be used must be defined on the DataTypeContainer class.

        For example, for an image, we could use ImageArray to display and render the
        picture, or just a NumericArray to display the inner array representation of the
        image.
        """
        try:
            datatype = self.__loaded_types[0][datatype_name]
        except KeyError:
            datatype = getattr(DataTypeContainer, datatype_name)()
            self.__loaded_types[0][datatype_name] = datatype

        self.__types[0] = datatype
        self.__dataset.x_datatype = datatype
        print("Input: Using", self.__types[0])

    def set_output_datatype(self, datatype_name):
        """Changes the datatype used to visalize the data.

        Any Datatype that can be used must be defined on the DataTypeContainer class.

        For example, for an image, we could use ImageArray to display and render the
        picture, or just a NumericArray to display the inner array representation of the
        image.
        """
        try:
            datatype = self.__loaded_types[1][datatype_name]
        except KeyError:
            datatype = getattr(DataTypeContainer, datatype_name)()
            self.__loaded_types[1][datatype_name] = datatype

        self.__types[1] = datatype
        self.__dataset.y_datatype = datatype
        print("Output: Using", self.__types[1])

    def rowCount(self, parent=QModelIndex()) -> int:
        """Returns the number of rows."""
        return len(self.__cached_data[self.ColumnLabel.Input])

    def columnCount(self, parent=QModelIndex()) -> int:
        """Returns the number of columns."""
        return len(self.ColumnLabel)

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role=Qt.DisplayRole
    ):
        """Returns the name of the headers."""
        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return (
                f"{self.ColumnLabel(section).name} "
                f"({type(self.__types[section]).__name__})"
            )

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return str(section)

        return None

    def canFetchMore(self, parent: "QModelIndex") -> bool:
        """Checks if the model can fetch more data from the Dataset object."""
        if parent.isValid():
            return False

        if not self.__dataset:
            return False

        return self.rowCount() < self.__dataset.row_count()

    def fetchMore(self, parent: "QModelIndex") -> bool:
        """Loads more data from the Dataset object to the `self.__cached_data`
        variable.

        Returns if the fetch operation was sucessfully performed.
        """
        if parent.isValid() or not self.__dataset:
            return False

        remainder = self.__dataset.row_count() - self.rowCount()
        items_to_fetch = min(remainder, self.max_row_count)

        if items_to_fetch <= 0:
            return False

        # Load new rows to the cached array
        row = self.rowCount()
        count = items_to_fetch

        return self.insertRows(row, row + count - 1, QModelIndex())

    def index(self, row: int, column: int, parent=QModelIndex()):
        """Creates an index for each row/column cell.

        Column 0 is X, column 1 is Y.
        """
        if row < 0 or row > self.rowCount():
            return QModelIndex()

        try:
            return self.createIndex(row, column, self.__cached_data[column][row])
        except IndexError:
            return QModelIndex()

    def data(self, index: "QModelIndex", role=Qt.DisplayRole):
        """Returns the corresponding data depending on the specified role."""
        if not index.isValid():
            return None

        try:
            return self.__role_map[role](index.row(), index.column())
        except KeyError:
            return None

    def setData(
        self, index: "QModelIndex", value: Any, role: int = Qt.EditRole
    ) -> bool:
        """Changes the data on the cell pointed by `index`."""
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            try:
                # Processes the `value`_data written by the user. If the value can't be
                # parsed an inserted to the dataset, a ValueError exception is thrown by
                # the 'convert_to_expected_format' method
                processed_value = self.__types[index.column()].display(
                    self.__types[index.column()].convert_to_expected_format(value)
                )
                self.__cached_data[index.column()][index.row()] = processed_value
                # TODO: Modify Dataset too

                self.dataChanged.emit(index, index, (Qt.EditRole))
                return True

            except ValueError:
                LOGGER.exception("Tried to store an invalid value!!")

        return False

    def flags(self, index: "QModelIndex") -> int:
        """Returns the flags for each cell."""
        general_flags = super().flags(index)

        # try:
        #     if self.__types[index.column()].is_editable:
        #         return general_flags | Qt.ItemIsEditable
        # except IndexError:
        #     pass

        return general_flags | Qt.ItemIsEditable

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        """Inserts new rows onto the model from the Dataset object.

        Important:
            This model DOES NOT add new rows to the inner Dataset object. For adding new
            rows, see the `insert_data` method.

        Returns:
            If the rows were inserted sucessfully.
        """
        if not self.__dataset:
            return False

        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        x_set, y_set = self.__dataset.items(
            start=row, end=row + count, role=Dataset.Role.Display
        )

        self.__cached_data[self.ColumnLabel.Input][row:row] = x_set
        self.__cached_data[self.ColumnLabel.Output][row:row] = y_set

        self.endInsertRows()

        return True

    def removeRows(self, row: int, count: int, index=QModelIndex()) -> bool:
        """Removes rows from the model.

        Important:
            This model DOES NOT removes any rows from the inner Dataset object. For
            removing rows, see the `remove_data` method.

        Returns:
            If the rows were removed sucessfully.
        """
        if row < 0:
            return False

        LOGGER.debug("Remove rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())

        self.beginRemoveRows(QModelIndex(), row, row + count - 1)

        del self.__cached_data[self.ColumnLabel.Input][row : row + count]
        del self.__cached_data[self.ColumnLabel.Output][row : row + count]
        # self.__dataset.delete_rows(row, count)  # type: ignore

        self.endRemoveRows()
        LOGGER.debug("Remove rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        return True

    def __display_role(self, row: int, column: int) -> str:
        """Returns a text representation of each cell value."""
        try:
            return self.__cached_data[column][row]

        except IndexError:
            return None

    def __type_role(self, row: int, column: int):
        """Returns the datatype associated to the row value."""
        try:
            return self.__types[column]

        except IndexError:
            return None

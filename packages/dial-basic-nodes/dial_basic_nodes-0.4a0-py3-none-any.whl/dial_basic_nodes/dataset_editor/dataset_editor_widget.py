# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)

from .dataset_table import TrainTestTabs, TrainTestTabsFactory
from .datasets_list import PredefinedDatasetsList

LOGGER = log.get_logger(__name__)


class DatasetEditorWidget(QWidget):
    """
    The DatasetEditorWidget class provides a window for displaying all the datasets
    related information:
        *_Tabs with the Train/Test data
        * Labels with information about the datasets length, data types, etc.
    """

    train_dataset_modified = Signal(Dataset)
    test_dataset_modified = Signal(Dataset)

    def __init__(self, train_test_tabs: "TrainTestTabs", parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__train_test_tabs = train_test_tabs
        self.__train_test_tabs.setParent(self)

        self.__dataset_name_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__train_len_label = QLabel("")
        self.__test_len_label = QLabel("")

        # Configure interface
        self.__setup_ui()

        # Connections
        self.__dataset_loader_button.clicked.connect(self.__load_predefined_dataset)

        self.__train_test_tabs.train_dataset_modified.connect(
            lambda dataset: self.update_train_labels(dataset)
        )
        self.__train_test_tabs.test_dataset_modified.connect(
            lambda dataset: self.update_test_labels(dataset)
        )

        self.update_train_labels(self.get_train_dataset())
        self.update_test_labels(self.get_test_dataset())

    def get_train_dataset(self) -> "Dataset":
        """Returns the train dataset."""
        return self.__train_test_tabs.train_dataset()

    def get_test_dataset(self) -> "Dataset":
        """Returns the test dataset."""
        return self.__train_test_tabs.test_dataset()

    def set_train_dataset(self, train: "Dataset"):
        """Loads a new train dataset."""
        self.__train_test_tabs.set_train_dataset(train)

    def set_test_dataset(self, test: "Dataset"):
        self.__train_test_tabs.set_test_dataset(test)

    def update_train_labels(self, train: "Dataset"):
        """Update all the text labels related to the train dataset."""
        LOGGER.info(f"Train dataset updated: {train}")
        self.__train_len_label.setText(str(train.row_count()))

        self.train_dataset_modified.emit(train)

    def update_test_labels(self, test: "Dataset"):
        """Update all the text labels related to the test dataset."""
        LOGGER.info(f"Test dataset updated: {test}")
        self.__test_len_label.setText(str(test.row_count()))

        self.test_dataset_modified.emit(test)

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(500, 300)

    def __setup_ui(self):
        """Widget layout configuration."""
        splitter = QSplitter()

        # Set label names
        self.__options_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items (train)", self.__train_len_label)
        self.__options_layout.addRow("Total items (test)", self.__test_len_label)
        self.__options_layout.addRow(
            "Load predefined dataset", self.__dataset_loader_button
        )

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__train_test_tabs)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def __load_predefined_dataset(self):
        """Pop a dialog for selecting a dataset between the predefined ones.

        The selected dataset will be loaded on this widget.
        """
        datasets_loader_dialog = PredefinedDatasetsList.Dialog()
        accepted = datasets_loader_dialog.exec()

        if accepted:
            dataset_loader = datasets_loader_dialog.selected_loader()
            train, test = dataset_loader.load()

            self.__dataset_name_label.setText(dataset_loader.name)
            self.set_train_dataset(train)
            self.set_test_dataset(test)

    def __getstate__(self):
        return {
            "dataset_name": self.__dataset_name_label.text(),
            "train_len": self.__train_len_label.text(),
            "test_len": self.__test_len_label.text(),
        }

    def __setstate__(self, new_state):
        self.__dataset_name_label.setText(new_state["dataset_name"])
        self.__train_len_label.setText(new_state["train_len"])
        self.__test_len_label.setText(new_state["test_len"])

    def __reduce__(self):
        return (DatasetEditorWidget, (self.__train_test_tabs,), self.__getstate__())


DatasetEditorWidgetFactory = providers.Factory(
    DatasetEditorWidget, train_test_tabs=TrainTestTabsFactory
)

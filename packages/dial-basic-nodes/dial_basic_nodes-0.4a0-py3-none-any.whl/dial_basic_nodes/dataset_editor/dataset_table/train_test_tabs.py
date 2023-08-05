# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

from .containers import DatasetTableMVFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class TrainTestTabs(QTabWidget):
    """
    The TrainTestTabs class is a container for a pair of train/test datasets. Each
    dataset is displayed on its own tab, and can be accessed through the `train_dataset`
    and `test_dataset` methods.
    """

    train_dataset_modified = Signal(Dataset)
    test_dataset_modified = Signal(Dataset)

    def __init__(
        self, datasettable_mv_factory: "DatasetTableMVFactory", parent: "QWidget" = None
    ):
        super().__init__(parent)

        self.__train_model = datasettable_mv_factory.Model(parent=self)
        self.__train_view = datasettable_mv_factory.View(parent=self)
        self.__train_view.setModel(self.__train_model)

        self.__test_model = datasettable_mv_factory.Model(parent=self)
        self.__test_view = datasettable_mv_factory.View(parent=self)
        self.__test_view.setModel(self.__test_model)

        self.addTab(self.__train_view, "Train")
        self.addTab(self.__test_view, "Test")

        self.__train_model.dataset_modified.connect(
            lambda dataset: self.train_dataset_modified.emit(dataset)
        )
        self.__test_model.dataset_modified.connect(
            lambda dataset: self.test_dataset_modified.emit(dataset)
        )

        # Load empty datasets by default
        self.set_train_dataset(train_dataset=Dataset())
        self.set_test_dataset(test_dataset=Dataset())

    def train_dataset(self) -> "Dataset":
        """Returns the train dataset."""
        return self.__train_model.dataset

    def test_dataset(self) -> "Dataset":
        """Returns the test dataset."""
        return self.__test_model.dataset

    def set_train_dataset(self, train_dataset: "Dataset"):
        """Sets a new dataset as the train dataset."""
        self.__train_model.load_dataset(train_dataset)
        self.train_dataset_modified.emit(train_dataset)

    def set_test_dataset(self, test_dataset: "Dataset"):
        """Sets a new dataset as the test dataset."""
        self.__test_model.load_dataset(test_dataset)
        self.test_dataset_modified.emit(test_dataset)

    def __getstate__(self):
        return {
            "train_dataset": self.__train_model.dataset,
            "test_dataset": self.__test_model.dataset,
        }

    def __setstate__(self, new_state):
        self.set_train_dataset(new_state["train_dataset"])
        self.set_test_dataset(new_state["test_dataset"])

    def __reduce__(self):
        return (TrainTestTabs, (DatasetTableMVFactory(),), self.__getstate__())


TrainTestTabsFactory = providers.Factory(
    TrainTestTabs, datasettable_mv_factory=DatasetTableMVFactory
)

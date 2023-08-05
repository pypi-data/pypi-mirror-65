# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QSize, Qt, Signal
from PySide2.QtWidgets import QDockWidget, QMainWindow
from tensorflow.keras.models import Sequential

from .layers_tree import LayersTreeWidgetFactory
from .model_table import ModelTableWidgetFactory

if TYPE_CHECKING:
    from .layers_tree import LayersTreeWidget
    from .model_table import ModelTableWidget
    from PySide2.QtWidgets import QWidget


class LayersEditorWidget(QMainWindow):
    """
    Window for all the model related operations (Create/Modify NN architectures)
    """

    layers_modified = Signal()

    def __init__(
        self,
        layers_tree: "LayersTreeWidget",
        model_table: "ModelTableWidget",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize widgets
        self.__model_table = model_table
        self.__model_table.setParent(self)

        self.__layers_tree = layers_tree
        self.__layers_tree.setParent(self)

        self.__dock_layers_tree = QDockWidget(self)

        # Configure interface
        self.__setup_ui()

        self.__model_table.layers_modified.connect(lambda: self.layers_modified.emit())

    def get_model(self):
        model = Sequential()

        for layer in self.__model_table.layers:
            model.add(layer)

        return deepcopy(model)

    def sizeHint(self) -> "QSize":
        return QSize(600, 300)

    def __setup_ui(self):
        # Configure dock widget with layers tree
        self.__dock_layers_tree.setWidget(self.__layers_tree)
        self.__dock_layers_tree.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )

        self.addDockWidget(Qt.LeftDockWidgetArea, self.__dock_layers_tree)

        self.setCentralWidget(self.__model_table)

    def __reduce__(self):
        return (LayersEditorWidget, (self.__layers_tree, self.__model_table))


LayersEditorWidgetFactory = providers.Factory(
    LayersEditorWidget,
    layers_tree=LayersTreeWidgetFactory,
    model_table=ModelTableWidgetFactory,
)

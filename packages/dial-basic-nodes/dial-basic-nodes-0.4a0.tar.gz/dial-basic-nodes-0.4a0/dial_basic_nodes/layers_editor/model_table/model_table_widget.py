# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import dependency_injector.providers as providers
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .containers import ModelTableMVFactory


class ModelTableWidget(QWidget):
    """
    Widget for displaying the model definition.
    """

    layers_modified = Signal(object)

    def __init__(
        self, modeltable_mv_factory: "ModelTableMVFactory", parent: "QWidget" = None
    ):
        super().__init__(parent)

        self.__model = modeltable_mv_factory.Model(parent=self)
        self.__view = modeltable_mv_factory.View(parent=self)
        self.__view.setModel(self.__model)

        self.__main_layout = QVBoxLayout()

        self.__setup_ui()

        self.__model.layers_modified.connect(
            lambda layers: self.layers_modified.emit(layers)
        )

    @property
    def layers(self):
        return self.__model.layers

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__view)

        self.setLayout(self.__main_layout)

    def __getstate__(self):
        return {"layers": self.__model.layers}

    def __setstate__(self, new_state):
        self.__model.load_layers(new_state["layers"])

    def __reduce__(self):
        return (ModelTableWidget, (ModelTableMVFactory(),), self.__getstate__())


ModelTableWidgetFactory = providers.Factory(
    ModelTableWidget, modeltable_mv_factory=ModelTableMVFactory
)

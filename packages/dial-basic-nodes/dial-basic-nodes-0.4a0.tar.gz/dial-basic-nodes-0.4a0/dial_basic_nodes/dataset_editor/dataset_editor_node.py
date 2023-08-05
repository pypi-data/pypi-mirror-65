# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node

from .dataset_editor_widget import DatasetEditorWidgetFactory

if TYPE_CHECKING:
    from .dataset_editor_widget import DatasetEditorWidget


class DatasetEditorNode(Node):
    """The DatasetEditorNode class provides a node capable of load, visualize and modify
        Dataset objects through an interface."""

    def __init__(self, dataset_editor_widget: "DatasetEditorWidget"):
        super().__init__(
            title="Dataset Editor Node", inner_widget=dataset_editor_widget
        )

        self.add_output_port(name="Train", port_type=Dataset)
        self.add_output_port(name="Test", port_type=Dataset)

        self.outputs["Train"].set_generator_function(
            self.inner_widget.get_train_dataset
        )
        self.outputs["Test"].set_generator_function(self.inner_widget.get_test_dataset)

        self.inner_widget.train_dataset_modified.connect(
            lambda: self.outputs["Train"].send()
        )
        self.inner_widget.test_dataset_modified.connect(
            lambda: self.outputs["Test"].send()
        )

    def __reduce__(self):
        return (DatasetEditorNode, (self.inner_widget,), super().__getstate__())


DatasetEditorNodeFactory = providers.Factory(
    DatasetEditorNode, dataset_editor_widget=DatasetEditorWidgetFactory
)

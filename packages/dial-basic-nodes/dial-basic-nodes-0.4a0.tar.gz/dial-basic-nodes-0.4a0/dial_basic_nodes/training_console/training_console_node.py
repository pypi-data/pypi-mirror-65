# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node
from PySide2.QtCore import QObject
from tensorflow.keras import Model

from .training_console_widget import TrainingConsoleWidgetFactory

if TYPE_CHECKING:
    from .training_console_widget import TrainingConsoleWidget


class TrainingConsoleNode(Node, QObject):
    def __init__(
        self, training_console_widget: "TrainingConsoleWidget", parent: "QObject" = None
    ):
        QObject.__init__(self, parent)
        Node.__init__(
            self, title="Training Console", inner_widget=training_console_widget
        )

        self.add_input_port("Train", port_type=Dataset)
        self.add_input_port("Validation", port_type=Dataset)
        self.add_input_port("Model", port_type=Model)
        self.add_input_port("Hyperparameters", port_type=dict)

        self.add_output_port("Trained Model", port_type=Model)

        self.inputs["Train"].set_processor_function(self.__compile_model)
        self.inputs["Model"].set_processor_function(self.__compile_model)
        self.inputs["Hyperparameters"].set_processor_function(self.__compile_model)

        self.outputs["Trained Model"].set_generator_function(
            self.inner_widget.get_trained_model
        )

        self.inner_widget.start_training_triggered.connect(self.__start_training)
        self.inner_widget.stop_training_triggered.connect(
            self.inner_widget.stop_training
        )

    def __compile_model(self, _=None):
        hyperparameters = self.inputs["Hyperparameters"].receive()
        model = self.inputs["Model"].receive()
        train_dataset = self.inputs["Train"].receive()

        self.inner_widget.compile_model(hyperparameters, model, train_dataset)

    def __start_training(self):
        hyperparameters = self.inputs["Hyperparameters"].receive()
        train_dataset = self.inputs["Train"].receive()

        self.inner_widget.start_training(hyperparameters, train_dataset)

    def __reduce__(self):
        return (TrainingConsoleNode, (self.inner_widget,), super().__getstate__())


TrainingConsoleNodeFactory = providers.Factory(
    TrainingConsoleNode, training_console_widget=TrainingConsoleWidgetFactory
)

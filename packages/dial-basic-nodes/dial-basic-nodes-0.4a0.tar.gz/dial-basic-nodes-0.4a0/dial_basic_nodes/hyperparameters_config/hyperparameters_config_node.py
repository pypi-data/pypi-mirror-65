# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.node_editor import Node
from PySide2.QtCore import QObject

from .hyperparameters_config_widget import HyperparametersConfigWidgetFactory

if TYPE_CHECKING:
    from .hyperparameters_config_widget import HyperparametersConfigWidget


class HyperparametersConfigNode(Node, QObject):
    def __init__(
        self,
        hyperparameters_config_widget: "HyperparametersConfigWidget",
        parent: "QObject" = None,
    ):
        QObject.__init__(self, parent)
        Node.__init__(
            self,
            title="Hyperparameters Config",
            inner_widget=hyperparameters_config_widget,
        )

        self.add_output_port("hyperparameters", port_type=dict)
        self.outputs["hyperparameters"].set_generator_function(
            self.inner_widget.get_hyperparameters
        )

    def __reduce__(self):
        return (HyperparametersConfigNode, (self.inner_widget,), super().__getstate__())


HyperparametersConfigNodeFactory = providers.Factory(
    HyperparametersConfigNode,
    hyperparameters_config_widget=HyperparametersConfigWidgetFactory,
)

# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QComboBox, QFormLayout, QSpinBox, QWidget


class HyperparametersConfigWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Widgets
        self.__epoch_spinbox = QSpinBox(parent=self)
        self.__epoch_spinbox.setMinimum(1)

        self.__loss_function_combobox = QComboBox(parent=self)
        self.__loss_function_combobox.addItems(
            [
                "mean_squared_error",
                "mean_absolute_error",
                "mean_absolute_percentage_error",
                "mean_square_logarithmic_error",
                "squared_hinge",
                "hinge",
                "categorical_hinge",
                "logcosh",
                "huber_loss",
                "categorical_crossentropy",
                "sparse_categorical_crossentropy",
                "binary_crossentropy",
                "kullback_leibler_divergence",
                "poisson",
                "cosine_proximity",
                "is_categorical_crossentropy",
            ]
        )

        self.__optimizer_combobox = QComboBox()
        self.__optimizer_combobox.addItems(
            ["SGD", "RMSprop", "Adagrad", "Adadelta", "Adam", "Adamax", "Nadam"]
        )

        # Layouts
        self.__main_layout = QFormLayout()
        self.__main_layout.addRow("Epochs", self.__epoch_spinbox)
        self.__main_layout.addRow("Optimizer", self.__optimizer_combobox)
        self.__main_layout.addRow("Loss function", self.__loss_function_combobox)
        self.setLayout(self.__main_layout)

        # Hyperparameters dictionary
        self.__hyperparameters = {
            "epochs": self.__epoch_spinbox.value(),
            "loss_function": self.__loss_function_combobox.currentText(),
            "optimizer": self.__optimizer_combobox.currentText(),
        }

        self.__epoch_spinbox.valueChanged.connect(self.set_epochs)
        self.__loss_function_combobox.currentTextChanged.connect(self.set_loss_function)

    def get_hyperparameters(self):
        return self.__hyperparameters

    def get_epochs(self):
        return self.__hyperparameters["epochs"]

    def set_epochs(self, new_epoch: int):
        self.__hyperparameters["epochs"] = new_epoch
        self.__epoch_spinbox.setValue(new_epoch)

    def get_loss_function(self):
        return self.__hyperparameters["loss_function"]

    def set_loss_function(self, new_loss_function: str):
        self.__hyperparameters["loss_function"] = new_loss_function
        self.__loss_function_combobox.setCurrentText(new_loss_function)

    def sizeHint(self) -> "QSize":
        return QSize(350, 200)

    def __getstate__(self):
        return {"hyperparameters": self.__hyperparameters}

    def __setstate__(self, new_state):
        self.__hyperparameters = new_state["hyperparameters"]

        self.__epoch_spinbox.setValue(self.__hyperparameters["epochs"])
        self.__loss_function_combobox.setCurrentText(
            self.__hyperparameters["loss_function"]
        )
        self.__optimizer_combobox.setCurrentText(self.__hyperparameters["optimizer"])

    def __reduce__(self):
        return (HyperparametersConfigWidget, (), self.__getstate__())


HyperparametersConfigWidgetFactory = providers.Factory(HyperparametersConfigWidget)

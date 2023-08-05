# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QObject, QSize, QThread, Signal
from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tensorflow import keras
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

LOGGER = log.get_logger(__name__)


class SignalsCallback(keras.callbacks.Callback, QObject):
    train_batch_end = Signal()
    train_end = Signal()

    def __init__(self):
        keras.callbacks.Callback.__init__(self)
        QObject.__init__(self)

    def on_train_batch_end(self, batch, logs=None):
        self.train_batch_end.emit()

    def on_train_end(self, logs=None):
        self.train_end.emit()

    def stop_model(self):
        print("Stopping model")
        self.model.stop_training = True


class FitWorker(QThread):
    def __init__(self, model, train_dataset, hyperparameters, callbacks):
        super().__init__()

        self.__model = model
        self.__train_dataset = train_dataset
        self.__hyperparameters = hyperparameters
        self.__callbacks = callbacks

    def run(self):
        self.__model.fit(
            self.__train_dataset,
            epochs=self.__hyperparameters["epochs"],
            callbacks=self.__callbacks,
        )


class TrainingConsoleWidget(QWidget):
    start_training_triggered = Signal()
    stop_training_triggered = Signal()

    class TrainingStatus(Enum):
        Running = 1
        Stopped = 2

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.__start_training_button = QPushButton("Start training", parent=self)
        self.__stop_training_button = QPushButton("Stop training", parent=self)

        self.__buttons_layout = QHBoxLayout()
        self.__buttons_layout.addWidget(self.__start_training_button)
        self.__buttons_layout.addWidget(self.__stop_training_button)

        self.training_output_textbox = QPlainTextEdit(parent=self)
        self.training_output_textbox.setReadOnly(True)

        console_output_group = QGroupBox("Console output")
        console_output_layout = QVBoxLayout()
        console_output_layout.setContentsMargins(0, 0, 0, 0)
        console_output_layout.addWidget(self.training_output_textbox)
        console_output_group.setLayout(console_output_layout)

        self.__main_layout = QVBoxLayout()
        self.__main_layout.addLayout(self.__buttons_layout)
        self.__main_layout.addWidget(console_output_group)
        self.setLayout(self.__main_layout)

        self.__start_training_button.clicked.connect(
            lambda: self.start_training_triggered.emit()
        )

        self.__stop_training_button.clicked.connect(
            lambda: self.stop_training_triggered.emit()
        )

        self.training_status = self.TrainingStatus.Stopped

        self.__training_thread = None

        self.__trained_model = None

    @property
    def training_status(self):
        return self.__training_status

    @training_status.setter
    def training_status(self, new_status):
        self.__training_status = new_status

        if self.__training_status == self.TrainingStatus.Running:
            self.__start_training_button.setEnabled(False)
            self.__stop_training_button.setEnabled(True)

        elif self.__training_status == self.TrainingStatus.Stopped:
            self.__start_training_button.setEnabled(True)
            self.__stop_training_button.setEnabled(False)

    def get_trained_model(self):
        return self.__trained_model

    def compile_model(self, hyperparameters, model, train_dataset):
        LOGGER.debug("Compiling model")

        input_layer = Input(train_dataset.input_shape)
        output = model(input_layer)

        self.__trained_model = Model(input_layer, output)

        print(train_dataset.input_shape)

        try:
            self.__trained_model.compile(
                optimizer=hyperparameters["optimizer"],
                loss=hyperparameters["loss_function"],
                metrics=["accuracy"],
            )
        except Exception as err:
            LOGGER.exception("Model Compiling error: ", err)
            self.training_output_textbox.setPlainText(
                "> Error while compiling the model:\n", str(err)
            )
            return

        self.__trained_model.summary()

    def start_training(self, hyperparameters, train_dataset, validation_dataset=None):
        if (
            self.training_status == self.TrainingStatus.Stopped
            and self.__trained_model is not None
        ):
            signals_callback = SignalsCallback()
            signals_callback.train_end.connect(self.stop_training)

            self.stop_training_triggered.connect(signals_callback.stop_model)

            self.__fit_worker = FitWorker(
                self.__trained_model,
                train_dataset,
                hyperparameters,
                [signals_callback],
            )

            self.training_status = self.TrainingStatus.Running
            self.__fit_worker.start()

    def stop_training(self):
        self.training_status = self.TrainingStatus.Stopped

    def sizeHint(self) -> "QSize":
        return QSize(500, 300)

    def __reduce__(self):
        return (TrainingConsoleWidget, ())


TrainingConsoleWidgetFactory = providers.Factory(TrainingConsoleWidget)

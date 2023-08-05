# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .model_table_model import ModelTableModel
from .model_table_view import ModelTableView


class ModelTableMVFactory(containers.DeclarativeContainer):
    Model = providers.Factory(ModelTableModel)
    View = providers.Factory(ModelTableView)

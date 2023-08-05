# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .dataset_table_model import DatasetTableModel
from .dataset_table_view import DatasetTableView


class DatasetTableMVFactory(containers.DeclarativeContainer):
    Model = providers.Factory(DatasetTableModel)
    View = providers.Factory(DatasetTableView)

# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widgets for displaying a dataset content with Train/Test tabs.
"""

from .train_test_tabs import TrainTestTabs, TrainTestTabsFactory

__all__ = [
    "TrainTestTabsFactory",
    "TrainTestTabs",
]

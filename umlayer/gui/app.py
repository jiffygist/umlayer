from PySide6.QtWidgets import *


class UMLayerApplication(QApplication):
    """UMLayer application class.

    It stores settings and other application resources
    """

    def __init__(self, args):
        super().__init__(args)

from PyQt4 import QtCore, QtGui
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui


class Coexpress(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Meta Volcano"
    icon = "icons/metavolcano.svg"
    want_main_area = False

    def __init__(self):
        super().__init__()

        label = QtGui.QLabel("Meta Volcano!")
        self.controlArea.layout().addWidget(
            label, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

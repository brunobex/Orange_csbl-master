import numpy
import Orange.data
import os
import sys
import csv
import scipy.io
import scipy.sparse
import pandas

from Orange.widgets.widget import OWWidget, Input, Output, settings
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting

class OWWidgetName(widget.OWWidget):
    name = "Teste"
    id = "orange.widgets.widget_category.widget_name"
    description = "Test"
    icon = "icons/Default.png"
    priority = 10
    category = ""
    keywords = ["list", "of", "keywords"]

    class Inputs:
        data = Input("Data", Orange.data.Table)
# [start-snippet-1]
    class Outputs:
        sample = Output("Sampled Data", Orange.data.Table)
        other = Output("Other Data", Orange.data.Table)
# [end-snippet-1]
    proportion = settings.Setting(50)
    commitOnChange = settings.Setting(0)
   

    want_main_area = False

    foo = Setting(True)

    def __init__(self):
        super().__init__()

        # controls
        gui.rubber(self.controlArea)

    def handler(self, obj):
        pass

@Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.dataset = dataset
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.sample = None
            self.otherdata = None
            self.optionsBox.setDisabled(True)
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
        self.commit()

    def selection(self):
        if self.dataset is None:
            return

        n_selected = int(numpy.ceil(len(self.dataset) * self.proportion / 100.))
        indices = numpy.random.permutation(len(self.dataset))
        indices_sample = indices[:n_selected]
        indices_other = indices[n_selected:]
        self.sample = self.dataset[indices_sample]
        self.otherdata = self.dataset[indices_other]
        self.infob.setText('%d sampled instances' % len(self.sample))

    def commit(self):
        self.Outputs.sample.send(self.sample)
        self.Outputs.sample.send(self.otherdata)

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()
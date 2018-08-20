import sys
import math
import numpy
import numpy as np
import csv
import pandas as pd

from AnyQt.QtWidgets import QFormLayout, QApplication
from AnyQt.QtCore import Qt

import sklearn.model_selection as skl

import Orange.data

from Orange.widgets.widget import Msg, OWWidget, Input, Output, settings
from Orange.widgets import gui

from Orange.widgets.settings import Setting
from Orange.data import Table
from Orange.data.sql.table import SqlTable
from Orange.util import Reprable

from Orange.data.pandas_compat import table_from_frame



class OWExpressed(OWWidget):
    name = "Test"
    description = "Selects most expressed genes."
    category = "New"
    icon = "icons/Default.png"
    priority = 30

    class Inputs:
        data = Input("Data", Orange.data.Table)
# [start-snippet-1]
    class Outputs:
        sample = Output("Selected Genes", Orange.data.Table)
        other = Output("Other Genes", Orange.data.Table)
        number = Output("Number", int)
# [end-snippet-1]
    proportionEX = settings.Setting(50)
    proportionVA = settings.Setting(50)
    commitOnChange = settings.Setting(0)

    want_main_area = False
    resizing_enabled = False

    RandomSeed = 42
    FixedProportion, FixedSize, CrossValidation, Bootstrap = range(4)
    SqlTime, SqlProportion = range(2)

    use_seed = Setting(False)
    replacement = Setting(False)
    stratify = Setting(False)
    sql_dl = Setting(False)
    sampling_type = Setting(FixedProportion)
    sampleSizeNumber = Setting(1)
    sampleSizePercentage = Setting(70)
    sampleSizeSqlTime = Setting(1)
    sampleSizeSqlPercentage = Setting(0.1)
    number_of_folds = Setting(10)
    selectedFold = Setting(1)

    class Error(OWWidget.Error):
         no_data = Msg("Dataset is empty")



    def __init__(self):
        super().__init__()

        self.dataset = None
        self.sample = None
        self.otherdata = None
        self.sampled_instances = self.remaining_instances = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '')
        self.infoc = gui.widgetLabel(box, '')
        self.infod = gui.widgetLabel(box, '')

        box2 = gui.widgetBox(self.controlArea, "Info2")
        self.infotest = gui.widgetLabel(box2, 'Test Box.')
        self.infotes2 = gui.widgetLabel(box2, 'Testing')

        self.sampling_box = gui.vBox(self.controlArea, "Sampling Type")
        sampling = gui.radioButtons(self.sampling_box, self, "sampling_type")

        def set_sampling_type(i):
            def set_sampling_type_i():
                self.sampling_type = i
            return set_sampling_type_i                       

        gui.appendRadioButton(sampling, "Fixed proportion of data:")
        self.sampleSizePercentageSlider = gui.hSlider(
            gui.indentedBox(sampling), self,
            'proportionEX',
            minValue=0, maxValue=99, ticks=10, labelFormat="%d %%",
            callback=[self.selection, self.checkCommit],
            )

        gui.separator(self.controlArea)
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        gui.spin(self.optionsBox, self, 'proportionEX',
                 minv=0, maxv=100, step=1,
                 label='Most Expressed Genes [%]:',
                 callback=[self.selection, self.checkCommit])
        gui.spin(self.optionsBox, self, 'proportionVA',
                 minv=0, maxv=100, step=1,
                 label='Most Variant Genes [%]:',
                 callback=[self.selection, self.checkCommit])         
        gui.checkBox(self.optionsBox, self, 'commitOnChange',
                     'Commit data on selection change')
        gui.button(self.optionsBox, self, "Commit", callback=self.commit)
        self.optionsBox.setDisabled(True)

        self.resize(100,50)

        

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.dataset = dataset
            self.data = dataset
            table = Orange.data.Table(dataset)
            
            self.infoa.setText('%d Genes in dataset' % len(table))
            self.infob.setText('%d Samples in dataset' % len(table.domain))
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.sample = None
            self.otherdata = None
            self.optionsBox.setDisabled(True)
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
            self.infoc.setText('')
            self.infod.setText('')
        self.commit()

    def selection(self):
        if self.dataset is None:
            return

        data_length = len(self.data)
        n_selected = int(numpy.ceil(len(self.dataset) * self.proportionEX / 100.))
        size = np.ceil(self.proportionEX / 100 * data_length)
        
        genes = len(self.dataset)
        expressed = numpy.mean(genes)
        indices = numpy.random.permutation(len(self.dataset))
        indices_sample = indices[:n_selected]
        indices_other = indices[n_selected:]
        self.sample = size
        self.otherdata = self.dataset[indices_other]
        self.infoc.setText('%d Selected Genes in dataset' % self.sample)
        self.infod.setText('%d Selected Genes in dataset' % size)


    def commit(self):
        self.Outputs.sample.send(self.sample)
        self.Outputs.sample.send(self.otherdata)
        

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()


def main(argv=None):
    from AnyQt.QtWidgets import QApplication
    # PyQt changes argv list in-place
    app = QApplication(list(argv) if argv else [])
    argv = app.arguments()
    if len(argv) > 1:
        filename = argv[1]
    else:
        filename = "iris"

    ow = OWExpressed()
    ow.show()
    ow.raise_()

    dataset = Orange.data.Table(filename)
    ow.set_data(dataset)
    ow.handleNewSignals()
    app.exec_()
    ow.set_data(None)
    ow.handleNewSignals()
    ow.onDeleteWidget()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

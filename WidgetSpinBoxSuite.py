# -*- coding: cp1251

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SetPlatformSpecPreferences import *

class WidgetSpinBoxSuite(QWidget):
    
    
    def __init__(self, title, maxValue, isDouble=False, step=1):
        QWidget.__init__(self)
        
        self.lblTitle = QLabel(title)
#        self.lblTitle.setAlignment(Qt.AlignLeft)
        if isDouble:
            self.spinBox = QDoubleSpinBox()
        else:
            self.spinBox = QSpinBox()
        
        self.spinBox.setSingleStep(step)
        self.spinBox.setMaximum(maxValue)
        self.spinBox.setFixedSize(52, 20)
        
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.lblTitle)
        self.hbox.addWidget(self.spinBox)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    spinBoxSuite = WidgetSpinBoxSuite('Число организмов популяции', 1, True)
    spinBoxSuite.show()
    sys.exit(app.exec_())
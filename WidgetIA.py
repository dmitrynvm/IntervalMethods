# -*- coding: cp1251

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IntervalOptimizer import *
from WidgetSpinBoxSuite import *
from WidgetTableSuite import *


class WidgetGA(QWidget):
    def __init__(self):
        QWidget.__init__(self)
    
        title = 'База данных функций'
        horizontalHeaders = QStringList()
        horizontalHeaders << 'Название' << 'Вид' << 'x*' << 'f(x*)'
        A = [['Квадратичная функция', 'x^2 - 31*x', '(15.5)', '-240.25'],
             ['Функция Розенброка', '100*(x2-x1^2)^2 + (1-x1)^2', '(1,1)', '0'],
             ['Функция Треккани', 'x1^4+4*x1^3+4*x1*2+x2*2', '(0,0), (-2,0)', '0']] 
        self.tblSuiteFunctionsDB = WidgetTableSuite(title, horizontalHeaders, A)
        self.tblSuiteFunctionsDB.table.setMinimumWidth(400)
        self.tblSuiteFunctionsDB.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.spinSuiteEpsilon = WidgetSpinBoxSuite('Эпсилон', 100, True, 0.01)
        self.spinSuiteEpsilon.spinBox.setValue(0.1)
        self.spinSuiteEpsilon.spinBox.setDecimals(5)
        self.spinSuiteEpsilon.spinBox.setFixedWidth(70)
        
        self.spinSuiteRadius = WidgetSpinBoxSuite('Радиус', 1000, True, 1)
        self.spinSuiteRadius.spinBox.setValue(1)
        self.spinSuiteRadius.spinBox.setDecimals(3)
        self.spinSuiteRadius.spinBox.setFixedWidth(70)
        
        self.lblToleranceRange = QLabel('Область допустимых значений')
        self.lblToleranceRange.setAlignment(Qt.AlignHCenter)
        self.spinSuiteA1 = WidgetSpinBoxSuite('a1', 1000)
        self.spinSuiteA1.spinBox.setMinimum(-1000)
        self.spinSuiteA1.spinBox.setValue(-100)
        self.spinSuiteA2 = WidgetSpinBoxSuite('a2', 1000)
        self.spinSuiteA2.spinBox.setMinimum(-1000)
        self.spinSuiteA2.spinBox.setValue(-100)
        self.spinSuiteB1 = WidgetSpinBoxSuite('b1', 1000)
        self.spinSuiteB1.spinBox.setMinimum(-1000)
        self.spinSuiteB1.spinBox.setValue(100)
        self.spinSuiteB2 = WidgetSpinBoxSuite('b2', 1000)
        self.spinSuiteB2.spinBox.setMinimum(-1000)
        self.spinSuiteB2.spinBox.setValue(100)
        
        self.textOpt = QTextEdit()
        self.textOpt.setFixedHeight(100)
        
        self.butOptimize = QPushButton('Оптимизировать')
        self.butOptimize.setFixedSize(100, 32)
        QObject.connect(self.butOptimize, SIGNAL('clicked()'), self.ButOptimizeClick)
        
#        self.progressGeneration = QProgressBar()
        
        self.hboxA1B1 = QHBoxLayout()
        self.hboxA1B1.addWidget(self.spinSuiteA1)
        self.hboxA1B1.addWidget(self.spinSuiteB1)
        self.hboxA2B2 = QHBoxLayout()
        self.hboxA2B2.addWidget(self.spinSuiteA2)
        self.hboxA2B2.addWidget(self.spinSuiteB2)
        self.hboxButtons = QHBoxLayout()
        self.hboxButtons.addWidget(self.butOptimize)
        
        self.vboxFunctionOptions = QVBoxLayout()
        self.vboxFunctionOptions.addWidget(self.tblSuiteFunctionsDB)
        
        self.vboxGroupedFunctionOptions = QVBoxLayout()
        self.vboxGroupedFunctionOptions.addWidget(self.spinSuiteEpsilon)
        self.vboxGroupedFunctionOptions.addWidget(self.spinSuiteRadius)
        self.vboxGroupedFunctionOptions.addWidget(self.lblToleranceRange)
        self.vboxGroupedFunctionOptions.addLayout(self.hboxA1B1)
        self.vboxGroupedFunctionOptions.addLayout(self.hboxA2B2)
        
        self.groupFunctionOptions = QGroupBox()
        self.groupFunctionOptions.setTitle('Настройки минимизируемых функций')
        self.groupFunctionOptions.setLayout(self.vboxGroupedFunctionOptions)
        self.vboxFunctionOptions.addWidget(self.groupFunctionOptions)
        self.vboxFunctionOptions.addWidget(self.textOpt)
#        self.vboxFunctionOptions.addWidget(self.progressGeneration)
        self.vboxFunctionOptions.addLayout(self.hboxButtons)
        
        self.hboxTotal = QHBoxLayout(self)
        self.hboxTotal.addLayout(self.vboxFunctionOptions)
        
    
    def GetOptions(self):
        self.nOfFunction = self.tblSuiteFunctionsDB.table.currentRow()
        self.a1 = self.spinSuiteA1.spinBox.value()
        self.b1 = self.spinSuiteB1.spinBox.value()
        self.a2 = self.spinSuiteA2.spinBox.value()
        self.b2 = self.spinSuiteB2.spinBox.value()
        self.epsilon = self.spinSuiteEpsilon.spinBox.value()
        self.radius = self.spinSuiteRadius.spinBox.value()
        
            
    def PrintOptions(self):
        print 'nOfFunction:', self.nOfFunction
        print 'a1:', self.a1
        print 'b1:', self.b1
        print 'a2:', self.a2
        print 'b2:', self.a2
        print 'epsilon:', self.epsilon
        print 'radius:', self.radius

    
    def SaveOptionsToStream(self, outf):
        outf << 'ХОД РАБОТЫ ИНТЕРВАЛЬНОГО АЛГОРИТМА' << '\n\n\n'
        outf << 'Введенные характеристики' << '\n'
        outf << 'nOfFunction: ' << self.nOfFunction << '\n'
        outf << 'a1:  ' << self.a1 << '\n'
        outf << 'b1: ' << self.b1 << '\n'
        outf << 'a2: ' << self.a2 << '\n'
        outf << 'b2: ' << self.a2 << '\n'

    
    def SaveIntegralInfoToFile(self, filename, integralInfo):
        file = QFile(filename)  
        file.open(QFile.WriteOnly | QFile.Text)
        outf = QTextStream(file)
        self.SaveOptionsToStream(outf)
        for i in range(len(integralInfo)):
            outf << str(integralInfo[i])
    
    
    def MakeInfo(self, boxes, f):
        '''
        Lres - список брусов,
        f - функция включения.
        '''
        x_str = '[x]:\n' 
        for box in boxes:
            x_str += str(box) + '\n'
        f_str = '[f]([x]):\n'
        if (len(boxes) > 0 and len(boxes[0]) == 1):
            f_str += str(f(boxes[0])) + '\n'
        elif (len(boxes) > 0 and len(boxes[0]) == 2):
            f_str += str(f(boxes[0][0], boxes[0][1])) + '\n'
        return x_str + f_str
    
    
    def ButOptimizeClick(self):
        self.GetOptions()
        #self.PrintOptions()
		
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.butOptimize.setText('Идут вычисления')
		
        opt = IntervalOptimizer()
        boxStart0 = interval[self.a1, self.b1]
        boxStart1 = interval[self.a2, self.b2]
#        print  boxStart0
        Lres = []
        info = []
        Lres_clustered = []
        if self.nOfFunction == 0:
            Lres, info = opt.Optimize1d(f1,f1_grad, f1_hess, boxStart0, self.epsilon)
            # Не кластеризуется            
            Lres_clustered = []
            for pair in Lres:
                Lres_clustered.append(pair[0])
            prettyInfo = self.MakeInfo(Lres_clustered, f1)
        
        elif self.nOfFunction == 1:
            Lres, info = opt.Optimize2d(f2, f2_grad, f2_hess, boxStart0, boxStart1, self.epsilon)
            Lres_clustered = FormClusters(Lres, self.radius)
            prettyInfo = self.MakeInfo(Lres_clustered, f2)
         
        elif self.nOfFunction == 2:
#            print boxStart0, boxStart1
            Lres, info = opt.Optimize2d(f3, f3_grad, f3_hess, boxStart0, boxStart1, self.epsilon)
            Lres_clustered = FormClusters(Lres, self.radius)
            prettyInfo = self.MakeInfo(Lres_clustered, f3)
        
        QApplication.restoreOverrideCursor()
        self.butOptimize.setText('Оптимизировать')
		
        self.textOpt.setPlainText(prettyInfo)
        opt.SaveIntegralInfoToFile('IA_Info.txt', info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    widgetGA = WidgetGA()
    widgetGA.show()
    sys.exit(app.exec_())

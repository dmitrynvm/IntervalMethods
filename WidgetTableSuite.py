# -*- coding: cp1251

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SetPlatformSpecPreferences import *

class WidgetTableSuite(QWidget):
    '''
        �����, �������������� ������� ����������� �������.
    '''
    
    
    def __init__(self, title, horizontalHeaders, textMatrix):
        QWidget.__init__(self)
        
        self.horizontalHeaders = horizontalHeaders
        self.textMatrix = textMatrix
        self.lblTitle = QLabel(title)
        self.table = self.CreateTable(self.horizontalHeaders, self.textMatrix)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.lblTitle)
        self.vbox.addWidget(self.table)
        
       
    def CreateTable(self, horizontalHeaders, textMatrix):
        '''
            �������, ��������� ������� � ����������� ������� (� ������������) 
            ������� ������ TableSuite.
        '''
        m = len(textMatrix)
        n = len(textMatrix[0])
        table = QTableWidget(m, n)
        # �������������� ��������� �������
        table.setHorizontalHeaderLabels(horizontalHeaders)
        # ������������ �������������� ���������� �� ������,
        # ������������� ������� ������������ ����������.
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setResizeMode(QHeaderView.Fixed)
        # �������� ��������
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem(textMatrix[i][j])
                # ��������� item'��
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                table.setItem(i, j, item)
        return table


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    title = '������� ���������� ��������'
    horizontalHeaders = QStringList()
    horizontalHeaders << 'a_i' << 'b_i'
    A = [['-10', '10'],
         ['-10', '10']]
    
    tblSuite = WidgetTableSuite(title, horizontalHeaders, A)
#    tblSuite.ta
    
    tblSuite.show()
    sys.exit(app.exec_())
    
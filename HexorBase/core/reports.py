import thread

import variables

from gui.report import *
from PyQt4 import QtGui,QtCore

class report(QtGui.QDialog,Ui_reports_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.limit = int()
        self.count = int()
        self.progressBar.setValue(0)

        self.query_responce_table = variables.report_raw_data

        self.set_frameless_window()

        self.connect(self,QtCore.SIGNAL('update progress'),self.update_progress)

        self.rows = self.query_responce_table.rowCount()
        self.columns = self.query_responce_table.columnCount()
        self.limit = self.rows + 1
        self.progressBar.setMaximum(self.limit)

        self.report = open(variables.report_save_path,'a+')
        self.report.write(variables.report_html)
        self.report.write('<tr class="middle">')

        self.emit(QtCore.SIGNAL('update progress'))
        for fields in variables.table_description:
            self.report.write('<td><b>'+ fields[0] +'</b>&nbsp;</td>')

        self.report.write('<tr>')

        thread.start_new_thread(self.process_data,())


    def set_frameless_window(self):
        try:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        except:pass


    def process_data(self):
        for row_iterate in xrange(self.rows):
            self.report.write('<tr class="middle">')
            self.emit(QtCore.SIGNAL('update progress'))
            for column_iterate in xrange(self.columns):
                data = QtGui.QTableWidgetItem(self.query_responce_table.item(row_iterate,column_iterate))
                self.report.write('<td class="small">'+ str(data.text()) +'</td>')
            self.report.write('<tr>')

        self.report.write('''
</table>
<p>&nbsp;</p>
<p class="middle"><span class="middle"></span></p>
<p>&nbsp;</p>
</body>
</html>''')
        self.report.close()


    def update_progress(self):
        self.count += 1
        self.progressBar.setValue(self.count)
        self.setWindowTitle('Generating Report ('+ str(self.progressBar.text()) +')')
        if(self.count == self.limit):
            self.close()










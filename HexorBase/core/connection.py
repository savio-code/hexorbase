import variables
import database_core
from gui.connection import *

from PyQt4 import QtGui,QtCore

class connection_setting_dialog(QtGui.QDialog,setting_dialog):
    ''' Class for server connections dialog '''
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.setupUi(self)
        self.retranslateUi(self)
        self.server_port.setEnabled(False)              # Disables the port linedit on initilization
        self.server_connection.setFocus()
        self.database_type_label.setPixmap(QtGui.QPixmap((variables.server_logo)))
        self.setWindowTitle(variables.server_settings_title)
        self.server_name.setText(variables.server_name_label)
        self.server_port_check.setText(variables.server_port_check_label)
        self.default_server_port.setText(variables.default_server_port_label)

        #
        # Generic connection settings dialog signals,and slots
        #
        self.connect(self.server_port_check,QtCore.SIGNAL("clicked()"),self.port_selected)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),self.initiate_connection)


    def initiate_connection(self):
        ''' Function accepts database server name
            or ip address and port, assigning them
            as global variables for the main_window
            class
        '''
        global postgres_server_connection

        global database_server_port
        global database_server_hostname


        database_server_hostname = str(self.server_connection.text())
        database_server_port = str(self.server_port.text())

        reexecute_dialog = connection_setting_dialog()
        variables.report_database_ip_address = str(self.server_connection.text())

        if database_server_hostname == '':
            QtGui.QMessageBox.warning(self,"Invalid Connection Details","Please input a valid Hostname or IP address of the Database Server")
            reexecute_dialog.exec_()
        else:
            if self.server_port_check.isChecked() == True:
                if database_server_port.isdigit() == False:
                    QtGui.QMessageBox.warning(self,"Invalid Connection Details","Please input a valid Port Number of which the Database Server runs")
                    reexecute_dialog.exec_()

            variables.server_connection = '%s'%(database_server_hostname)
            database_server_port = str(self.server_port.text())


            if variables.database_type == 'MySQL':                                            # MySQL Database Connection is initiated here
                import MySQLdb
                variables.oracle_status.setText("<font color=green>Connecting...</font>")     # MySQl Status label
                try:
                    if database_server_port != '':
                        database_server_port = str(self.server_port.text())
                    else:
                        database_server_port = 3306
                    variables.mysql_server_connection = str(self.server_connection.text())
                    variables.database_mysql = MySQLdb.connect(host = variables.mysql_server_connection,user = variables.username,passwd = variables.password,port = int(database_server_port))
                    variables.database_mysql_query = variables.database_mysql.cursor()
                    variables.report_database_ip_adress_port = database_server_port
                    variables.database_mysql_status = 'connected'             # Informs the classes of an action  connection, so that the interaction window is executed instead of the settings dialog
                    variables.oracle_status.setText("<font color=green><b>Connected</b></font>")
                    self.database_interaction()                    # Run database interaction dialog
                except MySQLdb.OperationalError,exception:
                    if int(exception.args[0]) == 1045:
                        QtGui.QMessageBox.warning(self,"Invalid Username or Password","Access denied for user '%s' on server '%s'"%(variables.username,variables.server_connection))
                        variables.oracle_status.setText("<font color=red>Connection Failed</font>")
                    elif int(exception.args[0]) == 2005:
                        QtGui.QMessageBox.warning(self,"Connection Failed","Unknown MySQL server host '%s'"%(variables.server_connection))
                        variables.oracle_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()
                    elif int(exception.args[0]) == 2002:
                        QtGui.QMessageBox.warning(self,"Connection Failed","Can't connect to MySQL server through socket, connection timeout")
                        variables.oracle_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()
                    else:
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s : %s"%(exception.args[0],exception.args[1]))
                        variables.oracle_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()


            elif variables.database_type == 'Oracle':                                     # Oracle Database Connection is initiated here
                import cx_Oracle
                variables.mysql_status.setText("<font color=green>Connecting...</font>")  # Oracle Status label
                try:
                    if database_server_port == '':
                        database_server_port = 1521
                    variables.oracle_server_connection = str(self.server_connection.text())
                    dsn = cx_Oracle.makedsn(variables.oracle_server_connection,database_server_port,'')      # A DSN Desicriptor is compulsory if connecting to Oracle
                    variables.database_oracle = cx_Oracle.connect(variables.username,variables.password,dsn)
                    variables.database_oracle_query = variables.database_oracle.cursor()
                    variables.report_database_ip_adress_port = database_server_port
                    variables.database_oracle_status = 'connected'
                    variables.mysql_status.setText("<font color=green><b>Connected</b></font>")
                    self.database_interaction()                    # Run database interaction dialog
                except cx_Oracle.DatabaseError,exception:
                    if  'ORA-01017' in str(exception):
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s"%(exception))
                        variables.mysql_status.setText("<font color=red>Connection Failed</font>")
                    elif 'ORA-12560' in str(exception):
                        QtGui.QMessageBox.warning(self,"Connection Failed","Can't connect to Oracle server through socket, connection timeout")
                        variables.mysql_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()
                    else:
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s"%(exception))
                        variables.mysql_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()


            elif variables.database_type == 'PostgreSQL':                                 # PostgreSQL Database Connection is initiated here
                import psycopg2
                variables.sql_status.setText("<font color=green>Connecting...</font>")
                try:
                    if database_server_port != '':
                        database_server_port = str(self.server_port.text())
                    else:
                        database_server_port = 5432
                    variables.postgres_server_connection = str(self.server_connection.text())
                    variables.database_postgresql = psycopg2.connect(user = variables.username,host = variables.postgres_server_connection,password = variables.password,port = str(database_server_port))
                    variables.database_postgresql_query = variables.database_postgresql.cursor()
                    variables.report_database_ip_adress_port = database_server_port
                    variables.database_postgresql_status = 'connected'
                    variables.sql_status.setText("<font color=green><b>Connected</b></font>")
                    self.database_interaction()
                except psycopg2.OperationalError,exception:
                    if 'password authentication failed' in str(exception):
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s"%(exception))
                        variables.sql_status.setText("<font color=red>Connection Failed</font>")
                    else:
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s"%(exception))
                        variables.sql_status.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()


            else:                                                                   # MSSQL Database Connection is initiated here
                import pymssql
                variables.sqlite_label.setText("<font color=green>Connecting...</font>")      # MSSQl Status label
                try:
                    if database_server_port.isdigit() == True:
                        variables.server_connection = '%s:%s'%(variables.server_connection,database_server_port)
                    else:
                        variables.server_connection = '%s:1433'%(variables.server_connection)
                    variables.mssql_server_connection = str(self.server_connection.text())
                    variables.database_mssql = pymssql.connect(host = variables.mssql_server_connection,user = variables.username,password = variables.password)
                    variables.database_mssql_query = variables.database_mssql .cursor()
                    variables.database_mssql .autocommit('ON')
                    variables.report_database_ip_adress_port = database_server_port
                    variables.database_mssql_status = 'connected'             # Informs the classes of an action  connection, so that the interaction window is executed instead of the settings dialog
                    variables.sqlite_label.setText("<font color=green><b>Connected</b></font>")
                    self.database_interaction()                    # Run database interaction dialog
                except (pymssql.OperationalError),exception:
                    if 'Login failed for user' in str(exception):
                        QtGui.QMessageBox.warning(self,"Connection Failed","Login failed for user %s"%(variables.username))
                        variables.sqlite_label.setText("<font color=red>Connection Failed</font>")
                    elif 'Server is unavailable or does not exist' in str(exception):
                        QtGui.QMessageBox.warning(self,"Connection Failed","Can't connect to Microsoft SQL server through socket, connection timeout")
                        variables.sqlite_label.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()
                    else:
                        QtGui.QMessageBox.warning(self,"Connection Failed","%s"%(exception))
                        variables.sqlite_label.setText("<font color=red>Connection Failed</font>")
                        reexecute_dialog.exec_()


    def port_selected(self):
        ''' This function checks if default
            port checkbox is enabled, if True,
            then it enables the line-edit vise
            versa
        '''
        if self.server_port_check.isChecked() == True:
            self.server_port.setEnabled(True)
        else:
            self.server_port.setEnabled(False)
            self.server_port.clear()


    def database_interaction(self):
        ''' Launches the database interaction window'''
        global Qsci
        try:
            from PyQt4 import Qsci
            database_interaction = database_core.database_interaction_dialog()
            database_interaction.exec_()
        except ImportError:
            QtGui.QMessageBox.warning(self,'SQL Syntax API not installed','SQL Code editor API is not installed,Please run <font color=blue> apt-get install python-qscintilla2</font> from linux terminal to get the API installed.')




#!/usr/bin/python

import os           # For Operating system related calls
import sys          # For validating GUI functions
import thread       # for bruteforce attack


import reports
import variables
import connection
import bruteforce
import password_manager

from gui.interaction import *
from gui.main_window import *
from gui.api_reference import *
from gui.password_manager import *

from PyQt4 import QtGui,QtCore      # GUI Library


# Global variable for sqlite3
sqlite_install_status = ''                  # String variable holds the installation status of the Sqlite API

# Global variable for MySQL
mysql_install_status = ''                   # String variable holds the installation status of the MySQL API

# Global variable for Oracle
oracle_install_status = ''                   # String variable holds the installation status of the Oracle API

# Global variable for PostgreSQL
postgresql_install_status = ''                   # String variable holds the installation status of the PostgreSQL API

# Global variable for MSSQL
mssql_install_status = ''                   # String variable holds the installation status of the PostgreSQL API


class main_window(QtGui.QMainWindow,Ui_MainWindow):
    ''' Main GUI class functional definitions'''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setupUi(self)
        self.retranslateUi(self)

        global oracle_status
        global mysql_status
        global sql_status
        global sqlite_label
        global postgresql_label
        global sqlite_install_status
        global mysql_install_status
        global oracle_install_status
        global postgresql_install_status
        global mssql_install_status

        variables.oracle_status = self.oracle_status      # Made a mistake with the labeling while sorting - Oracle_status is for MySQL Label
        variables.mysql_status = self.mysql_status
        variables.sql_status = self.sql_status
        variables.sqlite_label = self.sqlite_label
        postgresql_label = self.postgresql_label

        variables.username_linedit = self.username_linedit    # Password manager needs to access the line edit area
        variables.password_linedit = self.password_linedit

        self.username_linedit.setFocus()

        try:                                    # import database API module, if not exists, then display error text
            import sqlite3
            self.postgresql_label.setText("<font color=green>SQlite version: %s.%s</font>"%(sqlite3.version_info[0],sqlite3.version_info[1]))
        except ImportError:
            sqlite_install_status = 'Not Installed'
            self.postgresql_label.setText("<font color=red>API is not Installed</font>")
        try:
            import MySQLdb
            self.oracle_status.setText("<font color=green>MySQLdb version: %s.%s.%s %s</font>"%\
                                       (MySQLdb.version_info[0],MySQLdb.version_info[1],MySQLdb.version_info[2],MySQLdb.version_info[3],))
        except ImportError:
            mysql_install_status = 'Not Installed'
            self.oracle_status.setText("<font color=red>API is not Installed</font>")
        try:
            import cx_Oracle
            self.mysql_status.setText("<font color=green>cx_Oracle version: %s</font>"%(cx_Oracle.version))
        except ImportError:
            oracle_install_status = 'Not Installed'
            self.mysql_status.setText("<font color=red>API is not Installed</font>")
        try:
            import psycopg2
            self.sql_status.setText("<font color=green>Psycopg 2.3.2</font>")
        except ImportError:
            postgresql_install_status = 'Not Installed'
            self.sql_status.setText("<font color=red>API is not Installed</font>")
        try:
            import pymssql
            self.sqlite_label.setText("<font color=green>Pymssql %s</font>"%(pymssql.__version__))
        except ImportError:
            mssql_install_status = 'Not Installed'
            self.sqlite_label.setText("<font color=red>API is not Installed</font>")


        #
        # Main window GUI buttons signals and slots
        #
        self.connect(self.mysql_button,QtCore.SIGNAL("clicked()"),self.mysql_settings)
        self.connect(self.oracle_button,QtCore.SIGNAL("clicked()"),self.oracle_settings)
        self.connect(self.postgresql,QtCore.SIGNAL("clicked()"),self.postgresql_settings)
        self.connect(self.sql_button,QtCore.SIGNAL("clicked()"),self.mssql_settings)
        self.connect(self.sqlite_button,QtCore.SIGNAL("clicked()"),self.sqlite_settings)
        self.connect(self.login_button,QtCore.SIGNAL("clicked()"),self.lock_login_area)
        self.connect(self.password_manager_button,QtCore.SIGNAL("clicked()"),self.launch_password_manager)
        self.connect(self.brutefore_database,QtCore.SIGNAL("clicked()"),self.launch_bruteforce)



    def database_interaction(self):
        ''' Launches the database interaction window'''
        try:
            from PyQt4 import Qsci
            database_interaction = database_interaction_dialog()
            database_interaction.exec_()
        except ImportError:
            QtGui.QMessageBox.warning(self,'SQL Syntax API not installed','SQL Code editor \
        API is not installed,Please run <font color=blue> apt-get install python-qscintilla2\
        </font> from linux terminal to get the API installed.'.strip('\n'))


    def launch_bruteforce(self):
        ''' Launches the brutefore window'''
        bruteforce_run = bruteforce.brutefore_dialog()
        bruteforce_run.exec_()


    def lock_login_area(self):
        if self.username_linedit.text() == '':
            self.login_button.setCheckable(False)
            QtGui.QMessageBox.warning(self,"Null Credential","Please input a username before locking the login button")
            self.login_button.setCheckable(True)
        else:
            if self.login_button.isChecked() == True:
                self.username_linedit.setEnabled(False)
                self.password_linedit.setEnabled(False)
            else:
                self.username_linedit.setEnabled(True)
                self.password_linedit.setEnabled(True)


    def launch_password_manager(self):
        password_manager_run = password_manager.password_manager()
        password_manager_run.exec_()


    def mysql_settings(self):                       # MYSQL SETTINGS
        ''' accepts connection settings and then
            attempt database connection for MySQL
        '''
        global login_button
        global mysql_install_status

        variables.database_type = 'MySQL'
        variables.username = str(self.username_linedit.text())
        variables.password = str(self.password_linedit.text())

        if mysql_install_status != 'Not Installed':
            variables.server_name_label = 'MySQL Server:'
            variables.server_port_check_label = 'MySQL Port:'
            variables.server_settings_title = 'MySQL Server Connection Settings'
            variables.default_server_port_label = '( Default MySQL port is 3306 TCP)'
            variables.server_logo = '%s/Icons/mysql_logo.ico'%(os.getcwd())

            if variables.username == '':
                QtGui.QMessageBox.warning(self,"Username error","Please Input a username and press the lock button to enable Generic database mode")
                self.username_linedit.setFocus()
            elif self.login_button.isChecked() == False:
                QtGui.QMessageBox.warning(self,"Lock Button","Please press the Lock Button to enable Generic database mode")
                self.login_button.setFocus()
            elif variables.database_mysql_status == 'connected':
                self.database_interaction()
            else:
                run_settings_dialog = connection.connection_setting_dialog()
                run_settings_dialog.exec_()

        else:
            global api_reference
            global api_server_name
            global api_installation
            global api_download_link

            api_server_name = 'MySQl'
            api_download_link = '<font color=blue>apt-get install python-mysqldb</font>'
            api_reference = '<font color=blue>http://wiki.python.org/moin/MySQL</font>'
            api_installation = ''

            run_api_dialog = api_install_link()
            run_api_dialog.exec_()






    def oracle_settings(self):                                  # ORACLE SETTINGS
        ''' accepts connection settings and then
            attempt database connection for Oracle
        '''
        global login_button
        global oracle_install_status




        variables.database_type = 'Oracle'
        variables.username = str(self.username_linedit.text())
        variables.password = str(self.password_linedit.text())

        if oracle_install_status != 'Not Installed':
            variables.server_name_label = 'Oracle Server:'
            variables.server_port_check_label = 'Oracle Port:'
            variables.server_settings_title = 'Oracle Server Connection Settings'
            variables.default_server_port_label = '( Default Oracle port is 1521 TCP )'
            variables.server_logo = '%s/Icons/Oracle_Logo.ico'%(os.getcwd())

            if variables.username == '':
                QtGui.QMessageBox.warning(self,"Username error","Please Input a username and press the lock button to enable Generic database mode")
                self.username_linedit.setFocus()
            elif self.login_button.isChecked() == False:
                QtGui.QMessageBox.warning(self,"Lock Button","Please press the Lock Button to enable Generic database mode")
                self.login_button.setFocus()
            elif variables.database_oracle_status == 'connected':
                self.database_interaction()
            else:
                run_settings_dialog = connection.connection_setting_dialog()
                run_settings_dialog.exec_()

        else:
            global api_reference
            global api_server_name
            global api_installation
            global api_download_link

            api_server_name = 'Oracle'
            api_download_link = '<font color=blue>Please check the "Oracle-API-installation" note file for instructions on how to install Oracle\'s API bindings</font>'
            api_reference = '<font color=blue>http://wiki.oracle.com/page/Python</font>'
            api_installation = ''

            run_api_dialog = api_install_link()
            run_api_dialog.exec_()



    def postgresql_settings(self):
        ''' accepts connection settings and then
            attempt database connection for PostgreSQL
        '''
        global login_button
        global postgresql_install_status




        variables.database_type = 'PostgreSQL'
        variables.username = str(self.username_linedit.text())
        variables.password = str(self.password_linedit.text())

        if postgresql_install_status != 'Not Installed':
            variables.server_name_label = 'PostgreSQL Server:'
            variables.server_port_check_label = 'PostgreSQL Port:'
            variables.server_settings_title = 'PostgreSQL Server Connection Settings'
            variables.default_server_port_label = '( Default PostgreSQL port is 5432 TCP )'
            variables.server_logo = '%s/Icons/postgresql.ico'%(os.getcwd())

            if variables.username == '':
                QtGui.QMessageBox.warning(self,"Username error","Please Input a username and press the lock button to enable Generic database mode")
                self.username_linedit.setFocus()
            elif self.login_button.isChecked() == False:
                QtGui.QMessageBox.warning(self,"Lock Button","Please press the Lock Button to enable Generic database mode")
                self.login_button.setFocus()
            elif variables.database_postgresql_status == 'connected':
                self.database_interaction()
            else:
                run_settings_dialog = connection.connection_setting_dialog()
                run_settings_dialog.exec_()

        else:
            global api_reference
            global api_server_name
            global api_installation
            global api_download_link

            api_server_name = 'PostgreSQL'
            api_download_link = '<font color=blue>apt-get install python-psycopg2</font>'
            api_reference = '<font color=blue>http://wiki.python.org/moin/PostgreSQL</font>'
            api_installation = ''

            run_api_dialog = api_install_link()
            run_api_dialog.exec_()



    def mssql_settings(self):
        ''' accepts connection settings and then
            attempt database connection for MySQL
        '''
        variables.database_type = 'MSSQL'
        variables.username = str(self.username_linedit.text())
        variables.password = str(self.password_linedit.text())

        if mssql_install_status != 'Not Installed':
            variables.server_name_label = 'Microsoft SQL Server:'
            variables.server_port_check_label = 'MS-SQL Port:'
            variables.server_settings_title = 'Microsoft SQL Server Connection Settings'
            variables.default_server_port_label = '( Default MS-SQL port is 1433 TCP )'
            variables.server_logo = '%s/Icons/sql-server-2008-logo.ico'%(os.getcwd())

            if variables.username == '':
                QtGui.QMessageBox.warning(self,"Username error","Please Input a username and press the lock button to enable Generic database mode")
                self.username_linedit.setFocus()
            elif self.login_button.isChecked() == False:
                QtGui.QMessageBox.warning(self,"Lock Button","Please press the Lock Button to enable Generic database mode")
                self.login_button.setFocus()
            elif variables.database_mssql_status == 'connected':
                self.database_interaction()
            else:
                run_settings_dialog = connection.connection_setting_dialog()
                run_settings_dialog.exec_()

        else:
            global api_reference
            global api_server_name
            global api_installation
            global api_download_link

            api_server_name = 'MSSQl'
            api_download_link = '<font color=blue>apt-get install python-pymssql</font>'
            api_reference = '<font color=blue>http://wiki.python.org/moin/SQL Server</font>'
            api_installation = ''

            run_api_dialog = api_install_link()
            run_api_dialog.exec_()



    def sqlite_settings(self):
        ''' Run the connections dialog in respects
            to sqlite
        '''

        variables.database_type = 'SQLITE'
        variables.server_connection = 'localhost'
        self.database_interaction()




#######################################################3###
#                                                         #
#                DATABASE INTERACTION                     #
#                                                         #
##########################################################

class database_interaction_dialog(QtGui.QDialog,interaction_dialog):
    ''' This GUI class provides the interaction window for the
        databases
    '''
    global database_server_port
    global postgres_server_connection

    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.setupUi(self)
        self.retranslateUi(self)
        self.lineEdit.setEnabled(False)         # Disable the Linedit, for only SQLITE would be using that object
        self.interact_browse.setEnabled(False)  # Disable the Browse button,for only SQLITE would be using that object
        self.interact_comboBox.setEnabled(True)
        self.sqleditor.setEnabled(True)
        self.tables_button.setEnabled(True)
        self.save_report_button.setEnabled(False)
        self.close_interact_button.setEnabled(True)
        self.execute_sql_button.setEnabled(True)
        sql_code = Qsci.QsciLexerSQL()
        self.sqleditor.setLexer(sql_code)

        try:
            self.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCancelButtonHint | QtCore.Qt.WindowCloseButtonHint)
        except:pass
        self.sqleditor.setFocus()
        self.setWindowTitle("%s Database Interaction"%(variables.database_type))
        self.connect(self.execute_sql_button,QtCore.SIGNAL("clicked()"),self.browse_sql_script)
        self.connect(self.close_interact_button,QtCore.SIGNAL("clicked()"),self.close_database)
        self.connect(self.tables_button,QtCore.SIGNAL("clicked()"),self.show_tables)
        self.connect(self.interact_browse,QtCore.SIGNAL("clicked()"),self.connect_sqlite_database)
        self.connect(self.save_report_button,QtCore.SIGNAL("clicked()"),self.save_report)

        if variables.database_type == 'MySQL':

            database_list = []
            variables.database_mysql_query.execute('select version()')
            self.interact_server_name.setText('<font color=green>MySQL Server:</font>')
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.mysql_server_connection))
            variables.report_server_version = variables.database_mysql_query.fetchall()[0][0]
            self.label_4.setText('<font color=green>%s</font>'%(variables.report_server_version))

            variables.database_mysql_query.execute('show databases;')
            data = variables.database_mysql_query.fetchall()
            for iterate in data:
                database_list.append(iterate[0])
            self.interact_comboBox.addItems(database_list)


        elif variables.database_type == 'Oracle':

            database_list = [variables.username.upper()]
            variables.database_oracle_query.execute('select * from v$version')
            temp_data = variables.database_oracle_query.fetchall()
            self.interact_server_name.setText('<font color=green>%s</font>'%(temp_data[0][0]))
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.oracle_server_connection))
            variables.report_server_version = temp_data[3][0]
            self.label_4.setText('<font color=green>%s</font>'%(variables.report_server_version))
            variables.database_oracle_query.execute("""SELECT username FROM all_users ORDER BY username""")
            data = variables.database_oracle_query.fetchall()
            for iterate in data:
                if variables.username.upper() != str(iterate):
                    database_list.append(iterate[0])
            self.interact_comboBox.addItems(database_list)


        elif variables.database_type == 'PostgreSQL':
            variables.database_postgresql_query = variables.database_postgresql.cursor()
            database_list = []
            variables.database_postgresql_query.execute('SELECT version()')
            temp_data = variables.database_postgresql_query.fetchall()[0][0]
            server_edition = temp_data.index(',')
            self.interact_server_name.setText('<font color=green>%s:</font>'%(temp_data[0:server_edition]))
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.postgres_server_connection))
            variables.report_server_version = temp_data[server_edition +1:-1]
            self.label_4.setText('<font color=green>%s</font>'%(variables.report_server_version))
            variables.database_postgresql_query.execute('select * from pg_catalog.pg_database')
            data = variables.database_postgresql_query.fetchall()
            for iterate in data:
                database_list.append(iterate[0])
            self.interact_comboBox.addItems(database_list)



        elif variables.database_type == 'MSSQL':

            database_list = []
            variables.database_mssql_query.execute("SELECT SERVERPROPERTY('productversion'), SERVERPROPERTY ('productlevel'), SERVERPROPERTY ('edition')")
            temp_data = variables.database_mssql_query.fetchall()
            self.interact_server_name.setText('<font color=green>%s %s</font>'%(temp_data[0][2],temp_data[0][1]))
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.mssql_server_connection))
            variables.report_server_version = temp_data[0][0]
            self.label_4.setText('<font color=green>%s</font>'%(variables.report_server_version))
            variables.database_mssql_query.execute('select * from sys.databases')
            data = variables.database_mssql_query.fetchall()
            for iterate in data:
                database_list.append(iterate[0])
            self.interact_comboBox.addItems(database_list)


        else:
            variables.report_server_type = "SQlite"
            self.interact_browse.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.interact_comboBox.setEnabled(False)
            self.sqleditor.setEnabled(False)
            self.tables_button.setEnabled(False)
            self.close_interact_button.setEnabled(False)
            self.execute_sql_button.setEnabled(False)
            variables.report_server_version = ""
            self.interact_server_name.setText('<font color=green>SQLite: None Selected</font>')
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.server_connection))
            self.label_4.setText('<font color=green>None Selected</font>')


    def save_report(self):
        import random
        number = random.randint(34,80)

        variables.report_query_string = str(self.sqleditor.text())
        variables.report_raw_data = self.response_table
        variables.report_database = str(self.interact_comboBox.currentText())
        variables.report_server_type = variables.database_type

        variables.report_save_path = QtGui.QFileDialog.getSaveFileName(self,"Save Reports","hexorbase-report-%s"%(number),"HTML(*.html)")

        if variables.report_save_path:
            if not variables.report_database_ip_address:
                variables.report_database_ip_address = None
            if not variables.report_database_ip_adress_port:
                variables.report_database_ip_adress_port = None
            if not variables.report_server_type:
                variables.report_server_type = None
            if not variables.report_server_version:
                variables.report_server_version = None
            if not variables.report_database:
                variables.report_database = None
            if not variables.report_query_string:
                variables.report_query_string = None


            variables.report_html = variables.report_template % (variables.report_database_ip_address,
                                                            variables.report_database_ip_adress_port,
                                                            variables.report_server_type,
                                                            variables.report_server_version,
                                                            variables.report_database,
                                                            str(variables.report_query_string))

            report_class = reports.report()
            report_class.exec_()


    def connect_sqlite_database(self):
        ''' Selects and cursors an sqlite database
            for connections
        '''
        import sqlite3
        global database_sqlite


        self.lineEdit.clear()
        self.sqleditor.clear()
        self.interact_textBrowser.clear()
        database_name = str(QtGui.QFileDialog.getOpenFileName(self,"Select SQlite Database",""))
        if database_name:
            database_sqlite = sqlite3.connect(database_name)
            variables.database_sqlite_query = database_sqlite.cursor()
            variables.database_sqlite_status = 'connected'
            self.lineEdit.setText(database_name)
            self.interact_browse.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.interact_comboBox.setEnabled(True)
            self.sqleditor.setEnabled(True)
            self.tables_button.setEnabled(True)
            self.close_interact_button.setEnabled(True)
            self.execute_sql_button.setEnabled(True)
            index_database_name = database_name.rindex('/')      # Index the last occurence of '/' for linux and '\' for windows
            database = str(database_name[index_database_name +1:len(database_name)])
            self.interact_comboBox.addItems([database])
            self.interact_server_name.setText('<font color=green>SQLite: %s</font>'%(database))
            self.label_4.setText('<font color=green>SQlite %s</font>'%(sqlite3.version))

        else:
            self.interact_browse.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.interact_comboBox.setEnabled(False)
            self.sqleditor.setEnabled(False)
            self.tables_button.setEnabled(False)
            self.close_interact_button.setEnabled(False)
            self.execute_sql_button.setEnabled(False)
            self.interact_server_name.setText('<font color=green>SQLite: None Selected</font>')
            self.interact_server_connection.setText('<font color=green>%s</font>'%(variables.server_connection))
            self.label_4.setText('<font color=green>None Selected</font>')



    def browse_sql_script(self):
        ''' Read the contents of the a selected SQL
            script and pastes content to input area
        '''
        try:
            sql_script = QtGui.QFileDialog.getOpenFileName(self,"Select SQL Script","","SQL Script(*.sql)")
            sql_script_open = open(sql_script,'r')
            self.sqleditor.clear()
            self.sqleditor.setText(sql_script_open.read())
            sql_script_open.close()
        except IOError:
            pass


    def show_tables(self):

        seleted_database = str(self.interact_comboBox.currentText())
        self.interact_textBrowser.clear()                           # Clear the browser before adding new results
        self.clear_table()

        if variables.database_type == 'MySQL':
            try:
                self.interact_textBrowser.append("<font color=blue>\n TABLES LIST FOR DATABASE: '%s'\n</font>"%(seleted_database))
                variables.database_mysql_query.execute('use `%s`;'%(seleted_database))
                variables.database_mysql_query.execute('show tables;')
                responce = variables.database_mysql_query.fetchall()

                table_list = []
                if len(responce) >= 1:
                    for iterate in responce:
                        table_list.append((str(iterate[0]),''))
                    variables.table_description = variables.database_mysql_query.description
                    self.save_report_button.setEnabled(True)
                    self.table_insert_data(variables.database_mysql_query.description,table_list)
                    self.response_table.removeColumn(1)
                else:
                    self.save_report_button.setEnabled(False)

            except Exception,e:
                self.interact_textBrowser.append('<font color=red>%s</font>'%(e))

        elif variables.database_type == 'Oracle':
            try:
                self.interact_textBrowser.append("<font color=blue>\n TABLES LIST FOR DATABASE: '%s'\n</font>"%(seleted_database))
                variables.database_oracle_query.execute("SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = '%s'"%(seleted_database))
                responce = variables.database_oracle_query.fetchall()

                table_list = []
                if len(responce) >= 1:
                    for iterate in responce:
                        table_list.append((str(iterate[0]),''))
                    variables.table_description = variables.database_oracle_query.description
                    self.save_report_button.setEnabled(True)
                    self.table_insert_data(variables.database_oracle_query.description,table_list)
                    self.response_table.removeColumn(1)
                else:
                    self.save_report_button.setEnabled(False)

            except Exception,e:
                self.interact_textBrowser.append('<font color=red>%s</font>'%(e))


        elif variables.database_type == 'PostgreSQL':
            try:
                self.interact_textBrowser.append("<font color=blue>\n TABLES LIST FOR USER: '%s'\n</font>"%(variables.username))
                variables.database_postgresql_query.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                responce = variables.database_postgresql_query.fetchall()

                table_list = []
                if len(responce) >= 1:
                    for iterate in responce:
                        table_list.append((str(iterate[0]),''))
                    variables.table_description = variables.database_postgresql_query.description
                    self.save_report_button.setEnabled(True)
                    self.table_insert_data(variables.database_postgresql_query.description,table_list)
                    self.response_table.removeColumn(1)
                else:
                    self.save_report_button.setEnabled(False)


            except Exception,e:
                self.interact_textBrowser.append('<font color=red>%s</font>'%(e))


        elif variables.database_type == 'MSSQL':
            try:
                self.interact_textBrowser.append("<font color=blue>\n TABLES LIST FOR DATABASE: '%s'\n</font>"%(seleted_database))
                variables.database_mssql_query.execute('use %s \nselect name from sys.tables'%(seleted_database))
                responce = variables.database_mssql_query.fetchall()

                table_list = []
                if len(responce) >= 1:
                    for iterate in responce:
                        table_list.append((str(iterate[0]),''))
                    variables.table_description = variables.database_mssql_query.description
                    self.save_report_button.setEnabled(True)
                    self.table_insert_data(variables.database_mssql_query.description,table_list)
                    self.response_table.removeColumn(1)
                else:
                    self.save_report_button.setEnabled(False)

            except Exception,e:
                self.interact_textBrowser.append('<font color=red>%s</font>'%(e))

        else:
            try:
                self.interact_textBrowser.append("<font color=blue>\n TABLES LIST FOR DATABASE: '%s'\n</font>"%(seleted_database))
                variables.database_sqlite_query.execute('select tbl_name from sqlite_master')
                responce = variables.database_sqlite_query.fetchall()

                if len(responce) >= 1:
                    variables.table_description = variables.database_sqlite_query.description
                    self.save_report_button.setEnabled(True)
                    self.table_insert_data(variables.database_sqlite_query.description,responce)
                else:
                    self.save_report_button.setEnabled(False)

            except Exception,e:
                self.interact_textBrowser.append('<font color=red>%s</font>'%(e))


    def clear_table(self):
        row_number = self.response_table.rowCount()
        column_number = self.response_table.columnCount()

        for row in xrange(row_number):
            self.response_table.removeRow(0)

        for column in xrange(column_number):
            self.response_table.removeColumn(0)



    def table_insert_data(self,col_data,row_data):
        '''function accepts raw data output from server and
           then inputs list of data items to the GUI table
        '''
        row_number = self.response_table.rowCount()
        column_number = self.response_table.columnCount()

        column_data = []
        for data in col_data:
            column_data.append(data[0])

        for row in xrange(row_number):
            self.response_table.removeRow(0)

        for column in xrange(column_number):
            self.response_table.removeColumn(0)

        for column in xrange(len(column_data)):
            self.response_table.insertColumn(column)
            column_header = QtGui.QTableWidgetItem()
            self.response_table.setHorizontalHeaderItem(column,column_header)
            self.response_table.horizontalHeaderItem(column).setText(column_data[column] + ' '* 5)
            self.response_table.resizeRowsToContents()

        for row in xrange(len(row_data)):
            self.response_table.insertRow(row)
            data_ = row_data[row]
            for row_number in xrange(len(column_data)):
                item = QtGui.QTableWidgetItem()
                self.response_table.setItem(row,row_number,item)
                item.setText(str(data_[row_number]) + ' ' * 5)
                self.response_table.resizeColumnsToContents()





    def keyPressEvent(self,event):
        ''' This function executes SQL statements
            on the press of the F5 button
        '''
        if event.key() == QtCore.Qt.Key_F5:
            sql_statements = str(self.sqleditor.text())
            self.interact_textBrowser.clear()
            self.clear_table()

            iterable_data = ["list","tuple"]

            if variables.database_type == 'MySQL':
                try:
                    variables.database_mysql_query = variables.database_mysql.cursor()
                    variables.database_mysql_query.execute('''%s'''%(sql_statements))
                    server_output = variables.database_mysql_query.fetchall()

                    if str(type(server_output).__name__) in iterable_data:
                        if len(server_output) >= 1:
                            variables.table_description = variables.database_mysql_query.description
                            self.table_insert_data(variables.table_description,server_output)

                    if len(server_output) > 0:
                        self.interact_textBrowser.append('<font color=black>(%d row) </font>'%(len(server_output)))
                        self.save_report_button.setEnabled(True)
                    else:
                        self.save_report_button.setEnabled(False)

                    self.interact_textBrowser.append('<font color=black>Successfully executed query</font>')
                    variables.database_mysql.commit()
                except Exception,exception:
                    self.interact_textBrowser.append('<font color=red>%s</font>'%(exception))


            elif variables.database_type == 'Oracle':
                try:
                    variables.database_oracle_query = variables.database_oracle.cursor()
                    variables.database_oracle_query.execute('''%s'''%(sql_statements))
                    server_output = variables.database_oracle_query.fetchall()
                    variables.database_oracle.commit()

                    if str(type(server_output).__name__) in iterable_data:
                        if len(server_output) >= 1:
                            variables.table_description = variables.database_oracle_query.description
                            self.table_insert_data(variables.table_description,server_output)

                    if len(server_output) > 0:
                        self.interact_textBrowser.append('<font color=black>(%d row) </font>'%(len(server_output)))
                        self.save_report_button.setEnabled(True)
                    else:
                        self.save_report_button.setEnabled(False)

                    self.interact_textBrowser.append('<font color=black>Successfully executed query</font>')
                    variables.database_oracle.commit()
                except Exception,exception:
                    self.interact_textBrowser.append('<font color=red>%s</font>'%(exception))

            elif variables.database_type == 'PostgreSQL':
                try:
                    import psycopg2
                    variables.database_postgresql = psycopg2.connect(user = variables.username,host = variables.postgres_server_connection,password = variables.password,port = str(variables.report_database_ip_adress_port))
                    variables.database_postgresql_query = variables.database_postgresql.cursor()
                    variables.database_postgresql_query.execute('%s'%(sql_statements))
                    server_output = variables.database_postgresql_query.fetchall()

                    if str(type(server_output).__name__) in iterable_data:
                        if len(server_output) >= 1:
                            variables.table_description = variables.database_postgresql_query.description
                            self.table_insert_data(variables.table_description,server_output)

                    if len(server_output) > 0:
                        self.interact_textBrowser.append('<font color=black>(%d row) </font>'%(len(server_output)))
                        self.save_report_button.setEnabled(True)
                    else:
                        self.save_report_button.setEnabled(False)

                    self.interact_textBrowser.append('<font color=black>Successfully executed query</font>')
                    variables.database_postgresql.commit()
                except Exception,exception:
                    self.interact_textBrowser.append('<font color=red>%s</font>'%(exception))


            elif variables.database_type == 'MSSQL':
                try:
                    variables.database_mssql_query.execute("""%s"""%(sql_statements))
                    server_output = variables.database_mssql_query.fetchall()

                    if str(type(server_output).__name__) in iterable_data:
                        if len(server_output) >= 1:
                            variables.table_description = variables.database_mssql_query.description
                            self.table_insert_data(variables.table_description,server_output)

                    if len(server_output) > 0:
                        self.interact_textBrowser.append('<font color=black>(%d row) </font>'%(len(server_output)))
                        self.save_report_button.setEnabled(True)
                    else:
                        self.save_report_button.setEnabled(False)

                    self.interact_textBrowser.append('<font color=black>Successfully executed query</font>')
                except Exception,exception:
                    self.interact_textBrowser.append('<font color=red>%s</font>'%(exception))

            else:
                try:
                    variables.database_sqlite_query.execute('''%s'''%(sql_statements))
                    server_output = variables.database_sqlite_query.fetchall()

                    if str(type(server_output).__name__) in iterable_data:
                        if len(server_output) >= 1:
                            variables.table_description = variables.database_sqlite_query.description
                            self.table_insert_data(variables.table_description,server_output)

                    if len(server_output) > 0:
                        self.interact_textBrowser.append('<font color=black>(%d row) </font>'%(len(server_output)))
                        self.save_report_button.setEnabled(True)
                    else:
                        self.save_report_button.setEnabled(False)

                    self.interact_textBrowser.append('<font color=black>Successfully executed query</font>')
                    database_sqlite.commit()
                except Exception,exception:
                    self.interact_textBrowser.append('<font color=red>%s</font>'%(exception))




    def close_database(self):
        ''' Close the database connections according
            to which of them is currently selected
        '''
        global database_sqlite

        if variables.database_type == 'MySQL':
            import MySQLdb
            variables.database_mysql_status = 'not connected'
            variables.database_mysql.close()
            variables.oracle_status.setText("<font color=green>MySQLdb version: %s.%s.%s %s</font>"%\
                                       (MySQLdb.version_info[0],MySQLdb.version_info[1],MySQLdb.version_info[2],MySQLdb.version_info[3],))

        elif variables.database_type == 'Oracle':
            import cx_Oracle
            variables.database_oracle_status = 'not connected'
            variables.database_oracle.close()
            variables.mysql_status.setText("<font color=green>cx_Oracle version: %s</font>"%(cx_Oracle.version))

        elif variables.database_type == 'PostgreSQL':
            variables.database_postgresql_status = 'not connected'
            variables.database_postgresql.close()
            variables.sql_status.setText("<font color=green>Psycopg 2.3.2</font>")

        elif variables.database_type == 'MSSQL':
            import pymssql
            variables.database_mssql_status = 'not connected'
            variables.database_mssql .close()
            variables.sqlite_label.setText("<font color=green>Pymssql %s</font>"%(pymssql.__version__))

        else:
            import sqlite3
            variables.database_sqlite_status = 'not connected'
            database_sqlite.close()
            self.label_4.setText('<font color=green>SQlite %s</font>'%(sqlite3.version))

        self.close()




#########################################################
#             BRUTEFORCE DIALOG CLASS                   #
#########################################################





class api_install_link(QtGui.QDialog,api_install_reference):
    ''' This class defines the GUI object responsible for
        displaying to the user, the promt to install the
        api drivers
    '''
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.setupUi(self)
        self.retranslateUi(self)

        self.label_3.setText("%s"%(api_download_link))
        self.label_4.setText("Reference from pythons wiki page:")
        self.label_5.setText("%s"%(api_reference))
        self.label_6.setText("Windows API Drivers could be downloaded from the above python referenced page")
        self.label_7.setText("%s"%(api_installation))
        self.label.setText("The API(Application Programming Interface) Driver for %s is currently not installed, to install please download "%(api_server_name))





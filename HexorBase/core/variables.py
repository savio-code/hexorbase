# COnnection Setttings Strings
server_logo = ""
database_type = ""
server_name_label = ""
server_connection = ""
server_settings_title = ""
server_port_check_label = ""
default_server_port_label = ""

# GUI Object Strings
sqlite_label = ""
oracle_status = ""
mysql_status = ""
sql_status = ""
postgresql_label = ""

# Credential Strings
username = ""
password = ""
username_linedit = None
password_linedit = None

# Live Connection Object
database_mysql = None
database_mssql = None
database_oracle = None
database_postgresql = None

# Cursor Objects
database_mssql_query = None
database_mysql_query = None
database_oracle_query = None
database_sqlite_query = None
database_postgresql_query = None


# Connection Execution Status
database_mysql_status = 'not connected'
database_oracle_status = 'not connected'
database_postgresql_status = 'not connected'
database_mssql_status = 'not connected'
database_sqlite_status = 'not connected'

# Ip addresses
mysql_server_connection = ""
oracle_server_connection = ""
postgres_server_connection = ""
mssql_server_connection = ""


# Reports objects and variables
report_save_path = ""
report_database_ip_address = server_connection
report_database_ip_adress_port = ""
report_server_type = database_type
report_server_version = ""
table_description = None
report_query_string = None
report_database = None
report_raw_data = None
report_html = ""

report_template = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<style type="text/css">
.df {
	text-align: center;
}
.wqqw {
	text-align: center;
}
.ssdsw {
	font-weight: bold;
}
.wwew {
	text-align: left;
}
.wwew {
	font-weight: bold;
}
.wew {
	font-weight: normal;
}
.ass {
	text-align: center;
}
.middle {
	text-align: center;
}
.rtrtrt {
	font-size: 9px;
}
.wewew {
	font-size: 12px;
}
.middle .wewew strong {
	font-size: 15px;
}
.er {
	text-align: center;
}
italics {
	font-style: italic;
}
iterlics {
	font-style: italic;
}
.middle .wewew strong {
	text-align: left;
}
wew32 {
	text-align: left;
}
.wewew strong {
	font-size: 16px;
}
.small {
	font-size: 14px;
}
.middle {
	text-align: center;
}
</style>
</head>

<body>
<h1 class="df">HexorBase
</h1>
<p class="ass">Report</p>
<p class="ssdsw">Host Details</p>
<hr />
<p><strong>Hostname:&nbsp;</strong>%s&nbsp;<strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Host Port: &nbsp;</strong>%s<strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Server Type:&nbsp;</strong>%s</font><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Server Version:&nbsp;</strong>%s</p>
<p><strong>Database:&nbsp;</strong>%s</p>
<p>&nbsp;</p>
<p><span class="ssdsw">SQL Query</span></p>
<hr />
<p>%s</p>
<p>&nbsp;</p>
<p><span class="ssdsw">Query Results</span></p>
<hr />
    <table width="1007" border="0">
  <tr class="er">
    <td width="302"></td>
    <td width="232"></td>
    <td width="247"></td>
    <td width="175"></td>
  </tr>
'''




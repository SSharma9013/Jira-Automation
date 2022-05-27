import pyodbc
server = '10.64.143.202'
database = 'PSIMPM'
username = 'qa_auto'
password = 'Presensoft0'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
query_string = "SELECT top 10 * FROM ConversationLogActual"
cursor = cnxn.cursor()
query = cursor.execute(query_string)
row = query.fetchone()
print("Row return: %s" % row)
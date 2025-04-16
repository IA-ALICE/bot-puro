import pyodbc

#------------------------------------------------SECCION DEL LA DASE DE DATOS--------------------------------------------
def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-LRGLGH6;'
        'DATABASE=BDAJYP4;'  
        'Trusted_Connection=yes;'
    )
    return connection
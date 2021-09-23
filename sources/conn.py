# import pyodbc 

# def tryGetSP(serverName ,solutionName):
#     sp = 0
#     try:
#         conn = pyodbc.connect('Driver={SQL Server};'
#                             f'Server={serverName};'
#                             f'Database=BitMobile_express_{solutionName};'
#                             'Trusted_Connection=yes;')

#         cursor = conn.cursor()
#         cursor.execute(f'SELECT [Value] FROM [BitMobile_express_{s_name}].[dbo].[dbConfig] where [Key] = \'bitmobilePass\'')        
#         for row in cursor:
#             sp=row.Value        
#     except:
#         print("db error")
#     finally:
#         return sp
 

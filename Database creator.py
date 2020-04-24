import sqlite3

DbConnect = sqlite3.connect("LoginDataBase.db")
c = DbConnect.cursor()
####c.execute("""CREATE TABLE if NOT EXISTS LoginDataBaseTable
####('User_Number'INTEGER PRIMARY KEY NOT NULL, 'Username' STRING, 'Password' STRING)""")

##c.execute("INSERT INTO LoginDataBaseTable (Username, Password) VALUES (?,?)", ["Patrick","bruh"])
##c.execute("INSERT INTO LoginDataBaseTable (Username, Password) VALUES (?,?)", ["Joseph","123Pass"])
##c.execute("INSERT INTO LoginDataBaseTable (Username, Password) VALUES (?,?)", ["HAEC-School","Password10"])
##c.execute("INSERT INTO LoginDataBaseTable (Username, Password) VALUES (?,?)", ["Alexis","NotFunny"])

c.execute("""CREATE TABLE if NOT EXISTS BankAccountDataTable
    ('User_Number' INTEGER PRIMARY KEY NOT NULL, 'Username' STRING, 'Account_Balance_Current' REAL, 'Interest_Generated' REAL)""")
          
c.execute("INSERT INTO BankAccountDataTable (Username, Account_Balance_Current) VALUES (?,?)", ["Patrick", 456000])
c.execute("INSERT INTO BankAccountDataTable (Username, Account_Balance_Current) VALUES (?,?)", ["Joesph", 120000])
c.execute("INSERT INTO BankAccountDataTable (Username, Account_Balance_Current, Interest_Generated) VALUES (?,?,?)", ["HAEC-School", 46700])
c.execute("INSERT INTO BankAccountDataTable (Username, Account_Balance_Current) VALUES (?,?)", ["Alexis", 76432])

DbConnect.commit()
DbConnect.close()





import sqlite3
import tkinter
import random
from functools import partial

def Startup():
    window = tkinter.Tk()
    window.title("Banking Program Login")
    window.geometry("400x150") 
    label = tkinter.Label(window, text = "Welcome to the Banking Program.").pack()
    username_label = tkinter.Label(window, text = "Enter Username below").pack()
    username_entrybox = tkinter.Entry(window)
    username_entrybox.pack()
    password_label = tkinter.Label(window, text = "Enter Password below").pack()
    password_entrybox = tkinter.Entry(window, show = "*")
    password_entrybox.pack()

    def SignupWindowFunc():
        window.destroy()
        sw = tkinter.Tk()
        sw.title("Signup Window")
        sw.geometry("400x150")
        swLabel = tkinter.Label(sw, text = "Welcome to the signup page!").pack()
        sw_username_label = tkinter.Label(sw, text = "Enter Username below").pack()
        sw_username_entrybox = tkinter.Entry(sw, show = "*")
        sw_username_entrybox.pack()
        sw_password_label = tkinter.Label(sw, text = "Enter Password Below").pack()
        sw_password_entrybox = tkinter.Entry(sw)
        sw_password_entrybox.pack()

        def TryCreateUser(str_newusername, str_newpassword):
            try:
                with sqlite3.connect('LoginDataBase.db') as DbConnect:
                    c = DbConnect.cursor()
                    c.execute("INSERT INTO LoginDataBaseTable (Username, Password) VALUES (?, ?)", [str_newusername, str_newpassword])
                    c.execute("INSERT INTO BankAccountDataTable (Username, Account_Balance_Current, Interest_Generated) VALUES (?,?,?)", [str_newusername, 0, 0])
                    DbConnect.commit()
                    sw.destroy()
                    Startup()
                    
            except sqlite3.Error as e:
                sw_username_taken_label = tkinter.Label(sw, text = "This username was taken, please try another one.").pack()
                DbConnect.close()

        def sw_GetEntries():
            str_newusername = sw_username_entrybox.get()
            str_newpassword = sw_password_entrybox.get()
            TryCreateUser(str_newusername, str_newpassword)

        sw_okButton = tkinter.Button(sw, command = sw_GetEntries, text = "OK!").pack()
        sw.mainloop()

    def GetVariablesForSetup():
        global var_current_account_balance
        global var_current_account_generated_interest 
        with sqlite3.connect('LoginDataBase.db') as DbConnect:
            c = DbConnect.cursor()
            var_select = []
            var_select.append(var_UID)
            var_select.append(var_current_user_username)
            sql = 'SELECT * FROM BankAccountDataTable WHERE User_Number = ? AND Username = ?';
            c.execute(sql, var_select)
            result = c.fetchall()
            print(result)                
            for row in result:
                var_current_account_balance = float(row[2])
                print(var_current_account_balance)
                var_current_account_generated_interest = float(row[3])        
                    
    def moveOn():
        global var_current_account_balance
        global var_current_account_generated_interest
        window.destroy()
        window2 = tkinter.Tk()
        window2.title("Banking Program")
        window2.geometry("960x540")

        GetVariablesForSetup()
        print(var_current_account_generated_interest)
        var_current_account_balance_interest_added = round((var_current_account_balance * 1.002), 2)
        var_current_account_generated_interest = var_current_account_generated_interest + (var_current_account_balance_interest_added - var_current_account_balance)
        logged_in_message = "You are logged in as: {}          Your UID is {}".format(var_current_user_username, var_UID)
        balance_message = "Your Current Balance is: £{}".format(var_current_account_balance_interest_added)
        interest_message = "Your Current Generated interest is: £{}         (Interest is generated every time you run the program and successfully log in.)".format(round(var_current_account_generated_interest, 2))

        with sqlite3.connect('LoginDataBase.db') as DbConnect:
            c = DbConnect.cursor()
            sql_update_statement = "UPDATE BankAccountDataTable SET Account_Balance_Current = ?, Interest_Generated = ? WHERE User_Number = ? AND Username= ?"
            Values = (var_current_account_balance_interest_added, var_current_account_generated_interest, var_UID, var_current_user_username)
            c.execute(sql_update_statement, Values)
            DbConnect.commit()
            
        print(balance_message)
        username_label = tkinter.Label(window2, text = logged_in_message).pack() 
        balance_label = tkinter.Label(window2, text = balance_message).pack()
        interest_label = tkinter.Label(window2, text = interest_message).pack()

        space_label = tkinter.Label(window2).pack()
        enter_user_for_transaction_label = tkinter.Label(window2, text = "Please Enter A User For Transaction to, in format UID_NAME").pack()
        enter_user_for_transaction_entrybox = tkinter.Entry(window2)
        enter_user_for_transaction_entrybox.pack()
        enter_ammount_to_exchange_label = tkinter.Label(window2, text = "Please enter the ammount in £ you would like to transfer (Enter only a number)").pack()
        enter_ammount_to_exchange_entrybox = tkinter.Entry(window2)
        enter_ammount_to_exchange_entrybox.pack()

        def PayUser(tempvar_UID ,account, ammount):
            print(account)
            print(tempvar_UID)
            print(var_current_user_username)
            print(ammount)

        
        
        def FailWindowFunc():
            failwindow = tkinter.Tk()
            failwindow.title("User Does Not Exist!")
            failwindow.geometry("400x150")
            fail_window_label = tkinter.Label(failwindow, text ="That user does not exist!").pack()
            fail_space_label = tkinter.Label(failwindow).pack()
            fail_space_label2 = tkinter.Label(failwindow).pack()
            fail_space_label3 = tkinter.Label(failwindow).pack()
            fail_window_label_exit = tkinter.Label(failwindow, text = "Please press OK to exit this window").pack()
            def DestroyFailWindow():
                failwindow.destroy()
            
            fail_ok_button = tkinter.Button(failwindow, command = DestroyFailWindow, text = "OK!")
            fail_ok_button.pack()

            failwindow.mainloop()
            

        def CheckUserExists(var_UID2, var_Username):
            with sqlite3.connect('LoginDataBase.db') as DbConnect:
                c = DbConnect.cursor()
                var_select = []
                var_select.append(var_UID2)
                var_select.append(var_Username)
                sql = 'SELECT * FROM LoginDataBaseTable WHERE User_Number = ? AND Username = ?';
                c.execute(sql, var_select)
                result = c.fetchall()
                if(len(result) != 0):
                    print("Yay!")
                else:
                    FailWindowFunc()

        def GetInfo():
            recieving_account = enter_user_for_transaction_entrybox.get()
            recieving_account_UID = 2
            recieving_account_parsed_name = recieving_account
            money_to_transfer = float(enter_ammount_to_exchange_entrybox.get())
            print("tester")
            CheckUserExists(recieving_account_UID, recieving_account)
            PayUser(recieving_account_UID, recieving_account_parsed_name, money_to_transfer)

        pay_user_button = tkinter.Button(window2, command = GetInfo, text = "Pay User")
        pay_user_button.pack()

        window2.mainloop()
 
    def Login(username_string, password_string):
        var_select = []
        var_select.append(username_string)
        var_select.append(password_string)
        with sqlite3.connect('LoginDataBase.db') as DbConnect:
            c = DbConnect.cursor()
            sql = 'SELECT * FROM LoginDataBaseTable WHERE Username = ? AND Password = ?';
            c.execute(sql, var_select)
            result = c.fetchall()
            print(result)
            for row in result:
                global var_UID
                global var_current_user_username
                var_current_user_username = str(row[1])
                var_UID = int(row[0])
                print(var_UID)
            if(len(result) != 0):
                moveOn()
            else:
                fail_Label = tkinter.Label(window, text = "That was an invalid login, try again").pack()
                username_entrybox.delete(0, "end")
                password_entrybox.delete(0, "end")      

    def GetEntries():
        username_string = username_entrybox.get()
        password_string = password_entrybox.get()
        print(username_string, password_string)
        Login(username_string, password_string)
        
    ok_button = tkinter.Button(window, command = GetEntries, text = "OK!").pack()
    signup_button = tkinter.Button(window, command = SignupWindowFunc, text = "Sign up!")
    signup_button.pack()
    window.mainloop()

Startup()
print("The program ran successfully, at least to this point")
print("The program will exit now")





import sqlite3
import tkinter
import math
import datetime

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

    def FailWindowFunc(error_message):
            failwindow = tkinter.Tk()
            failwindow.title(error_message)
            failwindow.geometry("400x150")
            message_to_display = error_message
            fail_window_label = tkinter.Label(failwindow, text = error_message).pack()
            fail_space_label = tkinter.Label(failwindow).pack()
            fail_space_label2 = tkinter.Label(failwindow).pack()
            fail_space_label3 = tkinter.Label(failwindow).pack()
            fail_window_label_exit = tkinter.Label(failwindow, text = "Please press OK to exit this window").pack()
            def DestroyFailWindow():
                failwindow.destroy()
            
            fail_ok_button = tkinter.Button(failwindow, command = DestroyFailWindow, text = "OK!")
            fail_ok_button.pack()

            failwindow.mainloop()
            
    def SignupWindowFunc():
        window.destroy()
        sw = tkinter.Tk()
        sw.title("Signup Window")
        sw.geometry("400x150")
        swLabel = tkinter.Label(sw, text = "Welcome to the signup page!").pack()
        sw_username_label = tkinter.Label(sw, text = "Enter Username below").pack()
        sw_username_entrybox = tkinter.Entry(sw)
        sw_username_entrybox.pack()
        sw_password_label = tkinter.Label(sw, text = "Enter Password Below").pack()
        sw_password_entrybox = tkinter.Entry(sw, show = "*")
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
                sw_username_entrybox.delete(0, "end")
                sw_password_entrybox.delete(0, "end")               

        def sw_GetEntries():
            str_newusername = sw_username_entrybox.get()
            str_newpassword = sw_password_entrybox.get()

            if(str_newusername.find("_") != -1):
                 print("Found!")
                 FailWindowFunc("Name Contained Illegal Character '_'")
                 
            else:
                if(str_newusername == "" or str_newpassword == ""):
                    FailWindowFunc("Must have both username and password")
                else:
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

    def round_down(n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier
                    
    def moveOn():
        global var_current_account_balance
        global var_current_account_balance_interest_added
        global var_current_account_generated_interest
        global balance_message
        
        window.destroy()
        window2 = tkinter.Tk()
        window2.title("Banking Program")
        window2.geometry("960x540")

        GetVariablesForSetup()
        print(var_current_account_generated_interest)
        var_current_account_balance_interest_added = round_down((var_current_account_balance * 1.002), 2)
        var_current_account_generated_interest = round_down(var_current_account_generated_interest + (var_current_account_balance_interest_added - var_current_account_balance), 2)
        logged_in_message = "You are logged in as: {}          Your UID is {}".format(var_current_user_username, var_UID)
        balance_message_label_text = tkinter.StringVar()
        
        balance_message = "Your Current Balance is: £{}".format(var_current_account_balance_interest_added)
        balance_message_label_text.set(balance_message)
        interest_message = "Your Current Generated interest is: £{}         (Interest is generated every time you run the program and successfully log in.)".format(round_down(var_current_account_generated_interest, 2))

        with sqlite3.connect('LoginDataBase.db') as DbConnect:
            c = DbConnect.cursor()
            sql_update_statement = "UPDATE BankAccountDataTable SET Account_Balance_Current = ?, Interest_Generated = ? WHERE User_Number = ? AND Username= ?"
            Values = (var_current_account_balance_interest_added, var_current_account_generated_interest, var_UID, var_current_user_username)
            c.execute(sql_update_statement, Values)
            DbConnect.commit()
            
        
        print(balance_message)
        username_label = tkinter.Label(window2, text = logged_in_message).pack() 
        balance_label = tkinter.Label(window2, textvariable = balance_message_label_text).pack()
        interest_label = tkinter.Label(window2, text = interest_message).pack()

        space_label = tkinter.Label(window2).pack()
        enter_user_for_transaction_label = tkinter.Label(window2, text = "Please Enter A User For Transaction to, in format [UID_NAME]").pack()
        enter_user_for_transaction_entrybox = tkinter.Entry(window2)
        enter_user_for_transaction_entrybox.pack()
        enter_ammount_to_exchange_label = tkinter.Label(window2, text = "Please enter the amount in £ you would like to transfer (Enter only a number)").pack()
        enter_ammount_to_exchange_entrybox = tkinter.Entry(window2)
        enter_ammount_to_exchange_entrybox.pack()
        
        def ShowHistory():
            def CountLines():
                i = 0
                with sqlite3.connect('LoginDataBase.db') as DbConnect:
                    c = DbConnect.cursor()
                    var_select = []
                    var_select.append(var_UID)
                    var_select.append(var_current_user_username)
                    var_select.append(var_UID)
                    var_select.append(var_current_user_username)
                    sql_statement_find_history = 'SELECT * FROM TransactionHistoryTable WHERE User_Number_1 = ? AND User_Name_1 = ? OR User_Number_2 = ? AND Username_2 = ?';
                    c.execute(sql_statement_find_history, var_select)
                    result_history = c.fetchall()
                    print(result_history)                
                    for row in result_history:
                        i = i + 1
                return i
            hw = tkinter.Tk()
            scrollbar = tkinter.Scrollbar(hw)
            hw.title("Transaction History")
            hw.geometry("960x540")
            number_of_lines = CountLines()
            hw_text_box = tkinter.Text(hw, height = number_of_lines, width = 120)
            scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            hw_text_box.pack(side=tkinter.LEFT, fill=tkinter.Y)
            scrollbar.config(command=hw_text_box.yview)
            hw_text_box.config(yscrollcommand=scrollbar.set)
            
            with sqlite3.connect('LoginDataBase.db') as DbConnect:
                    c = DbConnect.cursor()
                    var_select = []
                    var_select.append(var_UID)
                    var_select.append(var_current_user_username)
                    var_select.append(var_UID)
                    var_select.append(var_current_user_username)
                    sql_statement_find_history = 'SELECT * FROM TransactionHistoryTable WHERE User_Number_1 = ? AND User_Name_1 = ? OR User_Number_2 = ? AND Username_2 = ?';
                    c.execute(sql_statement_find_history, var_select)
                    result_history = c.fetchall()
                    print(result_history)                
                    for row in result_history:
                        str_message = "Date: {} || {} ---> {} || £{}\n".format(row[0], row[2], row[4], row[5])
                        hw_text_box.insert(tkinter.END, str_message)
            
        def RecordTransaction(UID, current_user, UID2, current_user_2, payment):
            date_not_clipped = str(datetime.datetime.now())
            date_clipped_array = date_not_clipped.split('.')
            date_clipped = date_clipped_array[0]
            print(date_clipped)
            with sqlite3.connect('LoginDataBase.db') as DbConnect:
                c = DbConnect.cursor()
                c.execute("INSERT INTO TransactionHistoryTable (Date, User_Number_1, User_Name_1, User_Number_2, Username_2, Payment_Amount) VALUES (?,?,?,?,?,?)", [date_clipped, UID, current_user, UID2, current_user_2, payment])
                DbConnect.commit()
            
            
        def PayUser(tempvar_UID ,account, ammount):
            global var_current_account_balance_interest_added
            global balance_message
            ammount = round_down(ammount,2)
            tempbalance = var_current_account_balance_interest_added - ammount

            if(tempbalance > 0):
                print("Enoguh money")
                second_user_balance = 0.0
                with sqlite3.connect('LoginDataBase.db') as DbConnect:
                    c = DbConnect.cursor()
                    var_select = []
                    var_select.append(tempvar_UID)
                    var_select.append(account)
                    sql_statement_get_second_user_balance = 'SELECT * FROM BankAccountDataTable WHERE User_Number = ? AND Username = ?';
                    c.execute(sql_statement_get_second_user_balance, var_select)
                    result = c.fetchall()
                    print(result)                
                    for row in result:
                        print("got here")
                        second_user_balance = float(row[2])  
                    second_user_balance = round_down(second_user_balance, 2)
                    print("Second User data " + str(second_user_balance))
                    second_user_balance = second_user_balance + ammount
                    var_current_account_balance_interest_added = tempbalance
                    var_current_account_balance_interest_added = round_down(var_current_account_balance_interest_added, 2)
                    sql_update_statement_transaction_give = "UPDATE BankAccountDataTable SET Account_Balance_Current = ? WHERE User_Number = ? AND Username = ?"
                    sql_update_statement_transaction_recieve = "UPDATE BankAccountDataTable SET Account_Balance_Current = ? WHERE User_Number = ? AND Username = ?"
                    Values2 = (var_current_account_balance_interest_added, var_UID, var_current_user_username)
                    Values3 = (second_user_balance, tempvar_UID, account)
                    c.execute(sql_update_statement_transaction_give, Values2)
                    c.execute(sql_update_statement_transaction_recieve, Values3)
                    balance_message = "Your Current Balance is: £{}".format(var_current_account_balance_interest_added)
                    DbConnect.commit()
                RecordTransaction(var_UID, var_current_user_username, tempvar_UID, account, ammount)
                    
                    
                    
            else:
                FailWindowFunc("Not enough money")
            

        def CheckUserExists(var_UID2, var_Username, money_to_transfer):
            with sqlite3.connect('LoginDataBase.db') as DbConnect:
                c = DbConnect.cursor()
                var_select = []
                var_select.append(var_UID2)
                var_select.append(var_Username)
                sql = 'SELECT * FROM BankAccountDataTable WHERE User_Number = ? AND Username = ?';
                c.execute(sql, var_select)
                result = c.fetchall()
                if(len(result) != 0):
                    PayUser(var_UID2, var_Username, money_to_transfer)
                else:
                    FailWindowFunc("User Does Not Exist!")

        def RefreshPage():
            global balance_message
            balance_message_label_text.set(balance_message)

        def GetInfo():
            recieving_account = enter_user_for_transaction_entrybox.get()
            parts_of_full_input = recieving_account.split('_')
            try:
                recieving_account_UID = int(parts_of_full_input[0])
                print(recieving_account_UID)
                recieving_account_parsed_name = parts_of_full_input[1]
                print(recieving_account_parsed_name)
                if(recieving_account_UID != var_UID):
                    try:
                        money_to_transfer = float(enter_ammount_to_exchange_entrybox.get())
                        if(money_to_transfer > 0):
                            CheckUserExists(recieving_account_UID, recieving_account_parsed_name, money_to_transfer)
                            RefreshPage()
                        else:
                            FailWindowFunc("The transfer amount was less than or equal to 0")
                    except ValueError as e:
                        FailWindowFunc("That was not a number")
                        #enter_ammount_to_exchange_entrybox.delete(0, "end")
                else:
                    FailWindowFunc("You cannot transfer money to yourself!")
            except ValueError as e:
                FailWindowFunc("That was not a valid username formatted 'UID_Username'!")
            

        pay_user_button = tkinter.Button(window2, command = GetInfo, text = "Pay User")
        pay_user_button.pack()
        space_label = tkinter.Label(window2).pack()
        check_history_transaction_label = tkinter.Label(window2, text = "Press History to View Past Transactions").pack()
        check_history_transaction_button = tkinter.Button(window2, command = ShowHistory, text = "History")
        check_history_transaction_button.pack()

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
                FailWindowFunc("Invalid Login Username or Password!")
                #username_entrybox.delete(0, "end")
                #password_entrybox.delete(0, "end")      

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





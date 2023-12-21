# importing libraries
import os 
import time as t

#importing modules 
import registration_module as rm
import transaction_module as tm
from login_module import login

    
def second_menu(acc_no,name):
    print("Hi ",name)
    print("1. Withdraw Money")
    print("2. Deposit Money")
    print("3. Mini Statement")
    print("4. Exit")
    choice_second = int(input("Choose any option....... \n"))
    match choice_second:
        case 1:
            tm.Withdraw(acc_no)
        case 2:
            tm.Deposit(acc_no)
        case 3:
            tm.Mini_statement(acc_no)
        case 4:
            exit("Thanks for using XYZ Bank")
        case default:
            print("You have chosen the wrong option....")
            second_menu(acc_no,name)


while True:
    os.system("cls")
    print("WELCOME".center(50,"*"))
    print("1. Registration")
    print("2. Login       ")
    choice_first = int(input("Choose Any Option : "))
    match choice_first:
        case 1:
            rm.registeration()
        case 2:
            result,acc_no,login_first_name = login()
            if result:
                second_menu(acc_no,login_first_name)
        case default:
            print("You have choosed the wrong option...")
            print("Please select the correct option")
            t.sleep(5)













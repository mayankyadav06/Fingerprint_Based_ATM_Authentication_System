import datetime
import os
import time
import mysql.connector 
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
import binary_processing_module as bmp

conn  = mysql.connector.connect(host='localhost', password=PUT_PASSWORD,user= 'root',database=DATABASE_NAME,autocommit=True)
connection_cursor = conn.cursor()

def insertBLOB(firstname,lastname,phone_no,accountnum,finger_impression,balance):
    try:
            connection_cursor = conn.cursor()
            current_time = datetime.datetime.now()
            sql_insert_blob_query = """ INSERT INTO ATM_database(first_name,last_name,Phone_no,Account_no,finger_print,Balance,Transaction,Amount,Date_Time,block_status,block_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            blob_finger_impression = bmp.convertToBinaryData(finger_impression)
            insert_blob_tuple = (firstname,lastname,phone_no,accountnum, blob_finger_impression,balance,"Credited",balance,current_time,"Unblocked",None)
            connection_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            print("your account has been successfully registered \nThanks for using XYZ Bank")
            exit()
    
    except mysql.connector.IntegrityError:
          print("Failed to register your account \nError : You have entered duplicate Account Number ",accountnum)
          exit("Try again with unique Account number")
    except mysql.connector.Error as error:
            print("Failed to register your account \nError : {} ".format(error))
            print("Please try again OR contact to the bank to register your account")
            exit()

def registeration():
    os.system("cls")
    print("Hey User \nWelcome To XYZ Bank")
    print("To register your account fill up the following details")
    time.sleep(2)
    os.system("cls")
    while True:
        first_name = input("Enter your first name : ")
        last_name = input("Enter your last name : ")
        phone_no = input("Enter your phone number : ")
        Account_no = input("Enter account number : ")
        Balance = input("Enter how much money do you want to deposit at registration state : ")
        print("Place your finger on scanner.......")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        finger_impression = askopenfilename()
        print("Successfully Scanned")
        if first_name.strip() and last_name.strip() and phone_no.strip() and Account_no.strip() and Balance.strip() and finger_impression.strip() != "":
              break
        else:
              print("You have entered empty field")
    insertBLOB(first_name,last_name,phone_no,Account_no,finger_impression,Balance)
    # exit()
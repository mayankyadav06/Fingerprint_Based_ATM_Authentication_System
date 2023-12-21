import datetime
from tkinter.filedialog import askopenfilename
import cv2
from tkinter import Tk
from twilio.rest import Client
import mysql.connector 
import binary_processing_module as bmp
from inputimeout import inputimeout


conn  = mysql.connector.connect(host='localhost', password=PUT_PASSWORD,user= 'root',database=DATABASE_NAME,autocommit=True)
connection_cursor = conn.cursor()


def second_authentication(acc_no,trial):    
            
    account_sid = " "
    auth_token = " "
    verify_sid = " "
    verified_number = " TWILIO_REGISTERED_PHONE_NUMBER"
    client = Client(account_sid, auth_token)

    client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")

    try:
        otp_code = inputimeout(prompt="Please enter the OTP:", timeout=13)
    except Exception:
        print('Your time is over!')
        print('You have not entered the OTP')
        trial += 1
        if trial < 2:
            print("You have only one try   ")
        elif trial == 2:
            block_status_sql_query = """update ATM_database set block_status = %s, block_Time = %s where Account_no = %s"""
            current_time = datetime.datetime.now()
            block_status_tuple = ("Blocked",current_time,acc_no)
            connection_cursor.execute(block_status_sql_query,block_status_tuple)
            print("You have entered empty OTP twice ")
            print("Your Account has been blocked... \nContact your nearby bank to unblock your account ")
            exit()
        checking_finger_print(acc_no,trial)

    try:
        verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
        if verification_check.status == "approved":
            return True
        else:
            raise Exception

    except Exception:
        print("You have enterd wrong OTP")
        trial += 1
        if trial < 2:
            print("Your account will be blocked after one more wrong trial ")
        elif trial == 2:
            block_status_sql_query = """update ATM_database set block_status = %s, block_Time = %s where Account_no = %s"""
            current_time = datetime.datetime.now()
            block_status_tuple = ("Blocked",current_time,acc_no)
            connection_cursor.execute(block_status_sql_query,block_status_tuple)
            print("You have entered wrong OTP twice \nYour Account has been blocked... ")
            print("Contact your nearby Bank to unblock your account ")
            exit()
        checking_finger_print(acc_no,trial)

    
    
def checking_finger_print(account_no,trial=0):
    search_finger_print_query = """select finger_print from ATM_database where Account_no = %s """
    connection_cursor.execute(search_finger_print_query,(account_no,))
    result_finegrprint = connection_cursor.fetchall()
    proper_finger_print_after_writing = bmp.write_file(result_finegrprint[0][0],str(account_no)+".jpeg")
    truth = True  
    try :
        print("Place your finger on scanner ........")
        Tk().withdraw()
        scanned_finger_impression = askopenfilename()
        # scanned_finger_impression = "E:/Dataset/SOCOFing/Real/1__M_Left_index_finger.BMP"
        sample = cv2.imread(scanned_finger_impression)

        best_score = 0
        filename = None
        image  = None
        kp1, kp2, mp = None,None,None
        fingerprint_image = cv2.imread(proper_finger_print_after_writing)

        sift = cv2.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)

        match_points = []

        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)

        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

        print("Fingerprint has been matched with score : " + str(best_score))
        result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)

        result = cv2.resize(result, None, fx=2, fy=2)
        cv2.imshow("result",result)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
        if best_score < 80 :
            print("Place Your finger properly \nTry again")
            checking_finger_print(account_no,trial)

    except :
        truth = False
        print("Wrong Fingerprint")
        print("Try again....")
        checking_finger_print(account_no,trial)

    if truth:
        final_auth = second_authentication(account_no,trial)
        if final_auth == False:
            checking_finger_print(account_no)
    return True 
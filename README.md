# Fingerprint_Based_ATM_Authentication_System
This is an Python based ATM project which uses Biometric based system to authenticate the user. Along with fingerprint authentication this project also uses OTP authentication method as second step verification. It first register the user and store the bank account details on MySQL database (name, phone no., account no.,starting balance and user's finger impression). User can access his/her account by providing bank account number and then authenticating his/her identity. If user cant authenticate within two trials the account will be blocked (NOTE: You have to unblocked that account from MySQL database). With this project user will be able to:

-- Register his/her account

-- Login to account (with two step verification)

-- Withdraw and Deposit Money

-- Mini Statement with last transaction status

## Dataset 
This project uses kaggle fingerprint dataset 
 -- Sokoto Coventry Fingerprint Dataset (SOCOFing)

To download dataset go through this link: https://www.kaggle.com/datasets/ruizgara/socofing

## Required Libraries

pip install mysql-connector-python

pip install inputimeout

pip install twilio

## User Installation
To run the project:

 1. Clone this Repo to your local machine.
 2. Make sure that all files are stored in single folder.
 3. Use any IDE which supports Python version >3.
 4. Create a MySql database and account on twilio with OTP Authentication Service
 5. Save your MySQL database details in ATM_authentication.py, login_module.py,registration_module.py,transaction_module.py
 6. Save your twilio account_sid,auth_token,verify_sid and verified_number in ATM_authentication.py
 7. Before running the file make sure that you have provide all the required details correctly in the code.
 8. Run the ATM.py file.

## Screenshots
After Running the file in #7, you will see this interface:





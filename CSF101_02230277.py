########################################################
# Name: Ugyen Choeda
# Section: 1 ME
# STD ID: 02230277
########################################################
# Reference
#https://www.youtube.com/watch?v=q6Ul2t_-soQ&pp=ygUZaG93IGluY29kZSB0eHQgaW4gcHl0aG9uIA%3D%3D
#https://www.youtube.com/watch?v=yYALsys-P_w&pp=ygUYY2xhc3NlcyBpbiBweXRob24g2LTYsdit
#https://www.youtube.com/watch?v=xTh-ln2XhgU
########################################################

import os
import random
import string

# Helper functions
def generate_acc_id():
    return ''.join(random.choices(string.digits, k=10))

def generate_acc_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def load_account_data():
    if os.path.exists('accounts.txt'):
        with open('accounts.txt', 'r') as file:
            lines = file.readlines()
            account_info = {}
            for line in lines:
                acc_id, acc_password, acc_type, acc_balance = line.strip().split(',')
                account_info[acc_id] = {
                    'acc_password': acc_password,
                    'acc_type': acc_type,
                    'acc_balance': float(acc_balance)
                }
            return account_info
    return {}

def save_account_data(account_info):
    with open('accounts.txt', 'w') as file:
        for acc_id, details in account_info.items():
            line = f"{acc_id},{details['acc_password']},{details['acc_type']},{details['acc_balance']}\n"
            file.write(line)

# Base Account class
class BankAccount:
    def __init__(self, acc_id, acc_password, acc_type, acc_balance=0):
        self.acc_id = acc_id
        self.acc_password = acc_password
        self.acc_type = acc_type
        self.acc_balance = acc_balance

    def deposit_amount(self, amount):
        self.acc_balance += amount

    def withdraw_amount(self, amount):
        if amount <= self.acc_balance:
            self.acc_balance -= amount
            return True
        return False

class IndividualAccount(BankAccount):
    def __init__(self, acc_id, acc_password, acc_balance=0):
        super().__init__(acc_id, acc_password, "individual", acc_balance)

class CorporateAccount(BankAccount):
    def __init__(self, acc_id, acc_password, acc_balance=0):
        super().__init__(acc_id, acc_password, "corporate", acc_balance)

# Bank management class
class BankSystem:
    def __init__(self):
        self.account_info = load_account_data()

    def create_bank_account(self, acc_type):
        acc_id = generate_acc_id()
        acc_password = generate_acc_password()
        if acc_type == "individual":
            account = IndividualAccount(acc_id, acc_password)
        elif acc_type == "corporate":
            account = CorporateAccount(acc_id, acc_password)
        else:
            return
        self.account_info[acc_id] = {
            'acc_password': acc_password,
            'acc_type': acc_type,
            'acc_balance': account.acc_balance
        }
        save_account_data(self.account_info)
        print(f"Account ID: {acc_id}, Password: {acc_password}")

    def authenticate(self, acc_id, acc_password):
        account_details = self.account_info.get(acc_id)
        if account_details and account_details['acc_password'] == acc_password:
            return acc_id
        return None

    def retrieve_account(self, acc_id):
        account_details = self.account_info.get(acc_id)
        if account_details['acc_type'] == 'individual':
            return IndividualAccount(acc_id, account_details['acc_password'], account_details['acc_balance'])
        elif account_details['acc_type'] == 'corporate':
            return CorporateAccount(acc_id, account_details['acc_password'], account_details['acc_balance'])

    def update_account(self, account):
        self.account_info[account.acc_id] = {
            'acc_password': account.acc_password,
            'acc_type': account.acc_type,
            'acc_balance': account.acc_balance
        }
        save_account_data(self.account_info)

    def remove_account(self, acc_id):
        if acc_id in self.account_info:
            del self.account_info[acc_id]
            save_account_data(self.account_info)

    def transfer_funds(self, from_account, to_acc_id, amount):
        if to_acc_id in self.account_info and from_account.withdraw_amount(amount):
            self.account_info[to_acc_id]['acc_balance'] += amount
            self.update_account(from_account)
            save_account_data(self.account_info)
            return True
        return False

def main():
    bank = BankSystem()
    while True:
        print("\n1. Open Account\n2. Login\n3. Exit")
        user_choice = input("Select an option: ")
        if user_choice == '1':
            acc_type = input("Enter account type (individual/corporate): ")
            bank.create_bank_account(acc_type)
        elif user_choice == '2':
            acc_id = input("Enter account ID: ")
            acc_password = input("Enter password: ")
            authenticated_id = bank.authenticate(acc_id, acc_password)
            if authenticated_id:
                account = bank.retrieve_account(authenticated_id)
                while True:
                    print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Delete Account\n6. Logout")
                    action_choice = input("Select an action: ")
                    if action_choice == '1':
                        print(f"Current balance: {account.acc_balance}")
                    elif action_choice == '2':
                        amount = float(input("Enter deposit amount: "))
                        account.deposit_amount(amount)
                        bank.update_account(account)
                    elif action_choice == '3':
                        amount = float(input("Enter withdrawal amount: "))
                        if account.withdraw_amount(amount):
                            bank.update_account(account)
                        else:
                            print("Insufficient funds.")
                    elif action_choice == '4':
                        recipient_id = input("Enter recipient account ID: ")
                        amount = float(input("Enter transfer amount: "))
                        if not bank.transfer_funds(account, recipient_id, amount):
                            print("Transfer failed.")
                    elif action_choice == '5':
                        confirmation = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirmation.lower() == 'yes':
                            bank.remove_account(account.acc_id)
                            break
                    elif action_choice == '6':
                        break
        elif user_choice == '3':
            break

if __name__ == "__main__":
    main()

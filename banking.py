import random
import sqlite3


def print_main_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def print_log_menu():
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")


def check_luhn_algorithm(card_num):
    digits = list(map(int, str(card_num)))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10 == 0


def card_number_or_pin_in_database_or_not(cur, number, pn):
    cur.execute("SELECT * FROM card WHERE number=?", (number,))
    rows = cur.fetchall()
    cur.execute("SELECT * FROM card WHERE pin=?", (pn,))
    rows += cur.fetchall()
    return len(rows) == 2


def get_balance(cur, card_num):
    cur.execute("SELECT balance FROM card WHERE number=?", (card_num,))
    balance = cur.fetchone()
    return int(balance[0])


def add_income(cur, in_come, card_num):
    balance = get_balance(cur, card_num) + in_come
    cur.execute("UPDATE card SET balance=? WHERE number=?", (balance, card_num,))
    connection.commit()


def do_transfer(cur, card_num, transfer_card_num, money):
    balance_card_num = get_balance(cur, card_num) - money
    balance_transfer_card_num = get_balance(cur, transfer_card_num) + money
    cur.execute("UPDATE card SET balance=? WHERE number=?", (balance_card_num, card_num,))
    cur.execute("UPDATE card SET balance=? WHERE number=?", (balance_transfer_card_num, transfer_card_num,))
    connection.commit()


# connection to DB and creating a table
connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
command_for_creating_table_in_database = """CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, number TEXT, 
pin TEXT, balance INTEGER DEFAULT 0)"""
cursor.execute(command_for_creating_table_in_database)

true_or_false = True

while true_or_false:
    print_main_menu()
    action = int(input())
    print()
    if action == 0:
        print("Bye!")
        true_or_false = False
        break
    elif action == 1:
        print("Your card has been created")
        tmp_for_card = "400000"
        tmp_for_pin = ""
        for i in range(4):
            tmp_for_pin += str(random.randint(0, 9))
        print("Your card number:")
        while True:
            for i in range(10):
                tmp_for_card += str(random.randint(0, 9))
            if check_luhn_algorithm(tmp_for_card):
                print(tmp_for_card)
                break
            else:
                tmp_for_card = "400000"
        print("Your card PIN:")
        print(tmp_for_pin)
        cursor.execute("INSERT INTO card(number, pin) VALUES (?, ?)", (tmp_for_card, tmp_for_pin))
        connection.commit()
        print()
    elif action == 2:
        print("Enter your card number:")
        card = input()
        print("Enter your PIN:")
        pin = input()
        print()
        if not card_number_or_pin_in_database_or_not(cursor, card, pin):
            print("Wrong card number or PIN!")
            print()
        else:
            print("You have successfully logged in!")
            print()
            while True:
                print_log_menu()
                action = int(input())
                print()
                if action == 1:
                    print("Balance: " + str(get_balance(cursor, card)))
                    print()
                elif action == 2:
                    print("Enter income:")
                    income = int(input())
                    add_income(cursor, income, card)
                    print("Income was added!")
                    print()
                elif action == 3:
                    print("Transfer")
                    print("Enter card number:")
                    card_number = input()
                    cursor.execute("SELECT * FROM card WHERE number=?", (card_number,))
                    row_s = cursor.fetchall()
                    if card_number == card:
                        print("You can't transfer money to the same account!")
                    elif not check_luhn_algorithm(card_number):
                        print("Probably you made mistake in the card number. Please try again!")
                    elif len(row_s) == 0:
                        print("Such a card does not exist.")
                    else:
                        print("Enter how much money you want to transfer:")
                        transfer_money = int(input())
                        if get_balance(cursor, card) < transfer_money:
                            print("Not enough money!")
                        else:
                            do_transfer(cursor, card, card_number, transfer_money)
                            print("Success!")
                    print()
                elif action == 4:
                    cursor.execute("DELETE FROM card WHERE number=?", (card,))
                    connection.commit()
                    print("The account has been closed!")
                    print()
                    break
                elif action == 5:
                    print("You have successfully logged out!")
                    print()
                    break
                elif action == 0:
                    print("Bye!")
                    true_or_false = False
                    break

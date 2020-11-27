import random
import database

MENU_PROMPT = """
1. Create an account
2. Log into account
0. Exit
"""

LOGGED_IN_MENU_PROMPT = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""


def check_luhn(card_number):
    return card_number[-1] == luhn_generate_last(card_number[0:-1])


def luhn_generate_last(card_number):
    sum_n = 0
    for i in range(len(card_number)):
        tmp = int(card_number[i])
        if i % 2 == 0:
            tmp *= 2
        if tmp > 9:
            tmp -= 9
        sum_n += tmp
    for i in range(10):
        if (sum_n + i) % 10 == 0:
            return str(i)


def generate_card_number():
    card_number = "400000"
    for i in range(9):
        card_number += str(random.randint(0, 9))
    card_number += luhn_generate_last(card_number)
    return card_number


def generate_pin():
    pin = ""
    pin_length = 4
    for i in range(pin_length):
        pin += str(random.randint(0, 9))
    return pin


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "0":
        if user_input == "1":
            card_number = generate_card_number()
            pin = generate_pin()

            database.add_card(connection, card_number, pin)

            print("Your card has been created")
            print(f"Your card number:\n{card_number}")
            print(f"Your card PIN:\n{pin}")
        elif user_input == "2":
            card_number = input("Enter your card number:\n")
            entered_pin = input("Enter your PIN:\n")
            if database.get_pin_by_number(connection, card_number) == entered_pin:
                print("You have successfully logged in!")

                while True:
                    user_input = input(LOGGED_IN_MENU_PROMPT)
                    if user_input == "1":
                        print(f"Balance: {database.get_balance_by_number(connection, card_number)}")
                    elif user_input == "2":
                        income = input("Enter income:\n")
                        database.add_income(connection, income, card_number)
                        print("Income was added!")
                    elif user_input == "3":
                        print("Transfer")
                        recipient = input("Enter card number: ")
                        if recipient != card_number:
                            if check_luhn(recipient):
                                x = database.get_card_by_number(connection, recipient)
                                if x is not None:
                                    payment = int(input("Enter how much money you want to transfer:\n"))
                                    if payment <= database.get_balance_by_number(connection, card_number):
                                        database.add_forfeit(connection, payment, card_number)
                                        database.add_income(connection, payment, recipient)
                                        print("Success!")
                                    else:
                                        print("Not enough money!")
                                else:
                                    print("Such a card does not exist.")
                            else:
                                print("Probably you made a mistake in the card number. Please try again!")
                        else:
                            print("You can't transfer money to the same account!")
                    elif user_input == "4":
                        database.delete_by_number(connection, card_number)
                        print("The account has been closed!")
                        break
                    elif user_input == "5":
                        print("You have successfully logged out!")
                        break
                    elif user_input == "0":
                        print("Bye!")
                        exit()
            else:
                print("Wrong card number or PIN!")
    print("Bye!")


if __name__ == "__main__":
    menu()

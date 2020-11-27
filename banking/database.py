import sqlite3

CREATE_CARD_TABLE = "CREATE TABLE IF NOT EXISTS card (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"

INSERT_CARD = "INSERT INTO card (number, pin) VALUES (?, ?);"
INSERT_CARD_WITH_BALANCE = "INSERT INTO card (number, pin) VALUES (?, ?, ?);"

GET_PIN_BY_NUMBER = "SELECT pin FROM card WHERE number = ?;"
GET_CARD_BY_NUMBER = "SELECT * FROM card WHERE number = ?;"
GET_BALANCE_BY_NUMBER = "SELECT balance FROM card WHERE number = ?;"
GET_LAST_RECORD = "SELECT * FROM card WHERE id=(SELECT max(id) FROM card);"
GET_ALL = "SELECT * FROM card;"

ADD_INCOME = "UPDATE card SET balance = balance + ? WHERE number = ?"
ADD_FORFEIT = "UPDATE card SET balance = balance - ? WHERE number = ?"
DELETE_BY_NUMBER = "DELETE FROM card WHERE number = ?"


def connect():
    return sqlite3.connect("card.s3db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_CARD_TABLE)


def delete_by_number(connection, number):
    with connection:
        connection.execute(DELETE_BY_NUMBER, (number,))


def add_card(connection, number, pin, balance=None):
    with connection:
        if balance is None:
            connection.execute(INSERT_CARD, (number, pin))
        else:
            connection.execute(INSERT_CARD_WITH_BALANCE, (number, pin, balance))


def add_income(connection, income, number):
    with connection:
        connection.execute(ADD_INCOME, (income, number))


def add_forfeit(connection, forfeit, number):
    with connection:
        connection.execute(ADD_FORFEIT, (forfeit, number))


def get_pin_by_number(connection, number):
    with connection:
        x = connection.execute(GET_PIN_BY_NUMBER, (number,)).fetchone()
        return x[0] if x is not None else None


def get_balance_by_number(connection, number):
    with connection:
        x = connection.execute(GET_BALANCE_BY_NUMBER, (number,)).fetchone()[0]
        return x


def get_card_by_number(connection, number):
    with connection:
        return connection.execute(GET_BALANCE_BY_NUMBER, (number,)).fetchone()


def get_last_record(connection):
    with connection:
        return connection.execute(GET_LAST_RECORD).fetchone()


def get_all(connection):
    with connection:
        return connection.execute(GET_ALL).fetchall()

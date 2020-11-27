# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


def print_missed_tasks(session):
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < datetime.today().date()).all()

    print("Missed tasks:")
    if len(rows) > 0:
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    else:
        print("Nothing is missed!\n")


def print_today(session):
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()

    print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
    if len(rows) > 0:
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row.task}")
    else:
        print("Nothing to do!")


def print_day(session, date):
    rows = session.query(Table).filter(Table.deadline == date).all()

    print(f"{date.strftime('%A')} {date.day} {datetime.today().strftime('%b')}:")
    if len(rows) > 0:
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row.task}\n")
    else:
        print("Nothing to do!\n")


def print_week(session):
    for i in range(7):
        print_day(session, (datetime.today() + timedelta(days=i)).date())


def print_all(session):
    rows = session.query(Table).order_by(Table.deadline).all()

    print("All tasks:")
    if len(rows) > 0:
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    else:
        print("Nothing to do!")


def delete_task(session):
    rows = session.query(Table).order_by(Table.deadline).all()

    print("Choose the number of the task you want to delete:")
    if len(rows) > 0:
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")

        choice = int(input())
        if choice < len((rows)):
            specific_row = rows[choice]  # in case rows is not empty
            session.delete(specific_row)
            session.commit()
    else:
        print("Nothing to do!")


def add_task(session):
    task = input("Enter task\n")
    deadline = input("Enter deadline\n")

    new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()

    print("The task has been added!")


MENU_PROMPT = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
"""

if __name__ == "__main__":
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # create database file
    Base.metadata.create_all(engine)  # creates a table in our database by generating SQL queries

    # To access the database, we need to create a session:
    Session = sessionmaker(bind=engine)
    session = Session()

    while (user_input := input(MENU_PROMPT)) != "0":
        if user_input == "1":
            print_today(session)
        elif user_input == "2":
            print_week(session)
        elif user_input == "3":
            print_all(session)
        elif user_input == "4":
            print_missed_tasks(session)
        elif user_input == "5":
            add_task(session)
        elif user_input == "6":
            delete_task(session)

    print("Bye!")

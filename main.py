from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy import MetaData

Base = declarative_base()

class task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

today=datetime.strftime(datetime.today(), '%Y-%m-%d')
today_format=datetime.strftime(datetime.today(), '%d %b')

class menu():
    def __init__(self):
        self.task_4_today=None
        self.task_date = datetime.today().date()
        self.day=None


    def do(self):
        self.task_4_today = session.query(task).filter(task.deadline == self.task_date).all()
        if self.task_4_today:
            for i in range(len(self.task_4_today)):
                print(f'{i + 1}. {self.task_4_today[i]}')    # num. list of tasks
        else:
            print('Nothing to do!')
        # task for the certain date

    def weekd(self, d):
        week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        self.day=week[d]
        return self.day

    def do_on_week(self):
        days_counter=0
        for i in range(7):
            self.task_date = datetime.today().date() + timedelta(days_counter)
            print('\n', self.weekd(self.task_date.weekday()), ' ',
                  datetime.strftime(datetime.today() + timedelta(days_counter), '%d %b'), ':', sep='')
            # day by day using prev. func.
            self.do()
            days_counter += 1
        self.main()

    def all_tasks(self):
        all = (session.query(task).filter(task.deadline >= datetime.today().date()).order_by(task.deadline).all())
        dates = (session.query(task.deadline).filter(task.deadline
                                                     >= datetime.today().date()).order_by(task.deadline).all())
        # tasks to do
        session.commit()
        ind=0
        for d in dates:
            print(ind+1, '. ', all[ind], '. ', datetime.strftime(d[0], '%d %b'), sep='')
            ind+=1
        self.main()

    def missed_tasks(self):
        missed = (session.query(task.task, task.deadline).filter(task.deadline < datetime.today().date()).order_by(task.deadline).all())
        # task and date from sql
        if missed:
            print('Missed tasks:')
            tada_counter=1 # print counter
            for ta, date in missed:
                print(tada_counter, '. ', ta, '. ', datetime.strftime(date, '%d %b'), sep='')
                tada_counter+=1
        else: print('Missed tasks:\nNothing is missed!')
        self.main()

    def do_today(self):
        print(f'Today {today_format}:')
        self.task_date=today
        self.do()
        self.main()

    def add_task(self):
        print('Enter task')
        input_value = input()
        print('Enter deadline')
        input_deadline = input()
        # d = datetime.strptime(input_deadline, '%Y-%m-%d')
        # print(d)
        new_row=task(task=input_value, deadline=datetime.strptime(input_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('The task has been added!')
        self.main()

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        all_tasks = (session.query(task.id, task.task, task.deadline).order_by(task.deadline).all())
        at_counter = 1
        for aid, at, ad in all_tasks:
            print(at_counter, '. ', at, '. ', datetime.strftime(ad, '%d %b'), sep='')
            at_counter+=1
        to_delete = int(input())
        all_row = session.query(task).order_by(task.deadline).all()     # output order != sql id
        session.delete(all_row[to_delete-1])
        session.commit()
        print('The task has been deleted!')
        self.main()

    def exit(self):
        print('\nBye!')

    def main(self):
        print('\n1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n'
              '4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit')
        input_value=input()
        if input_value == '1':
            self.do_today()
        elif input_value == '2':
            self.do_on_week()
        elif input_value == '3':
            self.all_tasks()
        elif input_value == '4':
            self.missed_tasks()
        elif input_value == '5':
            self.add_task()
        elif input_value == '6':
            self.delete_task()
        elif input_value == '0':
            self.exit()
        # print(today)

m=menu()
m.main()

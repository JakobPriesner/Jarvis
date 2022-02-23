import io
import logging
from datetime import datetime
from typing import Callable, List, Dict, Any, TypeAlias

from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException

import sqlite3
from sqlite3 import Connection, Cursor

from src.speechassistant.exceptions.SQLException import *

shopping_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, float]]

class DataBase:
    def __init__(self, root_path: str) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[ACTION] Initialize DataBase...\n')
        self.db = sqlite3.connect(f'{root_path}database\\data_base')
        self.error_counter: int = 0

        self.alarm_interface = self._AlarmInterface(self.db)
        self.timer_interface = self._TimerInterface(self.db)
        self.reminder_interface = self._ReminderInterface(self.db)
        self.quiz_interface = self._QuizInterface(self.db)
        self.shoppinglist_interface = self._ShoppingListInterface(self.db, self.__execute)
        self.user_interface = self._UserInterface(self.db)
        self.routine_interface = self._RoutineInterface(self.db)

        logging.info('\n[INFO] DataBase successfully initialized.')

    def create_tables(self) -> None:
        # toDo: CONSTRAINTS

        logging.info('[ACTION] Create tables...')
        self.__create_table('CREATE TABLE IF NOT EXISTS audio ('
                            'id INTEGER PRIMARY KEY,'
                            'path VARCHAR(50))')

        self.__create_table('CREATE TABLE IF NOT EXISTS user ('
                            'uid INTEGER PRIMARY KEY,'
                            'alias VARCHAR(10) UNIQUE,'
                            'firstname VARCHAR(15),'
                            'lastname VARCHAR(30),'
                            'birthday VARCHAR(10),'
                            'mid INTEGER UNIQUE,'
                            'sid INTEGER,'
                            'FOREIGN KEY(sid) REFERENCES audio(id))')

        self.__create_table('CREATE TABLE IF NOT EXISTS alarm ('
                            'sid INTEGER,'
                            'uid INTEGER,'
                            'hour INTEGER,'
                            'minute INTEGER,'
                            'total_seconds UNSIGNED BIG INT,'
                            'timestamp VARCHAR(8) PRIMARY KEY,'
                            'text VARCHAR(255),'
                            'active INTEGER,'
                            'prepared INTEGER,'
                            'FOREIGN KEY(sid) REFERENCES audio(id),'
                            'FOREIGN KEY(uid) REFERENCES user(uid))'
                            )

        self.__create_table('CREATE TABLE IF NOT EXISTS timer ('
                            'id INTEGER PRIMARY KEY,'
                            'time VARCHAR(25),'
                            'text VARCHAR(255),'
                            'duration VARCHAR(50),'
                            'uid INTEGER,'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS shoppinglist ('
                            'id INTEGER PRIMARY KEY,'
                            'name varchar(50) UNIQUE,'
                            'measure varchar(4),'
                            'quantity FLOAT)')

        self.__create_table('CREATE TABLE IF NOT EXISTS reminder ('
                            'id INTEGER PRIMARY KEY,'
                            'time VARCHAR(25),'
                            'text VARCHAR(255),'
                            'uid INTEGER,'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routine ('
                            'rid INTEGER PRIMARY KEY,'
                            'daily INTEGER,'
                            'monday INTEGER,'
                            'tuesday INTEGER,'
                            'wednesday INTEGER,'
                            'thursday INTEGER,'
                            'friday INTEGER,'
                            'saturday INTEGER,'
                            'sunday INTEGER)')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinedates ('
                            'id INTEGER,'
                            'day INTEGER,'
                            'month INTEGER,'
                            'PRIMARY KEY(id, day, month),'
                            'FOREIGN KEY(id) REFERENCES routine(rid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinecommands ('
                            'id INTEGER,'
                            'module_name VARCHAR(50),'
                            'PRIMARY KEY(id, module_name),'
                            'FOREIGN KEY(id) REFERENCES routine(rid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS commandtext ('
                            'id INTEGER,'
                            'text VARCHAR(255),'
                            'PRIMARY KEY(id, text),'
                            'FOREIGN KEY(id) REFERENCES routinecommands(id))')

        self.__create_table('CREATE TABLE IF NOT EXISTS quiz ('
                            'category VARCHAR(50) PRIMARY KEY)')

        self.__create_table('CREATE TABLE IF NOT EXISTS questions ('
                            'category REFERENCES quiz(category),'
                            'qid INTEGER,'
                            'starting INTEGER,'
                            'question VARCHAR(255),'
                            'audio INTEGER,'
                            'answer VARCHAR(255),'
                            'PRIMARY KEY(category, qid),'
                            'FOREIGN KEY(audio) REFERENCES audio(id))')

        self.__create_table('CREATE TABLE IF NOT EXISTS answeroptions ('
                            'qid INTEGER,'
                            'text VARCHAR(255),'
                            'PRIMARY KEY(qid, text),'
                            'FOREIGN KEY(qid) REFERENCES questions(qid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS notification ('
                            'uid INTEGER,'
                            'text VARCHAR(255),'
                            'PRIMARY KEY(uid, text),'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        self.db.commit()

        if self.error_counter == 0:
            logging.info('\n[INFO] Tables successfully created!')
        else:
            raise UnsolvableException(f'During the creation of {self.error_counter} tables there were problems. '
                                      'Manual intervention mandatory.')

    def __create_table(self, command: str) -> None:
        cursor: Cursor = self.db.cursor()
        try:
            cursor.execute(command)
            logging.info(f"[INFO] Successfully created table {command.split(' ')[5]}!")
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Couldn't create table {command.split(' ')[5]}:\n {e}")
        finally:
            cursor.close()

    def __remove_tables(self):
        pass

    def stop(self):
        logging.info('[ACTION] Stopping database...')
        self.db.close()

    class _AlarmInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] AlarmInterface initialized.')

        def get_alarms(self):
            pass

        def add_alarm(self, time: datetime, text: str, song: str) -> bool:
            pass

        def delete_alarm(self):
            pass

        def update_alarm(self):
            pass

        def add_alarm_sound(self, name: str, sound: io.BytesIO) -> bool:
            pass

        def __create_table(self):
            pass

    class _TimerInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] TimerInterface initialized.')

        def get_timer(self):
            pass

        def add_timer(self):
            pass

        def delete_timer(self):
            pass

        def __create_table(self):
            pass

    class _ReminderInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] ReminderInterface initialized.')

        def get_reminder(self):
            pass

        def add_reminder(self):
            pass

        def delete_reminder(self):
            pass

        def __create_table(self):
            pass

    class _ShoppingListInterface:

        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
            logging.info('[INFO] ShoppingListInterface initialized.')

        def get_list(self) -> list[shopping_item]:
            statement: str = 'SELECT * FROM shoppinglist'
            result_set: list[tuple[int, str, str, float]] = self.exec_func(statement)
            return self.__build_json(result_set)

        def add_item(self, name: str, measure: str, quantity: float) -> None:
            statement: str = f'INSERT INTO shoppinglist ("name", "measure", "quantity") ' \
                             f'VALUES ("{name}", "{measure}", {quantity})'
            self.exec_func(statement)

        def update_item(self, name: str, quantity: float) -> None:
            statement: str = f'UPDATE shoppinglist ' \
                             f'SET quantity="{quantity}" ' \
                             f'WHERE name="{name}"'
            self.exec_func(statement)

        def remove_item(self, name: str) -> None:
            statement: str = f'DELETE FROM shoppinglist WHERE name="{name}"'
            self.exec_func(statement)

        def clear_list(self) -> None:
            statement: str = f'DELETE FROM shoppinglist'
            self.exec_func(statement)

        def __create_table(self):
            pass

        @staticmethod
        def __build_json(result_set: list[tuple[int, str, str, float]]) -> list[shopping_item]:
            result_list: list[shopping_item] = []

            for rid, name, measure, quantity in result_set:
                result_list.append({
                    "id": rid,
                    "name": name,
                    "measure": measure,
                    "quantity": quantity
                })
            return result_list

    class _UserInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] UserInterface initialized.')

        def get_users(self):
            pass

        def add_user(self):
            pass

        def remove_user(self):
            pass

        def __create_table(self):
            pass

    class _RoutineInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] RoutineInterface initialized.')

        def get_routines(self):
            pass

        def add_routine(self):
            pass

        def update_routine(self):
            pass

        def delete_routine(self):
            pass

        def __create_table(self):
            pass

    class _QuizInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] QuizInterface initialized.')

        def load_stack(self, theme: str):
            pass

        def update_stack(self, theme: str):
            pass

        def __create_table(self):
            pass

    def __execute(self, command: str) -> list:
        cursor: Cursor = self.db.cursor()
        result_set: list
        try:
            cursor.execute(command)
            result_set = cursor.fetchall()
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Couldn't execute SQL command: {command}:\n {e}")
            raise SQLException(f"Couldn't execute SQL Statement: {command}\n{e}")
        finally:
            cursor.close()
        self.db.commit()
        return result_set


if __name__ == "__main__":
    dbb = DataBase("C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\")
    # dbb.create_tables()
    dbb.shoppinglist_interface.clear_list()
    dbb.shoppinglist_interface.add_item('Milch', 'ml', 250)
    dbb.shoppinglist_interface.add_item('Bananen', '', 3)
    result = dbb.shoppinglist_interface.get_list()
    logging.info(result)
    dbb.shoppinglist_interface.update_item('Milch', 1402.95)
    result = dbb.shoppinglist_interface.get_list()
    logging.info(result)

import sqlite3 as sq
import datetime as dt


class Clients_table:
    """Класс для работы с таблицей, в которой расположены данные о клиентах в базе данных"""

    def __init__(self, path: str):
        """Инициализирует соединение с базой данных и создаёт таблицу, если её не существует"""

        self.con = sq.connect(path)

        self.cur = self.con.cursor()

        self.table_name = 'Клиенты'

        self.poles = ['ID_ученика', 'Telegram_id_родителя', 'Telegram_id_ученика',
                      'Фамилия_ученика', 'Имя_ученика', 'Отчество_ученика',
                      'Фамилия_родителя', 'Имя_родителя', 'Отчество_родителя',
                      'Телефон_родителя', 'Телефон_ученика',
                      'Изучаемые_предметы', 'Тип_обучения', 'Стоимость_занятия', 'Группа', 'Статус_обучения']

        req = f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                                             ({self.poles[0]} TEXT PRIMARY KEY AUTOINCREMENT,
                                             {self.poles[1]} TEXT,
                                             {self.poles[2]} TEXT,
                                             {self.poles[3]} TEXT NOT NULL,
                                             {self.poles[4]} TEXT NOT NULL,
                                             {self.poles[5]} TEXT NOT NULL,
                                             {self.poles[6]} TEXT NOT NULL,
                                             {self.poles[7]} TEXT NOT NULL,
                                             {self.poles[8]} TEXT NOT NULL,
                                             {self.poles[9]} TEXT NOT NULL,
                                             {self.poles[10]} TEXT NOT NULL,
                                             {self.poles[11]} TEXT NOT NULL,
                                             {self.poles[12]} TEXT NOT NULL,
                                             {self.poles[13]} REAL NOT NULL,
                                             {self.poles[14]} TEXT,
                                             {self.poles[15]} TEXT NOT NULL)"""

        self.cur.execute(req)

    def request_pupils_list(self, type_of_training: str, learning_status: str) -> list:
        """Функция, возвращающая учеников, у которых индивидуальны/групповые занятия и занимаются/больше не занимаются
        в зависимости от параметров"""

        req = f"""SELECT {self.poles[1]},
                         {self.poles[2]},
                         {self.poles[3]},
                         {self.poles[4]},
                         {self.poles[5]},
                         {self.poles[6]},
                         {self.poles[7]},
                         {self.poles[8]},
                         {self.poles[9]},
                         {self.poles[10]},
                         {self.poles[11]},
                         {self.poles[13]},
                         {self.poles[15]}
                  FROM {self.table_name}
                  WHERE {self.poles[12]} == ? AND {self.poles[15]} == ?"""

        pupils = list(self.cur.execute(req, (type_of_training, learning_status)))

        poles_list = [self.poles[i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15]]
        pupils = [{poles_list[j]: row[j] for j in range(len(row))} for row in pupils]

        return pupils

    def insert_datas(self, insert_dict: dict):
        """Функция, которая принимает словарь, в котором ключи являются полями, а значения - параметрами полей
        и создаёт новую строку в таблице с такими параметрами"""

        poles = ', '.join(list(insert_dict.keys()))
        values = tuple(insert_dict.values())

        q = '?, ' * len(values)
        req = f"""INSERT INTO {self.table_name} ({poles}) VALUES ({q.strip()[:-1]})"""

        self.cur.execute(req, values)
        self.con.commit()

    def change_pupil_data(self, pupil_id: str, pole: str, value: str):
        """Принимает на вход id_ученика, поле и значение, которое необходимо вставить в это поля для этого ученика"""

        req = f"""UPDATE {self.table_name} SET "{pole}" = ? WHERE {self.poles[0]} = ?"""

        self.cur.execute(req, (value, pupil_id))

        self.con.commit()

    def delete_pupil(self, pupil_id: str):
        """Принимает на вход id-ученика и удаляет его из базы данных"""

        req = f"""DELETE FROM {self.table_name} WHERE {self.poles[0]} = ?"""

        self.cur.execute(req, (pupil_id,))

        self.con.commit()

    def drop_table(self):
        """Удаляет таблицу"""

        req = f'DROP TABLE IF EXISTS {self.table_name}'

        self.cur.execute(req)


class Paids_table:
    """Класс для работы с таблицей, в которой расположены данные о занятиях и оплатах в базе данных"""

    def __init__(self, path: str):
        """Инициализирует соединение с базой данных и создаёт таблицу, если её не существует"""

        self.con = sq.connect(path)

        self.cur = self.con.cursor()

        self.table_name = 'Оплаты'

        self.poles = ['ID_ученика', 'Telegram_id_родителя', 'Фамилия_ученика', 'Имя_ученика', 'Отчество_ученика',
                      'Дата_и_время_начала_занятия', 'Дата_и_время_конца_занятия',
                      'Оплата', 'Статус_оплаты', 'Время_оплаты']

        req = f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                                             ({self.poles[0]} TEXT NOT NULL,
                                             {self.poles[1]} TEXT,
                                             {self.poles[2]} TEXT NOT NULL,
                                             {self.poles[3]} TEXT NOT NULL,
                                             {self.poles[4]} TEXT NOT NULL,
                                             {self.poles[5]} datetime NOT NULL,
                                             {self.poles[6]} datetime NOT NULL,
                                             {self.poles[7]} REAL NOT NULL,
                                             {self.poles[8]} TEXT,
                                             {self.poles[9]} datetime)"""

        self.cur.execute(req)

    def request_date_and_hours_when_was_pupil(self, pupil_id: str) -> list:
        """Функция, принимающая на вход ID ученика и возвращающая список с историей занятий этого ученика"""

        req = f"""SELECT {self.poles[5]},
                         {self.poles[6]}
                  FROM {self.table_name}
                  WHERE {self.poles[0]} = ?"""

        dates = list(self.cur.execute(req, (pupil_id,)))

        return dates

    def request_payded_dates(self, pupil_id: str) -> (list, int):
        """Функция, принимающая на вход ID ученика и возвращающая список с датами оплаченных занятий и суммарной оплатой"""

        req = f"""SELECT {self.poles[5]},
                         {self.poles[6]},
                         {self.poles[9]}
                  FROM {self.table_name}
                  WHERE {self.poles[0]} = ? AND {self.poles[8]} = ?"""

        dates = list(self.cur.execute(req, (pupil_id, 'Оплачено')))

        req = f"""SELECT SUM({self.poles[7]})
                  FROM {self.table_name} 
                  WHERE {self.poles[0]} = ? AND {self.poles[8]} = ?"""

        summ = list(self.cur.execute(req, (pupil_id, 'Оплачено')))[0][0]

        return dates, summ

    def request_not_payded_dates_and_debt(self, pupil_id: str) -> (list, int):
        """Функция, принимающая на вход ID ученика и возвращающая список с датами неоплаченных занятий и суммой долга"""

        req = f"""SELECT {self.poles[5]},
                         {self.poles[6]}
                  FROM {self.table_name}
                  WHERE {self.poles[0]} = ? AND {self.poles[8]} IS ?"""

        dates = list(self.cur.execute(req, (pupil_id, None)))

        req = f"""SELECT SUM({self.poles[7]})
                  FROM {self.table_name} 
                  WHERE {self.poles[0]} = ? AND {self.poles[8]} IS ?"""

        summ = list(self.cur.execute(req, (pupil_id, None)))[0][0]

        return dates, summ

    def request_statistics_at_the_period(self, begin_date: str, end_date: str) -> dict:
        """Функция, возвращающая полную статистику по оплатам в заданный промежуток времени"""

        if begin_date > end_date:
            begin_date, end_date = end_date, begin_date

        req = f"""SELECT SUM({self.poles[7]})
                  FROM {self.table_name}
                  WHERE {self.poles[5]} BETWEEN ? AND ?"""

        total_income = list(self.cur.execute(req, (begin_date, end_date)))[0][0]

        begin_date = dt.datetime.strptime(begin_date, '%d-%m-%Y %H:%M:%S')
        end_date = dt.datetime.strptime(end_date, '%d-%m-%Y %H:%M:%S')
        days = int(str((end_date - begin_date)).split()[0])
        years = days / 365
        months = years * 12
        weeks = days / 7
        statistic_dict = {"Период": str(begin_date) + ' - ' + str(end_date),
                          "Количество дней": days,
                          "Количество недель": weeks,
                          "Количество месяцев": months,
                          "Количество лет": years,
                          "Средний заработок в день": total_income / days,
                          "Средний заработок в неделю": total_income / weeks,
                          "Средний заработок в месяц": total_income / months,
                          "Средний заработок в год": total_income / years}

        return statistic_dict

    def insert_datas(self, insert_dict: dict):
        """Функция, которая принимает словарь, в котором ключи являются полями, а значения - параметрами полей
        и создаёт новую строку в таблице с такими параметрами"""

        poles = ', '.join(list(insert_dict.keys()))
        values = tuple(insert_dict.values())

        q = '?, ' * len(values)
        req = f"""INSERT INTO {self.table_name} ({poles}) VALUES ({q.strip()[:-1]})"""

        self.cur.execute(req, values)
        self.con.commit()

    def commit_paid(self, pupil_id: str, begin: str, end: str, paid_time: str):
        """Функция, которая вносит подтверждение об оплате занятия в таблицу"""

        req = f"""UPDATE {self.table_name} 
                  SET {self.poles[8]} = ?, {self.poles[9]} = ? 
                  WHERE {self.poles[0]} = ? AND {self.poles[5]} = ? AND {self.poles[6]} = ?"""

        self.cur.execute(req, ('Оплачено', paid_time, pupil_id, begin, end))

        self.con.commit()

    def delete_paid(self, pupil_id: str, begin: str):
        """Принимает на вход id-ученика и дату начала занятия и удаляет данную запись из базы данных"""

        req = f"""DELETE FROM {self.table_name} WHERE {self.poles[0]} = ? AND {self.poles[5]} = ?"""

        self.cur.execute(req, (pupil_id, begin))

        self.con.commit()

    def drop_table(self):
        """Удаляет таблицу"""

        req = f'DROP TABLE IF EXISTS {self.table_name}'

        self.cur.execute(req)


class Groups_members_table:
    """Класс для работы с составом групп. В этих таблицах содержится только ID-учеников по группам"""

    def __init__(self, path: str):
        """Инициализирует соединение с базой данных и создаёт таблицу, если её не существует"""

        self.con = sq.connect(path)

        self.cur = self.con.cursor()

        self.table_name = 'Ученики_в_группах'

        self.groups_pole = 'Группы'

        req = f"""CREATE TABLE IF NOT EXISTS {self.table_name} ({self.groups_pole} TEXT)"""

        self.cur.execute(req)

    def request_composition_of_the_group(self, group_number: str):
        """Возвращает состав заданной группы в виде списка id-учеников"""

        req = f"""PRAGMA table_info({self.table_name})"""
        self.cur.execute(req)

        pupils = [i[1] for i in self.cur.fetchall()]
        pupils.pop(0)

        req = f"""SELECT * FROM {self.table_name} WHERE {self.groups_pole} = ?"""
        self.cur.execute(req, (group_number,))

        groups = list(self.cur.fetchall()[0])
        groups.pop(0)

        composition = [pupils[i] for i in range(len(groups)) if groups[i] is not None]

        return composition

    def add_pupil(self, pupil: str):
        """Добавляет новый столбец с учеником в таблицу"""

        req = f"""PRAGMA table_info({self.table_name})"""
        self.cur.execute(req)

        pupils = self.cur.fetchall()
        pupils = [i[1] for i in pupils][1:]

        if pupil not in pupils:
            req = f"""ALTER TABLE {self.table_name} ADD '{pupil}' TEXT"""
            self.cur.execute(req)
            self.con.commit()

    def add_group(self, group: str):
        """Добавляет новую группу в таблицу"""

        req = f"""SELECT {self.groups_pole} FROM {self.table_name}"""
        self.cur.execute(req)
        groups = [el[0] for el in self.cur.fetchall()]

        if group not in groups:
            req = f"""INSERT INTO {self.table_name} ({self.groups_pole}) VALUES (?)"""
            self.cur.execute(req, (group,))
            self.con.commit()

    def insert_or_drop_pupil_into_group(self, pupil_id: str, group: str, status: bool):
        """Связывает ученика с его группой"""

        if status:
            status = 'Активен'
        else:
            status = None

        req = f"""UPDATE {self.table_name} SET "{pupil_id}" = ? WHERE "{self.groups_pole}" = ?"""

        self.cur.execute(req, (status, group))
        self.con.commit()

    def delete_group(self, group):
        """Принимает номер группы и удаляет её из базы данных"""

        req = f"""DELETE FROM {self.table_name} WHERE {self.groups_pole} = ?"""

        self.cur.execute(req, (group,))

        self.con.commit()

    def drop_table(self):
        """Удаляет таблицу"""

        req = f'DROP TABLE IF EXISTS {self.table_name}'

        self.cur.execute(req)


class Groups_info_table:
    """Класс для работы с таблицей, в которой содержится информация обо всех группах"""

    def __init__(self, path):
        """Инициализирует соединение с базой данных и создаёт таблицу, если её не существует"""

        self.con = sq.connect(path)

        self.cur = self.con.cursor()

        self.table_name = 'Информация_о_группах'

        self.poles = ['Номер_группы', 'Изучаемый_предмет', 'Количество_учеников', 'Статус_группы']

        req = f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                                             ({self.poles[0]} TEXT NOT NULL,
                                             {self.poles[1]} TEXT NOT NULL,
                                             {self.poles[2]} INTEGER,
                                             {self.poles[3]} TEXT NOT NULL)"""

        self.cur.execute(req)

    def request_list_of_active_groups(self) -> list:
        """Возвращает список с информацией об активных группах"""

        req = f"""SELECT {self.poles[0]}, {self.poles[1]}, {self.poles[2]}
                  FROM {self.table_name} 
                  WHERE {self.poles[3]} = ?"""

        self.cur.execute(req, ('Активна',))

        groups = self.cur.fetchall()

        return groups

    def request_list_of_deactivated_groups(self) -> list:
        """Возвращает список с информацией о неактивных группах"""

        req = f"""SELECT {self.poles[0]}, {self.poles[1]}, {self.poles[2]}
                  FROM {self.table_name} 
                  WHERE {self.poles[3]} = ?"""

        self.cur.execute(req, ('Не активна',))

        groups = self.cur.fetchall()

        return groups

    def add_group(self, group: str, science: str):
        """Добавление новой группы"""

        req = f"""INSERT INTO {self.table_name} ({self.poles[0]}, {self.poles[1]}, {self.poles[3]}) VALUES (?, ?, ?)"""

        self.cur.execute(req, (group, science, 'Не активна'))

        self.con.commit()

    def change_number_of_pupils_in_group(self, group: str, number_of_pupils: int):
        """Функция, которая меняет количество учеников для конкретной группы"""

        req = f"""UPDATE {self.table_name} SET {self.poles[2]} = ? WHERE {self.poles[0]} = ?"""

        self.cur.execute(req, (number_of_pupils, group))

        self.con.commit()

    def activate_or_deactivate_group(self, group: str, status: bool):
        """Функция, которая активирует/дезактивирует группу"""

        req = f"""UPDATE {self.table_name} SET {self.poles[3]} = ? WHERE {self.poles[0]} = ?"""
        if status:
            status = 'Активна'
        else:
            status = 'Не активна'

        self.cur.execute(req, (status, group))

        self.con.commit()

    def delete_group(self, group):
        """Принимает номер группы и удаляет её из базы данных"""

        req = f"""DELETE FROM {self.table_name} WHERE {self.poles[0]} = ?"""

        self.cur.execute(req, (group,))

        self.con.commit()

    def drop_table(self):
        """Удаляет таблицу"""

        req = f'DROP TABLE IF EXISTS {self.table_name}'

        self.cur.execute(req)


class Time_table:
    """Класс для работы с расписанием учеников и групп"""

    def __init__(self, path):
        """Инициализирует соединение с базой данных и создаёт таблицу, если её не существует
        заполнять таблицу промежутками времени от 09:00 до 1:00 и статусом "Свободно" для всех дней недели.
        Если таблица уже существует, то дополняет её промежутками времени, которые могли случайно удалиться
        из таблицы"""

        self.con = sq.connect(path)

        self.cur = self.con.cursor()

        self.table_name = 'Раcписание'

        self.poles = ['Время_начала_занятия', 'Время_конца_занятия',
                      'Понедельник', 'Вторник', 'Среда', 'Четверг',
                      'Пятница', 'Суббота', 'Воскресение']

        req = f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                                             ({self.poles[0]} time NOT NULL UNIQUE,
                                              {self.poles[1]} time NOT NULL,
                                              {self.poles[2]} TEXT NOT NULL,
                                              {self.poles[3]} TEXT NOT NULL,
                                              {self.poles[4]} TEXT NOT NULL,
                                              {self.poles[5]} TEXT NOT NULL,
                                              {self.poles[6]} TEXT NOT NULL,
                                              {self.poles[7]} TEXT NOT NULL,
                                              {self.poles[8]} TEXT NOT NULL)"""

        self.cur.execute(req)

        for i in range(9, 25):
            HH = i % 24
            if HH < 10:
                time_begin = f'0{HH}:00'
                if HH == 9:
                    time_end = f'{HH + 1}:00'
                else:
                    time_end = f'0{HH + 1}:00'
            else:
                time_begin = f'{HH}:00'
                if HH == 23:
                    time_end = f'00:00'
                else:
                    time_end = f'{HH + 1}:00'

            req = f"""SELECT {self.poles[0]} FROM '{self.table_name}' WHERE {self.poles[0]} = ?"""
            if not bool(list(self.cur.execute(req, (time_begin,)))):
                req = f"""INSERT INTO {self.table_name}
                                      ('{self.poles[0]}',
                                       '{self.poles[1]}',
                                       '{self.poles[2]}',
                                       '{self.poles[3]}',
                                       '{self.poles[4]}',
                                       '{self.poles[5]}',
                                       '{self.poles[6]}',
                                       '{self.poles[7]}',
                                       '{self.poles[8]}') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                params = (time_begin, time_end, 'Свободно', 'Свободно', 'Свободно', 'Свободно', 'Свободно', 'Свободно',
                          'Свободно')

                self.cur.execute(req, params)

        self.con.commit()

    @staticmethod
    def pop_empty_values_in_dict(Dictionary: dict) -> dict:
        """Метод, который удаляет из словаря все пары ключ-значение, у которых значение является пустым объектом"""

        keys_with_empty_value = []
        for key in Dictionary:
            if len(Dictionary[key]) == 0:
                keys_with_empty_value.append(key)
        for key in keys_with_empty_value:
            Dictionary.pop(key)

        return Dictionary

    def request_all_times_for_admin(self) -> dict:
        """Функция, возвращающая полное расписание занятий в виде словаря вида
        {(Время начала, Время конца):{<День недели1>:<Статус ячейки1>, <День недели2>:<Статус ячейки2>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row))}
                      for row in available_dates}

        return dates_dict

    def request_available_times_for_parent(self, pupil_id: str) -> dict:
        """Функция, принимающая на вход ID ученика и возвращающая расписание со свободными ячейками
        и с ячейками, в которых находится ученик в виде словаря вида
        {(Время начала, Время конца):{<День недели1>:<Статус ячейки1>, <День недели2>:<Статус ячейки2>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row))
                                         if row[i] == 'Свободно' or row[i] == pupil_id}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict

    def request_individual_schedule_for_pupil(self, pupil_id: str) -> dict:
        """Функция, принимающая на вход ID ученика и возвращающая расписание конкретного ученика
        в виде словаря вида
        {(Время начала, Время конца):{<День недели1>:<ID ученика>, <День недели2>:<ID ученика>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row)) if row[i] == pupil_id}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict

    def request_time_for_all_groups(self) -> dict:
        """Функция, принимающая, возвращающая расписание всех группа в виде словаря вида
        {(Время начала, Время конца):{<День недели1>:<Группа>, <День недели2>:<Группа>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row)) if row[i][0] == 'Г'}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict

    def request_time_for_group(self, group_number: str) -> dict:
        """Функция, принимающая на вход номер группы, возвращающая расписание этой группы в виде словаря вида
        {(Время начала, Время конца):{<День недели1>:<Группа>, <День недели2>:<Группа>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row)) if row[i] == group_number}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict

    def request_busy_time(self) -> dict:
        """Функция,возвращающая расписание со значениями ячеек "Занято"
        {(Время начала, Время конца):{<День недели1>:<Статус ячейки1>, <День недели2>:<Статус ячейки2>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row))
                                         if row[i] == 'Занято'}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict
    
    def request_all_available_times(self) -> dict:
        """Функция,возвращающая расписание со значениями ячеек "Свободно"
        {(Время начала, Время конца):{<День недели1>:<Статус ячейки1>, <День недели2>:<Статус ячейки2>}"""

        req = f"""SELECT * FROM {self.table_name}"""
        available_dates = list(self.cur.execute(req))
        dates_dict = {(row[0], row[1]): {self.poles[i]: row[i] for i in range(2, len(row))
                                         if row[i] == "Свободно"}
                      for row in available_dates}
        self.pop_empty_values_in_dict(dates_dict)

        return dates_dict

    def drop_pupil_or_group_from_time(self, day_of_week, begin, end):
        """Функция, удаляющая ученика/группу из ячейки"""

        req = f"""UPDATE {self.table_name} SET {day_of_week} = ? WHERE {self.poles[0]} = ? AND {self.poles[1]} = ?"""

        self.cur.execute(req, ('Свободно', begin, end))

        self.con.commit()

    def add_pupil_or_group_from_time(self, pupil_or_group, day_of_week, begin, end):
        """Функция, добавляющая ученика или группу в расписание"""

        req = f"""UPDATE {self.table_name} SET {day_of_week} = ? WHERE {self.poles[0]} = ? AND {self.poles[1]} = ?"""

        self.cur.execute(req, (pupil_or_group, begin, end))

        self.con.commit()

    def do_time_is_busy(self, day_of_week, begin, end):
        """Функция, делающая ячейку времени недоступной/занятой"""

        req = f"""UPDATE {self.table_name} SET {day_of_week} = ? WHERE {self.poles[0]} = ? AND {self.poles[1]} = ?"""

        self.cur.execute(req, ('Занято', begin, end))

        self.con.commit()

    def drop_table(self):
        """Удаляет таблицу"""

        req = f'DROP TABLE IF EXISTS {self.table_name}'

        self.cur.execute(req)


path = r'DBs\clients.db'

DB1 = Clients_table(path)
DB2 = Paids_table(path)
DB3 = Groups_members_table(path)
DB4 = Groups_info_table(path)
DB5 = Time_table(path)

# print(DB5.request_all_available_times())

# DB5.do_time_is_busy('Понедельник', '09:00', '10:00')

# print(DB5.request_busy_time())

# DB5.do_time_is_busy('Вторник', '12:00', '13:00')

# DB5.add_pupil_or_group_from_time('ГР1201', 'Понедельник', '12:00', '13:00')

# DB5.drop_pupil_or_group_from_time('Вторник', '12:00', '13:00')

# DB4.delete_group('Ф40-401')

# DB3.delete_group('Ф40-401')

# DB2.delete_paid('1223', '16-10-2020 18:48:00')

# DB1.delete_pupil('12212')

# DB4.request_list_of_active_groups()
# DB4.request_list_of_deactivated_groups()

# DB4.activate_or_deactivate_group('Ф30-401', True)

# DB4.change_number_of_pupils_in_group('Ф30-401', 5)

# DB4.add_group('Ф30-401', 'Матан')
# DB4.add_group('Ф40-401', 'Физон')
# DB4.add_group('Ф50-401', 'Прога')

# print(DB2.request_payded_dates('1223'))
# print(DB2.request_not_payded_dates_and_debt('1223'))


# DB2.commit_paid('1223', '16-10-2020 18:48:00', '16-10-2020 13:48:00', '16-10-2020 20:48:00')

# DB1.change_pupil_data('1222', 'Фамилия_ученика', 'Павлов')

# DB3.add_group('Ф30-401')
# DB3.add_group('Ф40-401')
# DB3.add_group('Ф50-401')
# DB3.add_pupil('2737392')
# DB3.add_pupil('2737393')
# DB3.add_pupil('2737376')
# DB3.add_pupil('2733332392')
# DB3.add_pupil('27373923467567')
# DB3.insert_or_drop_pupil_into_group('2737393', 'Ф30-401', True)
# DB3.insert_or_drop_pupil_into_group('2737376', 'Ф30-401', True)
# DB3.insert_or_drop_pupil_into_group('2737392', 'Ф50-401', True)
# DB3.insert_or_drop_pupil_into_group('2737376', 'Ф50-401', True)
# DB3.insert_or_drop_pupil_into_group('2733332392', 'Ф50-401', True)
# DB3.request_composition_of_the_group('Ф30-401')
# DB3.request_composition_of_the_group('Ф40-401')
# DB3.request_composition_of_the_group('Ф50-401')
# DB3.insert_or_drop_pupil_into_group('2737393', 'Ф30-401', False)

# DICT = {'ID_ученика': '1222', 'Фамилия_ученика': 'sss', 'Имя_ученика': 'ksdkdskf', 'Отчество_ученика': 'fdkdkfskkd',
#         'Фамилия_родителя': 'sss', 'Имя_родителя': 'ksdkdskf', 'Отчество_родителя': 'ksdkdskf',
#         'Телефон_родителя': '+2212', 'Телефон_ученика': '+23323',
#         'Изучаемые_предметы': 'MATH', 'Тип_обучения': 'ИНД', 'Стоимость_занятия': '2000', 'Статус_обучения': 'AKTIVE'}
# DB1.insert_datas(DICT)

# DB3.add_group('aaa')
# DB3.add_group('bbb')
# DB3.add_group('ccc')

# print(DB3.request_composition_of_the_group('aaa'))

# DB2.request_statistics_at_the_period('15-09-2020 00:00:01', '16-09-2020 00:00:01')

# DB3.create_or_update_table('ГФ1-415-17')

# print(DB1.request_pupils_list('Индивидуальные занятия', 'Активен'))
# print(DB1.request_pupils_list('Индивидуальные занятия', 'Не активен'))
# print(DB1.request_pupils_list('Групповые занятия', 'Активен'))
# print(DB1.request_pupils_list('Групповые занятия', 'Не активен'))

# print(DB2.request_date_and_hours_when_was_pupil('1223'))
# print(DB2.request_payded_dates('1223'))
# print(DB2.request_not_payded_dates_and_debt('1223'))

# print(DB5.request_all_times_for_admin())
# print(DB5.request_available_times_for_parent('3838383'))
# print(DB5.request_individual_schedule_for_pupil('3838383'))
# print(DB5.request_available_times_for_parent('33212232'))
# print(DB5.request_individual_schedule_for_pupil('33212232'))
# print(DB5.request_time_for_all_groups())
# print(DB5.request_time_for_group('Г29-212-333'))
# print(DB5.request_time_for_group('Г55-332-789'))

# DB1.drop_table()
# DB2.drop_table()
# DB3.drop_table()
# DB4.drop_table()
# DB5.drop_table()

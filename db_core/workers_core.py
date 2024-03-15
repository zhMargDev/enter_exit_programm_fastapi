import sqlite3
import os

def select_all_info(table):
    conn = sqlite3.connect('database.db')  # connecting to main database
    cursor = conn.cursor()  # it's a made cursors, it's needed for requests

    # Requested worker
    worker = f"SELECT * FROM {table}"
    cursor.execute(worker)
    row = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()  # this method is close db

    return row
def add_new_worker(data):
    if len(data['mainInfo']['name']) < 1 or len(data['mainInfo']['name']) > 35:
        if data['language'] == 'ru':
            return 'Error: Неверное имя.'
        elif data['language'] == 'am':
            return 'Error: Սխալ անուն։'
        else:
            return 'Error: Invalid name.'
    elif data['mainInfo']['status'] != 'normal' and data['mainInfo']['status'] != 'banned':
        if data['language'] == 'ru':
            return 'Error: Неправильный статус.'
        elif data['language'] == 'am':
            return 'Error: Սխալ ստատուս։'
        else:
            return 'Error: Invalid status.'
    elif type(data['mainInfo']['pin']) != int or data['mainInfo']['pin'] < 100000 or data['mainInfo']['pin'] > 999999:
        if data['language'] == 'ru':
            return 'Error: Неправильный ПИН код.'
        elif data['language'] == 'am':
            return 'Error: Սխալ ՊԻՆ կոդ։'
        else:
            return 'Error: Invalid PIN code.'
    elif data['workingTime']['from'] == '' or data['workingTime']['to'] == '':
        if data['language'] == 'ru':
            return 'Error: Нпраильное время работы.'
        elif data['language'] == 'am':
            return 'Error: Սխալ աշխատանքային ժամեր։'
        else:
            return 'Error: Invalid working time.'
    else:
        try:
            conn = sqlite3.connect('database.db')  # connecting to main database
            cursor = conn.cursor()  # it's a made cursors, it's needed for requests

            # Its needed for checking if pin is unique
            select_pin = f"SELECT * FROM workers"
            cursor.execute(select_pin)
            row = cursor.fetchall()

            for worker in row:
                if worker[1] == data['mainInfo']['pin']:
                    if data['language'] == 'ru':
                        return 'Error: Неправильный ПИН код. Пин код не уникальный.'
                    elif data['language'] == 'am':
                        return 'Error: Սխալ ՊԻՆ կոդ։ ՊԻՆ կոդը յուրահատուկ չի։'
                    else:
                        return 'Error: Invalid pin code. Pin code is not unique.'

            #If the pin is not unique, then the program will stop and return the error text, otherwise it will continue to work and change all the values.

            # Requested worker
            worker_info = "INSERT INTO workers (pin, status, workerName) VALUES (?, ?, ?)"
            new_values = (data['mainInfo']['pin'], data['mainInfo']['status'], data['mainInfo']['name'])
            cursor.execute(worker_info, new_values)

            # Select added worker
            worker = f"SELECT id FROM workers WHERE pin = {data['mainInfo']['pin']}"
            cursor.execute(worker)
            row = cursor.fetchone()


            # Add worker's working time
            new_working_time = "INSERT INTO workingTimes (workerId, workingTimeFrom, workingTimeTo) VALUES (?, ?, ?)"
            new_values = (row[0], data['workingTime']['from'], data['workingTime']['to'])
            cursor.execute(new_working_time, new_values)

            # Add banned week days
            for day in data['bannedWeekDays']:
                new_week_days = f"INSERT INTO bannedWeeks (workerId, bannedDay) VALUES (?, ?)"
                new_values = (row[0], day)
                cursor.execute(new_week_days, new_values)

            # Add new banned days
            for date in data['bannedDays']:
                new_date = f"INSERT INTO bannedDays (workerId, bannedData) VALUES (?, ?)"
                new_values = (row[0], date)
                cursor.execute(new_date, new_values)

            conn.commit()
            cursor.close()
            conn.close()

            return row[0]
        except sqlite3.OperationalError:
            if data['language'] == 'ru':
                return 'Error: Проблемы с сервером.'
            elif data['language'] == 'am':
                return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
            else:
                return 'Error: Problem with Server.'

def change_worker_info(data):
    #Change worker's main information
    language = data['len']
    if type(data['mainInfo']['id']) != int:
        if language == 'ru':
            return 'Error: Неверный id.'
        elif language == 'am':
            return 'Error: Սխալ id։'
        else:
            return 'Error: Invalid id.'
    elif len(data['mainInfo']['name']) < 1 or len(data['mainInfo']['name']) > 35:
        if language == 'ru':
            return 'Error: Неверный имя.'
        elif language == 'am':
            return 'Error: Սխալ անուն։'
        else:
            return 'Error: Invalid name.'
    elif data['mainInfo']['status'] != 'normal' and data['mainInfo']['status'] != 'banned':
        if language == 'ru':
            return 'Error: Неверный статус.'
        elif language == 'am':
            return 'Error: Սխալ կարգավիճակ (ստատուս)։.'
        else:
            return 'Error: Invalid status.'
    elif type(data['mainInfo']['pin']) != int or data['mainInfo']['pin'] < 100000 or data['mainInfo']['pin'] > 999999:
        if language == 'ru':
            return 'Error: Неверный ПИН код.'
        elif language == 'am':
            return 'Error: Սխալ ՊԻՆ կոդ։'
        else:
            return 'Error: Invalid PIN code.'
    elif data['workingTime']['from'] == '' or data['workingTime']['to'] == '':
        if language == 'ru':
            return 'Error: Неверный время работы.'
        elif language == 'am':
            return 'Error: Սխալ աշխատանքային ժամեր։'
        else:
            return 'Error: Invalid working time.'
    else:
        try:
            conn = sqlite3.connect('database.db')  # connecting to main database
            cursor = conn.cursor()  # it's a made cursors, it's needed for requests

            # Its needed for checking if pin is unique
            select_pin = f"SELECT * FROM workers"
            cursor.execute(select_pin)
            row = cursor.fetchall()

            for worker in row:
                if worker[0] != data['mainInfo']['id'] and worker[1] == data['mainInfo']['pin']:
                    if language == 'ru':
                        return 'Error: Неверный ПИН код. ПИН код не уникальный.'
                    elif language == 'am':
                        return 'Error: Սխալ ՊԻՆ կոդ։ ՊԻՆ կոդը յուրահատուկ չէ։'
                    else:
                        return 'Error: Invalid PIN code. PIN code is not unique.'

            #If the pin is not unique, then the program will stop and return the error text, otherwise it will continue to work and change all the values.

            # Requested worker
            worker_info = "UPDATE workers SET pin = ?, status = ?, workerName = ? WHERE id = ?"
            new_values = (data['mainInfo']['pin'], data['mainInfo']['status'], data['mainInfo']['name'], data['mainInfo']['id'])
            cursor.execute(worker_info, new_values)

            # Deleting old working time
            deleting_working_time = f"DELETE FROM workingTimes where workerId = {data['mainInfo']['id']}"
            cursor.execute(deleting_working_time)
            # Add worker's working time
            new_working_time = "INSERT INTO workingTimes (workerId, workingTimeFrom, workingTimeTo) VALUES (?, ?, ?)"
            new_values = (data['mainInfo']['id'], data['workingTime']['from'], data['workingTime']['to'])
            cursor.execute(new_working_time, new_values)

            # Deleting old banned week days
            old_week_days = f"DELETE FROM bannedWeeks WHERE workerId = {data['mainInfo']['id']}"
            cursor.execute(old_week_days)
            # Add banned week days
            for day in data['bannedWeekDays']:
                new_week_days = f"INSERT INTO bannedWeeks (workerId, bannedDay) VALUES (?, ?)"
                new_values = (data['mainInfo']['id'], day)
                cursor.execute(new_week_days, new_values)

            # Deleting old banned days
            old_banned_days = f"DELETE FROM bannedDays WHERE workerId = {data['mainInfo']['id']}"
            cursor.execute(old_banned_days)
            # Add new banned days
            for date in data['bannedDays']:
                new_date = f"INSERT INTO bannedDays (workerId, bannedData) VALUES (?, ?)"
                new_values = (data['mainInfo']['id'], date)
                cursor.execute(new_date, new_values)

            conn.commit()
            cursor.close()
            conn.close()

            if language == 'ru':
                return f"ID:{data['mainInfo']['id']} Информация работника было обнавлено."
            elif language == 'am':
                return f"ID:{data['mainInfo']['id']} Աշխատողի տվյալների փոփոխված են։"
            else:
                return f"ID:{data['mainInfo']['id']} Worker information updated."
        except sqlite3.OperationalError:
            if language == 'ru':
                return 'Error: Проблемы с сервером.'
            elif language == 'am':
                return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
            else:
                return 'Error: Problem with Server.'

def delete_worker(data):
    language = data[1]

    try:
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        # Delete worker
        del_worker = f"DELETE FROM workers where id = {data[0]}"
        cursor.execute(del_worker)

        # Deleting old working time
        deleting_working_time = f"DELETE FROM workingTimes where workerId = {data[0]}"
        cursor.execute(deleting_working_time)

        # Deleting old banned week days
        old_week_days = f"DELETE FROM bannedWeeks WHERE workerId = {data[0]}"
        cursor.execute(old_week_days)

        # Deleting old banned days
        old_banned_days = f"DELETE FROM bannedDays WHERE workerId = {data[0]}"
        cursor.execute(old_banned_days)
        # Add new banned days

        conn.commit()
        cursor.close()
        conn.close()

        if language == 'ru':
            return 'Информация работника удалена.'
        elif language == 'am':
            return 'Աշխատողի տվյալները ջնջված են։'
        else:
            return "Worker's information is Deleted."
    except sqlite3.OperationalError:
        if language == 'ru':
            return 'Error: Проблемы с сервером.'
        elif language == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'

def global_change_workers_time(data):
    try:
        #This function is change all workers working time
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        #Delete all workgin times for all workers
        delete_query = "DELETE FROM workingTimes"
        cursor.execute(delete_query)

        #Select all workers ids, for adding new working times
        workers_id = 'SELECT id FROM workers'
        cursor.execute(workers_id)
        all_workers_ids = cursor.fetchall()

        new_working_time = "INSERT INTO workingTimes (workerId, workingTimeFrom, workingTimeTo) VALUES (?, ?, ?)"
        for worker_id in all_workers_ids:
            new_values = (worker_id[0], data[0], data[1])
            cursor.execute(new_working_time, new_values)

        conn.commit()
        cursor.close()
        conn.close()

        if data[2] == 'ru':
            return 'Время работы всех рабочих было изменено.'
        elif data[2] == 'am':
            return 'Բոլոր աշխատողների աշխատանքային ժամերը փոփոխված են։'
        else:
            return 'New working time is changed for all workers.'
    except sqlite3.OperationalError:
        if data[2] == 'ru':
            return 'Error: Проблемы с сервером.'
        elif data[2] == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'

def remove_all_weekends(language):
    try:
        #Deleting all worker's weekends
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        #Deleting all weekends for all workers
        delete_weekends = f"DELETE FROM bannedWeeks"
        cursor.execute(delete_weekends)

        conn.commit()
        cursor.close()
        conn.close()

        if language == 'ru':
            return 'Все выходные были удалены.'
        elif language == 'am':
            return 'Բոլոր հանգստյան օրերը ջնջված են։'
        else:
            return 'All weekends are deleted.'
    except sqlite3.OperationalError:
        if language == 'ru':
            return 'Error: Проблемы с сервером.'
        elif language == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'

def remove_all_dates(language):
    try:
        #Deleting all worker's non working dates
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        #Deleting all non-working dates for all workers
        delete_dates = f"DELETE FROM bannedDays"
        cursor.execute(delete_dates)

        conn.commit()
        cursor.close()
        conn.close()

        if language == 'ru':
            return 'Все выходные дни были удалены.'
        elif language == 'am':
            return 'Բոլոր ազաը օրերը ջնջված են։'
        else:
            return 'All holidays are deleted.'
    except sqlite3.OperationalError:
        if language == 'ru':
            return 'Error: Проблемы с сервером.'
        elif language == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'

def add_weekend_for_all_workers(data):
    try:
        #Add weekends for all workers
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        # Selecting all workers ids
        select_all_workers_ids = "SELECT id FROM workers"
        cursor.execute(select_all_workers_ids)
        workers_id = cursor.fetchall()

        #Try is needed because the program stops if it does not find rows in the database.
        try:
            # Removing early weekends workers that were selected by the administrator so as not to check their availability.
            remove_choosed_weekends = f"DELETE FROM bannedWeeks"
            cursor.execute(remove_choosed_weekends)
        except:
            pass
        for day in data[0]:
            #Add weekend for all workers
            for worker_id in workers_id:
                insert_weekend = f"INSERT INTO bannedWeeks(workerId, bannedDay) VALUES (?, ?)"
                new_values = (worker_id[0], day)
                cursor.execute(insert_weekend, new_values)

        conn.commit()
        cursor.close()
        conn.close()

        #If res True, it meens that function is responsed from main py file
        if data[1] == 'ru':
            return "Выходные были добавлены."
        elif data[1] == 'am':
            return "Հանգստյան օրերը ավելացված են։"
        else:
            return "Weekends added for all workers."
    except sqlite3.OperationalError:
        if data[1] == 'ru':
            return 'Error: Проблемы с сервером.'
        elif data[1] == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'

def add_date_for_all_workers(data):
    try:
        # Add weekends for all workers
        conn = sqlite3.connect('database.db')  # connecting to main database
        cursor = conn.cursor()  # it's a made cursors, it's needed for requests

        # Selecting all workers ids
        select_all_workers_ids = "SELECT id FROM workers"
        cursor.execute(select_all_workers_ids)
        workers_id = cursor.fetchall()

        try:
            # Removing early weekends workers that were selected by the administrator so as not to check their availability.
            remove_choosed_weekends = f"DELETE FROM bannedDays"
            cursor.execute(remove_choosed_weekends)
        except:
            pass

        for date in data[0]:
            # Add weekend for all workers
            for worker_id in workers_id:
                insert_weekend = f"INSERT INTO bannedDays(workerId, bannedData) VALUES (?, ?)"
                new_values = (worker_id[0], date)
                cursor.execute(insert_weekend, new_values)

        conn.commit()
        cursor.close()
        conn.close()

        # If res True, it meens that function is responsed from main py file
        if data[1] == 'ru':
            return "Выходные дни были добавлены для всех пользователей."
        elif data[1] == 'am':
            return "Ազատ օրերը ավելացված են բոլոր աշխատողների համար։"
        else:
            return "Holidays added for all workers."
    except sqlite3.OperationalError:
        if data[1] == 'ru':
            return 'Error: Проблемы с сервером.'
        elif data[1] == 'am':
            return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
        else:
            return 'Error: Problem with Server.'
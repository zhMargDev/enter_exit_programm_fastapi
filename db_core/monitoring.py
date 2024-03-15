import sqlite3
import datetime


def worker_pin_request(data):
    #Worker's request for entering or exiting
    language = data[1]

    if type(data[0]) == str:
        if language == 'ru':
            return 'Error: Неправильный ПИН Код.'
        elif language == 'am':
            return 'Error: Սխալ ՊԻՆ Կոդ։'
        else:
            return 'Error: Invalid PIN Code.'
    else:
        try:
            conn = sqlite3.connect('database.db')  # connecting to main database
            cursor = conn.cursor()  # it's a made cursors, it's needed for requests

            # Select worker
            select_worker_id = f"SELECT * FROM workers WHERE pin = {data[0]}"
            cursor.execute(select_worker_id)
            worker = cursor.fetchone()

            #If pin code is wrong, return this message
            if worker == None:
                if language == 'ru':
                    return 'Error: Неправильный ПИН Код.'
                elif language == 'am':
                    return 'Error: Սխալ ՊԻՆ Կոդ։'
                else:
                    return 'Error: Invalid PIN Code.'

            #Checking worker's status
            if worker[2] == 'banned':
                if language == 'ru':
                    return 'Error: У вас нету доступа, обратитесь к вашему системному администратору.'
                elif language == 'am':
                    return 'Error: Դուք մուտք չունեք, դիմեք ձեր սիստեմ ադմինիստրատորին:'
                else:
                    return 'Error: You do not have access, contact your system administrator.'


            # Select working time for worker
            select_worker_working_time = f"SELECT * FROM workingTimes WHERE workerId = {worker[0]}"
            cursor.execute(select_worker_working_time)
            working_time = cursor.fetchone()

            if working_time == None:
                if language == 'ru':
                    return 'Error: Возникла проблема с вашей учетной записью. Обратитесь к системному администратору.'
                elif language == 'am':
                    return 'Error: Ձեր հաշվի հետ կապված խնդիր կան, խնդրում ենք կապվել ձեր սիստեմ ադմինիստրատորի հետ:'
                else:
                    return "Error: There is a problem with your account, please contact your system administrator."

            # Select weekends
            select_weekends = f"SELECT * FROM bannedWeeks WHERE workerId = {worker[0]}"
            cursor.execute(select_weekends)
            weekends_arr = cursor.fetchall()

            #Checking if today is working day or weekend
            #Week days 0-6 mon-sun
            week_day_now = datetime.date.today().weekday()
            # Changing selected weekends to numbers (weekday() get now in number from 0-6)
            weekends = [{"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}[day[2]] for day in weekends_arr]
            for weekend in weekends:
                if weekend == week_day_now:
                    if language == 'ru':
                        return 'Error: Сегодня ваш выходной.'
                    elif language == 'am':
                        return 'Error: Այսօր ձեր հանգստյան օրն է:'
                    else:
                        return "Error: Today is your weekend."

            # Get date now
            date_now = datetime.datetime.now().strftime("%Y-%m-%d")

            # Select worker's holiays or non working days
            select_holidays = f"SELECT * FROM BannedDays WHERE workerId = {worker[0]}"
            cursor.execute(select_holidays)
            holidays = cursor.fetchall()

            for holiday in holidays:
                if holiday[2] == date_now:
                    if language == 'ru':
                        return 'Error: Сегодня для вас не рабочий день.'
                    elif language == 'am':
                        return 'Error: Այսօր ձեր համար ազատ օր է:'
                    else:
                        return "Error: Today is not a working day for you."

            # Get time and date
            time_now = datetime.datetime.now().strftime("%H:%M")

            select_workers_monitoring = f"SELECT * FROM monitoring WHERE pin = {data[0]}"
            cursor.execute(select_workers_monitoring)
            monitoring_rows = cursor.fetchall()

            # Insert into monitoring entering
            if time_now < working_time[2] and monitoring_rows[-1][5] == 'exiting' or time_now > working_time[3] and monitoring_rows[-1][5] == 'exiting':
                if language == 'ru':
                    return 'Error: Сейчас не рабочее время.'
                elif language == 'am':
                    return 'Error: Հիմա աշխատանքային ժամ չէ:'
                else:
                    return "Error: It's not working hours."
            else:
                if len(monitoring_rows) == 0 or monitoring_rows[-1][5] == 'exiting':
                    if len(monitoring_rows) != 0:
                        if date_now == monitoring_rows[-1][4]:
                            if language == 'ru':
                                return 'Error: Вы можете зайти на работу только 1 раз в сутки..'
                            elif language == 'am':
                                return 'Error: Դուք կարող եք մուտք գործել աշխատանք միայն 1 անգամ օրվա ընթացքում:'
                            else:
                                return "Error: You can only enter work once per day."

                    #late is the time that means sleep how late the worker was
                    # lating
                    # Split the working time and current time into hours and minutes
                    working_hours, working_minutes = working_time[2].split(":")
                    current_hours, current_minutes = time_now.split(":")

                    # Convert hours and minutes to integers
                    working_hours = int(working_hours)
                    working_minutes = int(working_minutes)
                    current_hours = int(current_hours)
                    current_minutes = int(current_minutes)

                    # Calculate the difference in minutes
                    minutes_diff = (current_hours * 60 + current_minutes) - (working_hours * 60 + working_minutes)

                    # Handle negative difference (worker came in early)
                    if minutes_diff < 0:
                        minutes_diff = 0  # Consider worker on time if they came in early

                    # Print the difference in a readable format (hours:minutes)
                    hours_late = minutes_diff // 60
                    minutes_late = minutes_diff % 60

                    late_time = f'{hours_late}:{minutes_late}'

                    recycling_time = '00:00'

                    # Insert into monitoring entering
                    insert_monitoring = f"INSERT INTO monitoring (pin, workerName, time, date, type, late, recycling) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    new_values = (data[0], worker[3], time_now, date_now, 'entering', late_time, recycling_time)
                    cursor.execute(insert_monitoring, new_values)

                    conn.commit()
                    cursor.close()
                    conn.close()

                    if language == 'ru':
                        return 'Добро пожаловать.'
                    elif language == 'am':
                        return 'Բարի գալուստ:'
                    else:
                        return "Welcome."
                elif monitoring_rows[-1][5] == 'entering':
                    # recycling
                    #It is checked if the worker left before his final work time, then the time is added to the database, which means how much he did not finish working
                    if working_time[3] > time_now:
                        working_hours, working_minutes = working_time[3].split(":")
                    else:
                        working_hours, working_minutes = working_time[2].split(':')

                    # Split the working time and current time into hours and minutes
                    current_hours, current_minutes = time_now.split(":")

                    # Convert hours and minutes to integers
                    working_hours = int(working_hours)
                    working_minutes = int(working_minutes)
                    current_hours = int(current_hours)
                    current_minutes = int(current_minutes)

                    # Calculate the difference in minutes
                    minutes_diff = (working_hours * 60 + working_minutes) - (current_hours * 60 + current_minutes)

                    # Print the difference in a readable format (hours:minutes)
                    hours_late = minutes_diff // 60
                    minutes_late = minutes_diff % 60

                    if working_time[3] > time_now:
                        recycling_time = f'-{hours_late}:{minutes_late}'
                    else:
                        recycling_time = f'{hours_late}:{minutes_late}'

                    late_time = '00:00'

                    # Insert into monitoring entering
                    insert_monitoring = f"INSERT INTO monitoring (pin, workerName, time, date, type, late, recycling) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    new_values = (data[0], worker[3], time_now, date_now, 'exiting', late_time, recycling_time)
                    cursor.execute(insert_monitoring, new_values)

                    conn.commit()
                    cursor.close()
                    conn.close()

                    if language == 'ru':
                        return 'До свидания. Хорошего дня.'
                    elif language == 'am':
                        return 'Ցտեսություն։ Լավ օր եմ մաղթում։'
                    else:
                        return "Goodbye. Have a good day."
        except sqlite3.OperationalErrorf:
            if language == 'ru':
                return 'Error: Возникла проблема с вашей учетной записью. Обратитесь к системному администратору.'
            elif language == 'am':
                return 'Error: Ձեր հաշվի հետ կապված խնդիր կան, խնդրում ենք կապվել ձեր սիստեմ ադմինիստրատորի հետ:'
            else:
                return "Error: There is a problem with your account, please contact your system administrator."

def selecting_all_monitoring():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    select_monitoring = "SELECT * FROM monitoring"
    cursor.execute(select_monitoring)
    monitoring_arr = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return list(reversed(monitoring_arr))
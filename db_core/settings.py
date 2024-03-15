import sqlite3
import re

def check_ip(device_ip, device_type):
    try:
        # This method is check if client ip is in database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Select all ip addresses from ip registry
        select_ips = "SELECT * FROM registry"
        cursor.execute(select_ips)
        ip_addreses = cursor.fetchall()

        # If ip registry is empty add first requested device ip
        if len(ip_addreses) == 0:
            insert_device('administrator', device_ip)
            return True
        else:
            #Checking if requested device ip addres is in databse's registru, return True else return false
            for ip_addr in ip_addreses:
                if ip_addr[1] == device_type and ip_addr[2] == device_ip or ip_addr[1] == 'administrator' and ip_addr[2] == device_ip:
                    return True
            return False

        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.OperationalError:
        return 'Error: 500.'

def select_all_regisctry():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    select_registry = "SELECT * FROM registry"
    cursor.execute(select_registry)
    registry = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return registry

def insert_device(device_type, device_ip):
    try:
        # This method is check if client ip is in database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # If ip registry is empty add first requested device ip
        inserting = f"INSERT INTO registry (deviceType, deviceIp) VALUES (?, ?)"
        values = (device_type, device_ip)
        cursor.execute(inserting, values)

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except sqlite3.OperationalError:
        return False
def validate_ip(ip):
    #Checking if ip == IPv4
    # if ip == IPv4 return True else return False
    regex = re.compile(r"^((25[0-5]|2[0-4]\d|[0-1]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[0-1]?\d\d?)$")
    return regex.match(ip)
def add_new_avialable_device(data):
    #Checking if deviceType is true and deviceIp is IPv4 format
    if data['deviceType'] == "administrator" and validate_ip(data['deviceIp']) or data['deviceType'] == 'user' and validate_ip(data['deviceIp']):
        #Check if this ip is already registred
        array = select_all_regisctry()

        # If IP address is already added return error
        for item in array:
            if item[1] == data['deviceType'] and item[2] == data['deviceIp']:
                if data['language'] == 'ru':
                    return "Error: Этот IP адрс уже добавлен."
                elif data['language'] == 'am':
                    return "Error: Այս IP հասցեն արդեն ավելացված է։"
                else:
                    return "Error: This IP Address is already added."

        # else insert it
        inserting_response = insert_device(data['deviceType'], data['deviceIp'])

        #If inserting is denied
        if inserting_response == False:
            if data['language'] == 'ru':
                return 'Error: Проблемы с сервером.'
            elif data['language'] == 'am':
                return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
            else:
                return 'Error: Problem with Server.'

        if data['language'] == 'ru':
            return 'Устройство было добавлено.'
        elif data['language'] == 'am':
            return 'Սարքեը ավելացված է։'
        else:
            return "Device is added."
    else:
        if data['language'] == 'ru':
            return 'Error: Неправильный тип устройства.'
        elif data['language'] == 'am':
            return 'Error: Սարքավորման սխալ տեսակ։'
        else:
            return "Error: Invalid type of device."


def registry_delete_device(data, request_device_ip):
    #Checking fi responsed ip is IPv4 and device type is administrator or user
    if data['deviceType'] == "administrator" and validate_ip(data['deviceIp']) or data['deviceType'] == 'user' and validate_ip(data['deviceIp']):
        select_all = select_all_regisctry()

        #This flag check if requested data is in db
        flag = False
        for element in select_all:
            if element[1] == data['deviceType'] and element[2] == data['deviceIp']:
                flag = True
                # Check if removed ip is IP of device, which requested, and if it true return error
                if element[2] == request_device_ip:
                    if data['language'] == 'ru':
                        return 'Error: Вы не можете удалить чвой IP адрес.'
                    elif data['language'] == 'am':
                        return 'Error: Դուք չեք կարող ջնջել ձեր IP հասցեն։'
                    else:
                        return 'Error: You cannot delete your IP.'
                break

        if flag == False:
            if data['language'] == 'ru':
                return 'Error: Неверный IP адрес или тип устройства. В реестре совпадений не найдено.'
            elif data['language'] == 'am':
                return 'Error: Անվավեր IP հասցե կամ սարքի տեսակ: Ռեյեստրում համընկնումներ չեն գտնվել։'
            else:
                return 'Error: Invalid IP or Device Type. No matches were found in the registry.'
        else:
            try:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                deleteing = 'DELETE FROM registry WHERE deviceType = ? and deviceIp = ?'
                values = (data['deviceType'], data['deviceIp'])
                cursor.execute(deleteing, values)

                conn.commit()
                cursor.close()
                conn.close()

                if data['language'] == 'ru':
                    return 'Устройство было удалено.'
                elif data['language'] == 'am':
                    return 'Սարքեը ջնջված է։'
                else:
                    return "Device is deleted."
            except sqlite3.OperationalError:
                if data['language'] == 'ru':
                    return 'Error: Проблемы с сервером.'
                elif data['language'] == 'am':
                    return 'Error: Կան խնդիրներ սերվերի հետ կապված։'
                else:
                    return 'Error: Problem with Server.'
    else:
        if data['language'] == 'ru':
            return 'Error: Неправильный тип устройства.'
        elif data['language'] == 'am':
            return 'Error: Սարքավորման սխալ տեսակ։'
        else:
            return "Error: Invalid type of device."
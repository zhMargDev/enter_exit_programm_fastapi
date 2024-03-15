from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import socket

import db_core.workers_core as workers_core
import db_core.monitoring as monitoring
import db_core.settings as settings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    #Cehcking if requested ip is in registry
    language = 'en'
    if '?ln=ru' in str(request.url):
        language = 'ru'
    elif '?ln=am' in str(request.url):
        language = 'am'

    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'user')

    if respond_ip_check == True:
        try:
            return templates.TemplateResponse("pin_form.html", {"request": request, 'checker_flag': 'True', 'language': language})
        except Exception as e:
            return templates.TemplateResponse("pin_form.html", {"request": request, 'checker_flag': 'False', 'language': language})
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

@app.get("/error_ip", response_class=HTMLResponse)
async def error_ip(request: Request):
    device_ip = request.client.host
    return templates.TemplateResponse('error_ip.html', {"request": request, 'device_ip': device_ip})

@app.get("/administrator", response_class=HTMLResponse)
async def admin_panel(request: Request):
    #Cehcking if requested ip is in registry
    language = 'en'
    if '?ln=ru' in str(request.url):
        language = 'ru'
    elif '?ln=am' in str(request.url):
        language = 'am'
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == 'Error: 500.':
        return templates.TemplateResponse("admin_panel.html", {"request": request, 'checker_flag': 'False', 'language': language})
    elif respond_ip_check == True:
        try:
            workers = workers_core.select_all_info('workers')
            workingTimes = workers_core.select_all_info('workingTimes')
            bannedWeekDays = workers_core.select_all_info('bannedWeeks')
            allWeekDays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            bannedDates = workers_core.select_all_info('bannedDays')

            #Registry responsed 2 times, when programm have u bug
            #When sending 1 time, it is not possible to display data 2 times
            #There won't be a lot of data so it won't affect performance
            registry = settings.select_all_regisctry()
            registry_user = reversed(registry)
            data = {
                'workers': reversed(workers),
                'workingTimes': workingTimes,
                'bannedWeekDays': bannedWeekDays,
                'bannedDates': bannedDates,
                'registry': reversed(registry),
                'registry_user': registry_user
            }
            return templates.TemplateResponse("admin_panel.html", {"request": request, 'data': data, 'checker_flag': 'True', 'language': language})
        except Exception as e:
            return templates.TemplateResponse("admin_panel.html", {"request": request, 'checker_flag': 'False', 'language': language})
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Select all monitoring datas
@app.post("/administrator/selecting_all_monitoring")
async def selecting_all_monitoring(request: Request):
    flag = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:
        if flag == 'true':
            returned_data = monitoring.selecting_all_monitoring()

            return {"success": True, 'message': returned_data}
        else:
            return 'False'
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Send pin code to server from worker
@app.post("/worker_pin_request")
async def worker_pin_request(request: Request):
    pin_code = await request.json()

    returned_info = monitoring.worker_pin_request(pin_code)

    return {"success": True, 'message': returned_info}

#This function is tak post data from ajax response, for changing wroker's information
@app.post("/administrator/change_worker_info")
async def change_worker_info(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.change_worker_info(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#This function is tak post data from ajax response, for adding new worker
@app.post("/administrator/add_new_worker")
async def add_new_worker(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.add_new_worker(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Deleting worker by his id
@app.post("/administrator/delete_worker")
async def delete_worker(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.delete_worker(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Change workign time for all workers
@app.post("/administrator/global_change_workers_time")
async def global_change_workers_time(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.global_change_workers_time(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Delete all worker's weekends
@app.post("/administrator/remove_all_weekends")
async def remove_all_weekends(request: Request):
    language = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.remove_all_weekends(language)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Delete all worker's working dates
@app.post("/administrator/remove_all_dates")
async def remove_all_dates(request: Request):
    language = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.remove_all_dates(language)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Add weekends for all workers
@app.post("/administrator/add_weekend_for_all_workers")
async def add_weekend_for_all_workers(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.add_weekend_for_all_workers(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Add banned dates for all workers
@app.post("/administrator/add_date_for_all_workers")
async def add_date_for_all_workers(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = workers_core.add_date_for_all_workers(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Add new avialable device to registry
@app.post("/administrator/add_new_avialable_device")
async def add_new_avialable_device(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = settings.add_new_avialable_device(data_array)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)

#Delete device from registry by ip and device type admin or user
@app.post('/administrator/registry_delete_device')
async def registry_delete_device(request: Request):
    data_array = await request.json()

    #Cehcking if requested ip is in registry
    device_ip = request.client.host
    respond_ip_check = settings.check_ip(device_ip, 'administrator')

    if respond_ip_check == True:

        returned_info = settings.registry_delete_device(data_array, device_ip)

        return {"success": True, 'message': returned_info}
    else:
        return RedirectResponse(url='/error_ip', status_code=302)
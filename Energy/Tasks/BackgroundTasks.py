from celery import shared_task
import time
from Energy.db import Hello, AddUser, AddUserCloudCredentials, UserExists, GetUser, AddDeviceData, GetAllEmails, GetDataFor, AddDeviceData, GetUsageDataFor
import datetime
from Energy.SwitchBotCloudInterface import GetDevicesFromSwitchBot, GetDeviceStatusFromSwitchBot
import time

from Energy.RemoteDataHandler import RemoteDataHandler
import os
import matplotlib.pyplot as plt


def ReformatDate(date_list):
    new_date_list = []
    for date in date_list:
        day = date.split(",")[0]
        time = date.split(",")[1]

        day = day.split("/")
        time = time.split(":")

        new_date = f"{day[0]}/{day[1]} {time[0]}:{time[0]}"

        new_date_list.append(new_date)

    return new_date_list



# def DrawSingleGraph(X, Y, x_label, y_label, title, save_dir):
#     plt.figure()
#     plt.plot(X, Y)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.title(title)

#     plt.savefig(save_dir)

# def DrawGraphs(email, data):
#     RDH = RemoteDataHandler()

#     for device_id in data["devices"]:
#         dates = data["devices"][device_id]["data"]["date"]
#         voltage_list = data["devices"][device_id]["data"]["voltage"]
#         current_list = data["devices"][device_id]["data"]["current"]
#         energy_list = data["devices"][device_id]["data"]["energy"]
#         power_list = data["devices"][device_id]["data"]["power"]

#         dates = ReformatDate(dates)

#         voltage_public_id = f"{email}-{device_id}-voltage"
#         voltage_graph_dir = os.path.join(GRAPHS_DIR, voltage_public_id + ".png")
#         DrawSingleGraph(dates, voltage_list, "Dates", "Voltage (v)", "Voltage Graph", voltage_graph_dir)
#         RDH.UploadToCloud(voltage_graph_dir, voltage_public_id, resource_type = "image")

#         current_public_id = f"{email}-{device_id}-current"
#         current_graph_dir = os.path.join(GRAPHS_DIR, current_public_id + ".png")
#         DrawSingleGraph(dates, current_list, "Dates", "Current (A)", "Current Graph", current_graph_dir)
#         RDH.UploadToCloud(current_graph_dir, current_public_id, resource_type = "image")

#         power_public_id = f"{email}-{device_id}-power"
#         power_graph_dir = os.path.join(GRAPHS_DIR, power_public_id + ".png")
#         DrawSingleGraph(dates, power_list, "Dates", "Power (W)", "Power Graph", power_graph_dir)
#         RDH.UploadToCloud(power_graph_dir, power_public_id, resource_type = "image")


#         energy_public_id = f"{email}-{device_id}-energy"
#         energy_graph_dir = os.path.join(GRAPHS_DIR, energy_public_id + ".png")
#         DrawSingleGraph(dates, energy_list, "Dates", "Energy (Wh)", "Energy Graph", energy_graph_dir)
#         RDH.UploadToCloud(energy_graph_dir, energy_public_id, resource_type = "image")


#     time.sleep(2)
#     for device_id in data["devices"]:
#         voltage_public_id = f"{email}-{device_id}-voltage"
#         voltage_graph_dir = os.path.join(GRAPHS_DIR, voltage_public_id + ".png")

#         current_public_id = f"{email}-{device_id}-current"
#         current_graph_dir = os.path.join(GRAPHS_DIR, current_public_id + ".png")

#         power_public_id = f"{email}-{device_id}-power"
#         power_graph_dir = os.path.join(GRAPHS_DIR, power_public_id + ".png")


#         energy_public_id = f"{email}-{device_id}-energy"
#         energy_graph_dir = os.path.join(GRAPHS_DIR, energy_public_id + ".png")

#         os.remove(voltage_graph_dir)
#         os.remove(current_graph_dir)
#         os.remove(power_graph_dir)
#         os.remove(energy_graph_dir)


@shared_task(ignore_result=False)
def HelloWorld():
    for i in range(1, 6):
        print(i)
        time.sleep(1)

    print("Hello Celery")

@shared_task(ignore_result=False)
def GetDevicesData():
    all_emails = GetAllEmails()

    if len(all_emails) > 0:
        date_time_str = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        t = int(round(time.time() * 1000))
        for email in all_emails:
            data = GetDataFor(email)
            if data is not None:
                if data["cloud_credentials"] is not None:
                    secret = data["cloud_credentials"]["secret"]
                    token = data["cloud_credentials"]["token"]
                    devices = data["devices"]

                    for device in devices:
                        params = GetDeviceStatusFromSwitchBot(token, secret, device["deviceId"], t)

                        if params is not None:
                            voltage, current, upTime, power = params
                            AddDeviceData(email, device["deviceId"], date_time_str, voltage, current, upTime, power)

                    # data = GetUsageDataFor(email)
                    # DrawGraphs(email, data)
#!/usr/bin/python3

from enum import Enum
import pyteslaapi.common as common
import requests

# define constants
API_URL = "https://owner-api.teslamotors.com/api/1/vehicles"

class State(Enum):
    ASLEEP = "asleep"
    ONLINE = "online"

# container for details about single vehicle
class Vehicle:
    def __init__(self):
        self.name = None
        self.id = None
        self.vin = None
        self.state = None
        self.in_service = None

    # prints all details for vehicle
    def __str__(self):
        return """\r\n\
    name:       {}\r\n\
    id:         {}\r\n\
    vin:        {}\r\n\
    state:      {}\r\n\
    in_service: {}\r\n\
    """.format(self.name, self.id, self.vin, self.state, self.in_service)

# uses headers with access token to obtain list of vehicles
class Vehicles:
    def __init__(self, headers):
        self.headers = headers
        self.vehicle_list = []

    def send_list_request(self):
        # send request to get response with list of vehicles
        result = requests.get(API_URL, headers=self.headers)
        response = common.handle_result(result)
        if response:
            # store details of each vehicle in list
            self.vehicle_list = []
            for item in response["response"]:
                vehicle = Vehicle()
                vehicle.name = item["display_name"]
                vehicle.id = item["id"]
                vehicle.vin = item["vin"]
                vehicle.state = State(item["state"])
                vehicle.in_service = item["in_service"]
                self.vehicle_list.append(vehicle)

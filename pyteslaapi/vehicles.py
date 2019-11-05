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
    def __init__(self, headers):
        self.headers = headers
        self.name = None
        self.id = None
        self.vin = None
        self.state = None
        self.in_service = None

    # prints all details for vehicle
    def __str__(self):
        return """\
    name:       {}\r\n\
    id:         {}\r\n\
    vin:        {}\r\n\
    state:      {}\r\n\
    in_service: {}""".format(self.name, self.id, self.vin, self.state, self.in_service)

    def update(self, response_item):
        self.name = response_item["display_name"]
        self.id = response_item["id"]
        self.vin = response_item["vin"]
        self.state = State(response_item["state"])
        self.in_service = response_item["in_service"]

    def send_wake_up_request(self):
        # send request to wake up specific vehicle
        URL = API_URL + "/{}/wake_up".format(self.id)
        result = requests.post(URL, headers=self.headers)
        response = common.handle_result(result)
        if response:
            # update vehicle with response fields
            self.update(response["response"])

    def send_vehicle_data_request(self):
        # send request to get response with all data for specific vehicle
        URL = API_URL + "/{}/vehicle_data".format(self.id)
        result = requests.get(URL, headers=self.headers)
        response = common.handle_result(result)
        if response:
            # TODO: handle all data in response
            print(response)

# uses headers with access token to obtain list of vehicles
class Vehicles:
    def __init__(self, headers):
        self.headers = headers
        self.vehicle_map = {}

    def get_vehicle(self, index):
        id = list(self.vehicle_map)[index]
        return self.vehicle_map[id]

    def send_list_request(self):
        # send request to get response with list of vehicles
        result = requests.get(API_URL, headers=self.headers)
        response = common.handle_result(result)
        if response:
            # clear and store details of each vehicle
            self.vehicle_map = {}
            for item in response["response"]:
                vehicle = Vehicle(self.headers)
                vehicle.update(item)
                self.vehicle_map[str(vehicle.id)] = vehicle

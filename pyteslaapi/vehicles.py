#!/usr/bin/python3

import requests

# define constants
API_URL = "https://owner-api.teslamotors.com/api/1/vehicles"

# uses headers with access token to obtain list of vehicles
class Vehicles:
    def __init__(self, headers):
        self.headers = headers

    def send_list_request(self):
        # send request to get response with list of vehicles
        result = requests.get(API_URL, headers=self.headers)
        if not result.ok:
            # handle error code for invalid response
            print(result)

        # get JSON for in/valid response
        try:
            response = result.json()
        except:
            return

        if "error_description" in response:
            # handle response for invalid request
            print(response["error_description"])
        else:
            # store refresh token and authorization headers for API calls
            print(response)

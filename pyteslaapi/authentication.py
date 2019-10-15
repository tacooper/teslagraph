#!/usr/bin/python3

import requests
import sys

# define constants
CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"

# uses account email/password or refresh token to obtain access token for authenticating API calls
class Authentication:
    def __init__(self):
        self.refresh_token = None
        self.headers = None

    def send_initial_request(self, email, password):
        # build request with email/password
        request_data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "email": email,
            "password": password
        }

        self.send_request(request_data)

    def send_refresh_request(self):
        # build request with refresh token
        request_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": self.refresh_token
        }

        self.send_request(request_data)

    def send_request(self, request_data):
        # send request to get response with access token
        response = requests.post("https://owner-api.teslamotors.com/oauth/token", data=request_data).json()
        if "error_description" in response:
            # handle response for invalid request
            print(response["error_description"])
        elif "response" in response:
            # handle response for invalid request
            print(response["response"])
        else:
            # store refresh token and authorization headers for API calls
            self.refresh_token = response["refresh_token"]
            self.headers = {
                "Authorization": "Bearer " + response["access_token"]
            }
